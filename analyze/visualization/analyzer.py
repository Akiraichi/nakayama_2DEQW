# calc
import glob
import itertools

import numpy as np
from helper import get_probability, load_data_by_error_handling, return_simulation_data_file_names, save_jb_file

# config
from config.config import *
# misc
from analyze.visualization.plot_image import select_plot_t_step
# import glob
from numba import njit
from multiprocessing import Pool


class AnalyzeData:
    def __init__(self, **data):
        self.__KL_div = data["KL_div"]
        self.__L1_norm = data["L1_norm"]
        self.__L2_norm = data["L2_norm"]
        self.__correlation_coefficient = data["correlation_coefficient"]
        self.__t = data["t"]

    def save(self, folder_path, file_name):
        """現在のインスタンスを保存する"""
        save_jb_file(self, folder_path, file_name)

    @staticmethod
    def load(folder_path, file_name):
        """保存したAnalyzeDataインスタンスを返却する"""
        return load_data_by_error_handling(f"{folder_path}/{file_name}")

    @property
    def KL_div(self):
        return self.__KL_div

    @property
    def L1_norm(self):
        return self.__L1_norm

    @property
    def L2_norm(self):
        return self.__L2_norm

    @property
    def correlation_coefficient(self):
        return self.__correlation_coefficient

    @property
    def t(self):
        return self.__t


class Analyzer:
    def __init__(self, qw1, qw2, analyze_indexes, options):
        self.__exp1_name = qw1.conditions[0].exp_name
        self.__exp2_name = qw2.conditions[0].exp_name
        self.__exp1_index = 0

        self.__not_analyzed_indexes = self.check_finished(
            folder_path=AnalyzeSetting(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
                                       exp2_name=self.__exp2_name, exp2_index=analyze_indexes[0]).folder_path,
            index_list=analyze_indexes)
        self.__options = options
        self.__parallel = self.__options["parallel"]
        self.__t_list = select_plot_t_step()  # 解析を実行する時間ステップ
        self.simulation_data_names_1 = return_simulation_data_file_names(exp_name=self.__exp1_name,
                                                                         exp_index=self.__exp1_index)
        self.__p1_list = []  # qw1のシミュレーション結果より求めた確率分布のリスト
        self.__load_qw1_data()  # 共通データ（qw1のシミュレーション結果データ）をロードする

    def __load_qw1_data(self):
        for t_step in self.__t_list:
            prob = get_probability(self.simulation_data_names_1, t_step)
            self.__p1_list.append(prob)
        print_finish("前処理完了")

    def start_processing(self):
        if self.__parallel:
            self.__start_parallel_processing()
        else:
            self.__start_single_processing()
        print_finish("FINISH：KLダイバージェンス")

    def __start_parallel_processing(self):
        arguments = []
        for exp2_index in self.__not_analyzed_indexes:
            arguments.append(
                [self.__exp1_name, self.__exp1_index, self.__exp2_name, exp2_index, self.__p1_list, self.__options])

        with Pool(ConfigSimulation.PlotParallelNum) as p:
            # 並列処理開始
            p.starmap(func=Analyzer.do, iterable=arguments)

    def __start_single_processing(self):
        for i, exp2_index in enumerate(self.__not_analyzed_indexes):
            print(i, "番目の処理")
            Analyzer.do(self.__exp1_name, self.__exp1_index, self.__exp2_name, exp2_index, self.__p1_list,
                        self.__options)

    @staticmethod
    def check_finished(folder_path, index_list):
        """
        処理が完了しているかを確認し、処理できていないファイルのみ処理する。
        """
        generated_files = glob.glob(f"{folder_path}/*.jb")  # すでに生成されたファイルの一覧
        generated_index_list = []  # すでに生成されたtの一覧
        for generated_file in generated_files:
            extract_index = int(generated_file[-7:-3])
            generated_index_list.append(extract_index)

        # 共通しない要素のうち、まだプロットされていないものを取得
        not_generated_index_list = set(index_list) - set(generated_index_list)

        if not not_generated_index_list:
            for generated_index in generated_index_list:
                print_green_text(f"index={generated_index}：既に完了")
        else:
            for not_generated_index in not_generated_index_list:
                print_warning(f"index={not_generated_index}：完了していません")
        return not_generated_index_list

    @staticmethod
    def do(exp1_name, exp1_index, exp2_name, exp2_index, p1_list, options):
        analyze_core = AnalyzerCore(exp1_name, exp1_index, exp2_name, exp2_index, p1_list, options)
        analyze_core.do()


class AnalyzerCore:
    def __init__(self, exp1_name, exp1_index, exp2_name, exp2_index, p1_list, options):
        self.__exp1_name = exp1_name
        self.__exp2_name = exp2_name
        self.__exp1_index = exp1_index
        self.__exp2_index = exp2_index
        self.__p1_list = p1_list
        # self.__options = options
        self.__enable_KL_div = options["KL_div"]
        self.__enable_L1_norm = options["L1_norm"]
        self.__enable_L2_norm = options["L2_norm"]
        self.__enable_correlation_coefficient = options["correlation_coefficient"]

        self.__t_list = select_plot_t_step()

        self.__simulation_data_names_2 = return_simulation_data_file_names(exp_name=self.__exp2_name,
                                                                           exp_index=self.__exp2_index)
        print(f"exp_name_2のデータ数：{len(self.__simulation_data_names_2)}")

    def do(self):
        KL_div_list = []
        L1_norm_list = []
        L2_norm_list = []
        correlation_coefficient_list = []

        for i, t_step in enumerate(self.__t_list):
            # t=t_stepのシミュレーションデータをロード
            p1 = self.__p1_list[i]
            p2 = get_probability(self.__simulation_data_names_2, t_step)
            KL_div, L1_norm, L2_norm = calc_KL_and_L1_and_L2(p1=p1, p2=p2, enable_KL_div=self.__enable_KL_div,
                                                             enable_L1_norm=self.__enable_L1_norm,
                                                             enable_L2_norm=self.__enable_L2_norm)
            correlation_coefficient = calc_correlation_coefficient(p1=p1, p2=p2,
                                                                   enable_correlation_coefficient=self.__enable_correlation_coefficient)

            if self.__enable_KL_div:
                KL_div_list.append(KL_div)
            if self.__enable_L1_norm:
                L1_norm_list.append(L1_norm)
            if self.__enable_L2_norm:
                L2_norm_list.append(L2_norm)
            if self.__enable_correlation_coefficient:
                correlation_coefficient_list.append(correlation_coefficient)
            print(self.__exp2_index, f"t={t_step}")

        self.__save(KL_div_list=KL_div_list, L1_norm_list=L1_norm_list, L2_norm_list=L2_norm_list,
                    correlation_coefficient_list=correlation_coefficient_list)
        print_finish(self.__exp2_index)

        # def __calc_KL_div(self, p1, p2):
        #     KL_div_list = []
        #     # __low_KL_div_lists = []
        #     for i, t_step in enumerate(self.__t_list):
        #         # その時のp2と全てのp1_listのp1とのKLダイバージェンスを求め、KLダイバージェンスが低い順にリストを返す
        #         # low_kl_div_list = find_near_KL(p1_list=p1_list, p2=p2)
        #         # low_kl_div_lists.append(low_kl_div_list)
        #
        #         # KL_div = calc_KL_div(p1=p1, p2=p2)
        #         # KL_div_list.append(KL_div)
        #         # print(self.__exp2_index, f"t={t_step}")
        #
        #     data_dict = {
        #         "KLdiv_list": KL_div_list,  # t=tの時のKLダイバージェンスの値
        #         "t": self.__t_list  # 時間ステップ
        #     }
        #     save_jb_file(data_dict, self.__DefaultSavePathSetting["KL_div"], self.__DefaultSaveFileName["KL_div"])
        #     # self.save_file_low_list(low_kl_div_lists, self.save_path_csv, f"{self.file_name}_low.jb")
        #     print_finish("KL_div")

    def __save(self, KL_div_list, L1_norm_list, L2_norm_list, correlation_coefficient_list):
        setting = AnalyzeSetting(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
                                 exp2_name=self.__exp2_name, exp2_index=self.__exp2_index)

        analyze_data = AnalyzeData(KL_div=KL_div_list, L1_norm=L1_norm_list, L2_norm=L2_norm_list,
                                   correlation_coefficient=correlation_coefficient_list, t=self.__t_list)
        analyze_data.save(setting.folder_path, setting.file_name)


@njit('Tuple((f8,f8,f8))(f8[:,:],f8[:,:],b1,b1,b1)', cache=True)
def calc_KL_and_L1_and_L2(p1, p2, enable_KL_div, enable_L1_norm, enable_L2_norm):
    """
        概要
            量子ウォークの確率分布のKLダイバージェンスを求める。ただし中心が原点で直径が指定した値である円形領域では、KLダイバージェンスの値を0とする（領域内を無視する）
            また、その領域内のKLダイバージェンスを求める。
        引数
            p1,p2：大きさの等しい2次元リストp1[x,y]のように指定できること。
        返却値
            円形領域を無視した場合のKLダイバージェンスと、その円形領域のKLダイバージェンスを返却する
        """
    # 変数を初期化
    KL_div = 0
    L1_norm = 0
    L2_norm = 0
    # 便利な変数を定義
    len_x = p1.shape[1]
    len_y = p1.shape[0]

    for x in range(len_x):
        for y in range(len_y):

            # KLダイバージェンスを求める場合は以下を実行
            if enable_KL_div:
                if p1[x, y] == 0:
                    continue
                if p2[x, y] == 0:
                    p2[x, y] = 10E-20
                KL_div += p1[x, y] * np.log(p1[x, y] / p2[x, y])

            # L1ノルムを求める場合は以下を実行
            if enable_L1_norm:
                """誤差の絶対値の和"""
                # 小さすぎる値でも処理できるようにしておく
                # 確率が1以上になるまで10を何度かければいいのか、その回数をcountに代入する。
                count = 1
                while (p1[x, y] * count) > 1.0:
                    count += 1
                L1_norm += np.abs(p1[x, y] * (10 ** count) - p2[x, y] * (10 ** count)) / (10 ** count)
            # L2ノルムを求める場合は以下を実行
            if enable_L2_norm:
                """二乗誤差の和"""
                # 小さすぎる値でも処理できるようにしておく
                # 確率が1以上になるまで10を何度かければいいのか、その回数をcountに代入する。
                count = 1
                while (p1[x, y] * count) > 1.0:
                    count += 1
                L2_norm += ((p1[x, y] * (10 ** count) - p2[x, y] * (10 ** count)) ** 2) / (10 ** (count * 2))
    return KL_div, L1_norm, L2_norm


def calc_correlation_coefficient(p1, p2, enable_correlation_coefficient):
    # 相関係数を求める場合は以下を実行
    correlation_coefficient = 0
    if enable_correlation_coefficient:
        data_1 = list(itertools.chain.from_iterable(p1))
        data_2 = list(itertools.chain.from_iterable(p2))

        # 相関行列を計算
        correlation_coefficient = np.corrcoef(data_1, data_2)

    return correlation_coefficient[0, 1]

# def find_near_KL(p1_list, p2):
#     """
#     その時のp2と全てのp1_listのp1とのKLダイバージェンスを求め、KLダイバージェンスが低い順にリストを返す
#     """
#     kl_div_list = []
#     for i, p1 in enumerate(p1_list):
#         kl_div, _ = calc_KL_div(p1=p1, p2=p2)
#         kl_div_list.append([i, kl_div])
#
#     # kl_divの小さい順に並べ替える
#     kl_div_list.sort()
#     kl_div_list = sorted(kl_div_list, key=lambda x: x[1])  # [1]に注目してソート
#     print(kl_div_list)
#     return kl_div_list

# def do_plot_graph(file_name, dates, t_list, title, xlabel, ylabel):
#     fig = plt.figure(figsize=(4, 3), tight_layout=True, dpi=400)
#     ax = fig.add_subplot(111, xlabel=xlabel, ylabel=ylabel)
#     ax.set_title(title, size=24)
#     ax.scatter(t_list, dates, c='blue')
#     fig.savefig(file_name)
#     print("FIN")
