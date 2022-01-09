from data_analysis.data_analyze.analyze_algorithm import calc_KL_and_L1_and_L2, calc_correlation_coefficient
from config.config_data_analyze import AnalyzeNameSetting, DefaultAnalyzeSetting, DefaultAnalyzeOptimizeSetting, \
    AnalysisOptimizeSaveName
import helper
from multiprocessing import Pool
from dataclasses import dataclass

from config.config_simulation import ConfigSimulationSetting
from typing import List


@dataclass(frozen=True)
class AnalyzeData:
    KL_div: List[float]
    L1_norm: List[float]
    L2_norm: List[float]
    correlation_coefficient: List[float]
    t: List[int]


@dataclass(frozen=True)
class OptimizeData:
    KL_divergence: list
    L1_norm: list
    L2_norm: list
    correlation_coefficient: list


class AnalyzeOptimizer:
    def __init__(self, exp1_name, exp2_name, exp1_index, analyze_indexes, setting: DefaultAnalyzeOptimizeSetting):
        self.__exp1_name = exp1_name
        self.__exp2_name = exp2_name
        self.__exp1_index = exp1_index
        self.__setting = setting
        self.__analyze_t = self.__setting.analyze_t
        self.__not_analyzed_indexes = helper.check_finished_file(
            folder_path=AnalysisOptimizeSaveName(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
                                                 exp2_name=self.__exp2_name, analyze_t=self.__analyze_t).path_to_file,
            will_generate_index_list=analyze_indexes, extension="jb")

        self.simulation_data_names_1 = helper.return_simulation_data_file_names(exp_name=self.__exp1_name,
                                                                                exp_index=self.__exp1_index)
        self.__p1_list = []  # qw1のシミュレーション結果より求めた確率分布のリスト
        self.__load_qw1_data()  # 共通データ（qw1のシミュレーション結果データ）をロードする

    def __load_qw1_data(self):
        self.__p1_list = [helper.get_probability(self.simulation_data_names_1, t_step) for t_step in
                          self.__setting.t_list]
        helper.print_finish("前処理完了")

    def optimize_t_all(self):
        for i, exp2_index in enumerate(self.__not_analyzed_indexes):
            print(i, "番目の処理")
            self.__optimize_t_single(exp2_index=exp2_index)

    def __optimize_t_single(self, exp2_index):
        optimize_correlation_coefficient_list = []
        optimize_KL_div_list = []
        optimize_L1_norm_list = []
        optimize_L2_norm_list = []

        # STEP1：analyze_tステップ目のp2のデータをロードする。
        simulation_data_names_2 = helper.return_simulation_data_file_names(exp_name=self.__exp2_name,
                                                                           exp_index=exp2_index)
        p2 = helper.get_probability(simulation_data_names_2, self.__analyze_t)

        # STEP2：最適な時間ステップを求める
        for p1, t in zip(self.__p1_list, self.__setting.t_list):
            KL_div, L1_norm, L2_norm = calc_KL_and_L1_and_L2(p1=p1, p2=p2,
                                                             enable_KL_div=self.__setting.enable_KL_divergence,
                                                             enable_L1_norm=self.__setting.enable_L1_norm,
                                                             enable_L2_norm=self.__setting.enable_L2_norm)
            correlation_coefficient = calc_correlation_coefficient(p1=p1, p2=p2,
                                                                   enable_correlation_coefficient=self.__setting.enable_correlation_coefficient)
            optimize_KL_div_list.append([t, KL_div])
            optimize_L1_norm_list.append([t, L1_norm])
            optimize_L2_norm_list.append([t, L2_norm])
            optimize_correlation_coefficient_list.append([t, correlation_coefficient])

        # STEP3：確率分布の類似性が高い順に並べ替える
        optimize_correlation_coefficient_list = sorted(optimize_correlation_coefficient_list, key=lambda x: x[1],
                                                       reverse=True)
        optimize_KL_div_list = sorted(optimize_KL_div_list, key=lambda x: x[1])
        optimize_L1_norm_list = sorted(optimize_L1_norm_list, key=lambda x: x[1])
        optimize_L2_norm_list = sorted(optimize_L2_norm_list, key=lambda x: x[1])

        # STEP4：保存する
        setting = AnalysisOptimizeSaveName(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
                                           exp2_name=self.__exp2_name, analyze_t=self.__analyze_t, file_index=exp2_index)
        optimize_data = OptimizeData(optimize_KL_div_list, optimize_L1_norm_list, optimize_L2_norm_list,
                                     optimize_correlation_coefficient_list)
        helper.save_jb_file(optimize_data, setting.path_to_file, setting.file_name_jb)


class Analyzer:
    def __init__(self, exp1_name, exp2_name, exp1_index, analyze_indexes, setting: DefaultAnalyzeSetting):
        self.__exp1_name = exp1_name
        self.__exp2_name = exp2_name
        self.__exp1_index = exp1_index

        self.__not_analyzed_indexes = helper.check_finished_file(
            folder_path=AnalyzeNameSetting(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
                                           exp2_name=self.__exp2_name, file_index=analyze_indexes[0]).path_to_file,
            will_generate_index_list=analyze_indexes, extension="jb")
        self.__setting = setting
        self.simulation_data_names_1 = helper.return_simulation_data_file_names(exp_name=self.__exp1_name,
                                                                                exp_index=self.__exp1_index)
        self.__load_qw1_data()  # 共通データ（qw1のシミュレーション結果データ）をロードする

    def __load_qw1_data(self):
        self.__p1_list = [helper.get_probability(self.simulation_data_names_1, t_step) for t_step in
                          self.__setting.t_list]
        helper.print_finish("前処理完了")

    def start_processing(self):
        if self.__setting.parallel:
            self.__start_parallel_processing()
        else:
            self.__start_single_processing()
        helper.print_finish("FINISH：Analyze")

    def __start_parallel_processing(self):
        arguments = [[self.__exp1_name, self.__exp1_index, self.__exp2_name, exp2_index, self.__p1_list, self.__setting]
                     for exp2_index in self.__not_analyzed_indexes]

        with Pool(ConfigSimulationSetting.PlotParallelNum) as p:
            # 並列処理開始
            p.starmap(func=self.single_analyze_do, iterable=arguments)

    def __start_single_processing(self):
        for i, exp2_index in enumerate(self.__not_analyzed_indexes):
            print(i, "番目の処理")
            self.single_analyze_do(self.__exp1_name, self.__exp1_index, self.__exp2_name, exp2_index, self.__p1_list,
                                   self.__setting)
            helper.print_finish(exp2_index)

    @staticmethod
    def single_analyze_do(exp1_name, exp1_index, exp2_name, exp2_index, p1_list, setting):
        # STEP1-1：使用するリストを初期化
        KL_div_list = []
        L1_norm_list = []
        L2_norm_list = []
        correlation_coefficient_list = []
        # STEP1-2：使用する変数を求める
        simulation_data_names_2 = helper.return_simulation_data_file_names(exp_name=exp2_name,
                                                                           exp_index=exp2_index)
        print(f"exp_name_2のデータ数：{len(simulation_data_names_2)}")

        # STEP2：解析を実行する
        for i, t_step in enumerate(setting.t_list):
            # t=t_stepのシミュレーションデータをロード
            p1 = p1_list[i]
            p2 = helper.get_probability(simulation_data_names_2, t_step)
            KL_div, L1_norm, L2_norm = calc_KL_and_L1_and_L2(p1=p1, p2=p2,
                                                             enable_KL_div=setting.enable_KL_divergence,
                                                             enable_L1_norm=setting.enable_L1_norm,
                                                             enable_L2_norm=setting.enable_L2_norm)
            correlation_coefficient = calc_correlation_coefficient(p1=p1, p2=p2,
                                                                   enable_correlation_coefficient=setting.enable_correlation_coefficient)

            if setting.enable_KL_divergence:
                KL_div_list.append(KL_div)
            if setting.enable_L1_norm:
                L1_norm_list.append(L1_norm)
            if setting.enable_L2_norm:
                L2_norm_list.append(L2_norm)
            if setting.enable_correlation_coefficient:
                correlation_coefficient_list.append(correlation_coefficient)
            print(exp2_index, f"t={t_step}")
        # STEP3: 保存する
        Analyzer.save_AnalyzeData(exp1_name, exp1_index, exp2_name, exp2_index, AnalyzeData(KL_div=KL_div_list,
                                                                                            L1_norm=L1_norm_list,
                                                                                            L2_norm=L2_norm_list,
                                                                                            correlation_coefficient=correlation_coefficient_list,
                                                                                            t=setting.t_list))

    @staticmethod
    def save_AnalyzeData(exp1_name, exp1_index, exp2_name, exp2_index, analyze_data):
        # STEP3：保存する
        name_setting = AnalyzeNameSetting(exp1_name=exp1_name, exp1_index=exp1_index,
                                          exp2_name=exp2_name, file_index=exp2_index)
        helper.save_jb_file(analyze_data, name_setting.path_to_file, name_setting.file_name_jb)

#
# class AnalyzerCore:
#     def __init__(self, exp1_name, exp1_index, exp2_name, exp2_index, p1_list, setting: DefaultAnalyzeSetting):
#         self.__exp1_name = exp1_name
#         self.__exp2_name = exp2_name
#         self.__exp1_index = exp1_index
#         self.__exp2_index = exp2_index
#         self.__p1_list = p1_list
#         self.__setting = setting
#         self.__simulation_data_names_2 = helper.return_simulation_data_file_names(exp_name=self.__exp2_name,
#                                                                                   exp_index=self.__exp2_index)
#         print(f"exp_name_2のデータ数：{len(self.__simulation_data_names_2)}")
#
#     def do(self):
#         KL_div_list = []
#         L1_norm_list = []
#         L2_norm_list = []
#         correlation_coefficient_list = []
#
#         for i, t_step in enumerate(self.__setting.t_list):
#             # t=t_stepのシミュレーションデータをロード
#             p1 = self.__p1_list[i]
#             p2 = helper.get_probability(self.__simulation_data_names_2, t_step)
#             KL_div, L1_norm, L2_norm = calc_KL_and_L1_and_L2(p1=p1, p2=p2,
#                                                              enable_KL_div=self.__setting.enable_KL_divergence,
#                                                              enable_L1_norm=self.__setting.enable_L1_norm,
#                                                              enable_L2_norm=self.__setting.enable_L2_norm)
#             correlation_coefficient = calc_correlation_coefficient(p1=p1, p2=p2,
#                                                                    enable_correlation_coefficient=self.__setting.enable_correlation_coefficient)
#
#             if self.__setting.enable_KL_divergence:
#                 KL_div_list.append(KL_div)
#             if self.__setting.enable_L1_norm:
#                 L1_norm_list.append(L1_norm)
#             if self.__setting.enable_L2_norm:
#                 L2_norm_list.append(L2_norm)
#             if self.__setting.enable_correlation_coefficient:
#                 correlation_coefficient_list.append(correlation_coefficient)
#             print(self.__exp2_index, f"t={t_step}")
#
#         self.__save(KL_div_list=KL_div_list, L1_norm_list=L1_norm_list, L2_norm_list=L2_norm_list,
#                     correlation_coefficient_list=correlation_coefficient_list)
#         helper.print_finish(self.__exp2_index)
#
#     def __save(self, KL_div_list, L1_norm_list, L2_norm_list, correlation_coefficient_list):
#         setting = AnalyzeNameSetting(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
#                                      exp2_name=self.__exp2_name, file_index=self.__exp2_index)
#
#         analyze_data = AnalyzeData(KL_div=KL_div_list, L1_norm=L1_norm_list, L2_norm=L2_norm_list,
#                                    correlation_coefficient=correlation_coefficient_list, t=self.__setting.t_list)
#         helper.save_jb_file(analyze_data, setting.path_to_file, setting.file_name)
