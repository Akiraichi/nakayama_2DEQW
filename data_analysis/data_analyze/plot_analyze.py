import pandas as pd
import matplotlib.pyplot as plt
from data_analysis.data_analyze.analyzer import AnalyzeData, OptimizeData
import helper
from typing import List

from config.config_data_analyze import AnalyzeNameSetting, DefaultAnalyzePlotSetting, DefaultOptimizePlotSetting, \
    OptimizeNameSetting


class OptimizePlotter:
    def __init__(self, qw1, qw2, analyze_indexes, analyze_t):
        self.__exp1_name = qw1.conditions[0].exp_name
        self.__exp2_name = qw2.conditions[0].exp_name
        self.__exp1_index = 0
        self.__exp2_indexes = analyze_indexes
        self.__analyze_t = analyze_t
        self.__all_optimize_data = self.__load_all_optimize_data()

    def __load_all_optimize_data(self):
        optimize_data_list = [self.__load_single_optimize_data(index=exp2_index) for exp2_index in self.__exp2_indexes]
        return optimize_data_list

    def __load_single_optimize_data(self, index):
        setting = OptimizeNameSetting(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
                                      exp2_name=self.__exp2_name, analyze_t=self.__analyze_t, file_index=index)
        return helper.load_file_by_error_handling(file_path=f"{setting.path_to_file}/{setting.file_name}")

    def print_all_optimize_result(self):
        for optimize_data in self.__all_optimize_data:
            self.__print_single_optimize_result(optimize_data)

    @staticmethod
    def __print_single_optimize_result(optimize_data, count=3):
        print(f"KL_div：")
        for optimize_KL_div in optimize_data.KL_div[:count]:
            print(optimize_KL_div)
        print(f"L1_norm：")
        for optimize_L1_norm in optimize_data.L1_norm[:count]:
            print(optimize_L1_norm)
        print(f"L2_norm：")
        for optimize_L2_norm in optimize_data.L2_norm[:count]:
            print(optimize_L2_norm)
        print(f"correlation_coefficient：")
        for optimize_correlation_coefficient in optimize_data.correlation_coefficient[:3]:
            print(optimize_correlation_coefficient)

    def plot_optimize_result_x_axis_is_rank(self):
        for optimize_data in self.__all_optimize_data:
            self.__plot_KL_div_x_axis_is_rank(optimize_data)
            self.__plot_L1_norm_x_axis_is_rank(optimize_data)
            self.__plot_L2_norm_x_axis_is_rank(optimize_data)
            self.__plot_correlation_coefficient_x_axis_is_rank(optimize_data)

    def __plot_KL_div_x_axis_is_rank(self, optimize_data: OptimizeData):
        y_axis_data_list = optimize_data.KL_divergence
        title = f"{self.__analyze_t}step KL divergence"
        x_axis_data_list = list(range(1, len(y_axis_data_list)))
        plot_setting = DefaultOptimizePlotSetting.x_axis_is_rank_prepare(exp1_name=self.__exp1_name,
                                                                         exp1_index=self.__exp1_index,
                                                                         exp2_name=self.__exp2_name,
                                                                         analyze_t=self.__analyze_t,
                                                                         x_axis_data_list=x_axis_data_list,
                                                                         y_axis_data_list=y_axis_data_list,
                                                                         title=title)

        helper.plot_multi_scatter(plot_setting)

    def __plot_L1_norm_x_axis_is_rank(self, optimize_data: OptimizeData):
        y_axis_data_list = optimize_data.L1_norm
        title = f"{self.__analyze_t}step L1 norm"
        x_axis_data_list = list(range(1, len(y_axis_data_list)))
        plot_setting = DefaultOptimizePlotSetting.x_axis_is_rank_prepare(exp1_name=self.__exp1_name,
                                                                         exp1_index=self.__exp1_index,
                                                                         exp2_name=self.__exp2_name,
                                                                         analyze_t=self.__analyze_t,
                                                                         x_axis_data_list=x_axis_data_list,
                                                                         y_axis_data_list=y_axis_data_list,
                                                                         title=title)

        helper.plot_multi_scatter(plot_setting)

    def __plot_L2_norm_x_axis_is_rank(self, optimize_data: OptimizeData):
        y_axis_data_list = optimize_data.L2_norm
        title = f"{self.__analyze_t}step L2 norm"
        x_axis_data_list = list(range(1, len(y_axis_data_list)))
        plot_setting = DefaultOptimizePlotSetting.x_axis_is_rank_prepare(exp1_name=self.__exp1_name,
                                                                         exp1_index=self.__exp1_index,
                                                                         exp2_name=self.__exp2_name,
                                                                         analyze_t=self.__analyze_t,
                                                                         x_axis_data_list=x_axis_data_list,
                                                                         y_axis_data_list=y_axis_data_list,
                                                                         title=title)

        helper.plot_multi_scatter(plot_setting)

    def __plot_correlation_coefficient_x_axis_is_rank(self, optimize_data: OptimizeData):
        y_axis_data_list = optimize_data.correlation_coefficient
        title = f"{self.__analyze_t}step correlation_coefficient"
        x_axis_data_list = list(range(1, len(y_axis_data_list)))
        plot_setting = DefaultOptimizePlotSetting.x_axis_is_rank_prepare(exp1_name=self.__exp1_name,
                                                                         exp1_index=self.__exp1_index,
                                                                         exp2_name=self.__exp2_name,
                                                                         analyze_t=self.__analyze_t,
                                                                         x_axis_data_list=x_axis_data_list,
                                                                         y_axis_data_list=y_axis_data_list,
                                                                         title=title)

        helper.plot_multi_scatter(plot_setting)

    def plot_optimize_result_x_axis_is_index(self):
        self.__plot_KL_div_x_axis_is_index(self.__all_optimize_data)
        # self.__plot_L1_norm_x_axis_is_index(self.__all_optimize_data)
        # self.__plot_L2_norm_x_axis_is_index(self.__all_optimize_data)
        # self.__plot_correlation_coefficient_x_axis_is_index(self.__all_optimize_data)

    @staticmethod
    def __convert_to_plot_data_x_axis_is_index(optimize_data_list: List[OptimizeData]):
        y_axis_data_list = [optimize_data.KL_divergence[:5] for optimize_data in optimize_data_list]
        y_axis_data_list = [list(data_tuple) for data_tuple in zip(*y_axis_data_list)]  # 転置
        return y_axis_data_list
        # 上位10位までのデータを取得する

    def __plot_KL_div_x_axis_is_index(self, optimize_data_list: List[OptimizeData]):
        y_axis_data_list = self.__convert_to_plot_data_x_axis_is_index(optimize_data_list)
        title = f"{self.__analyze_t}step KL divergence"
        plot_setting = DefaultOptimizePlotSetting.x_axis_is_index_prepare(exp1_name=self.__exp1_name,
                                                                          exp1_index=self.__exp1_index,
                                                                          exp2_name=self.__exp2_name,
                                                                          analyze_t=self.__analyze_t,
                                                                          x_axis_data_list=self.__exp2_indexes,
                                                                          y_axis_data_list=y_axis_data_list,
                                                                          title=title)

        helper.plot_multi_scatter(plot_setting)

    # def __plot_L1_norm_x_axis_is_index(self, optimize_data: OptimizeData):
    #     y_axis_data_list = optimize_data.L1_norm
    #     title = f"{self.__analyze_t}step L1 norm"
    #     plot_setting = DefaultOptimizePlotSetting.x_axis_is_index_prepare(exp1_name=self.__exp1_name,
    #                                                                       exp1_index=self.__exp1_index,
    #                                                                       exp2_name=self.__exp2_name,
    #                                                                       analyze_t=self.__analyze_t,
    #                                                                       x_axis_data_list=self.__exp2_indexes,
    #                                                                       y_axis_data_list=y_axis_data_list,
    #                                                                       title=title)
    #
    #     helper.plot_multi_scatter(plot_setting)
    #
    # def __plot_L2_norm_x_axis_is_index(self, optimize_data: OptimizeData):
    #     y_axis_data_list = optimize_data.L2_norm
    #     title = f"{self.__analyze_t}step L2 norm"
    #     plot_setting = DefaultOptimizePlotSetting.x_axis_is_index_prepare(exp1_name=self.__exp1_name,
    #                                                                       exp1_index=self.__exp1_index,
    #                                                                       exp2_name=self.__exp2_name,
    #                                                                       analyze_t=self.__analyze_t,
    #                                                                       x_axis_data_list=self.__exp2_indexes,
    #                                                                       y_axis_data_list=y_axis_data_list,
    #                                                                       title=title)
    #
    #     helper.plot_multi_scatter(plot_setting)
    #
    # def __plot_correlation_coefficient_x_axis_is_index(self, optimize_data: OptimizeData):
    #     y_axis_data_list = optimize_data.correlation_coefficient
    #     title = f"{self.__analyze_t}step correlation_coefficient"
    #     plot_setting = DefaultOptimizePlotSetting.x_axis_is_index_prepare(exp1_name=self.__exp1_name,
    #                                                                       exp1_index=self.__exp1_index,
    #                                                                       exp2_name=self.__exp2_name,
    #                                                                       analyze_t=self.__analyze_t,
    #                                                                       x_axis_data_list=self.__exp2_indexes,
    #                                                                       y_axis_data_list=y_axis_data_list,
    #                                                                       title=title)
    #
    #     helper.plot_multi_scatter(plot_setting)


class AnalyzePlotter:
    def __init__(self, exp1_name, exp2_name, exp1_index, analyze_indexes, plot_list,
                 setting: DefaultAnalyzePlotSetting):
        self.__exp1_name = exp1_name
        self.__exp2_name = exp2_name
        self.__exp1_index = exp1_index
        self.__exp2_indexes = analyze_indexes
        self.__plot_list = plot_list
        self.__analyze_data_list = self.__load_analyze_data()
        self.__setting = setting
        # self.__DefaultPlotSetting_x_axis_is_t = {
        #     "plot_indexes": plot_list,  # t_erase_list
        #     "x_label": "t",
        #     "y_label": None,
        #     "folder_path": AnalyzeNameSetting(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
        #                                       exp2_name=self.__exp2_name, exp2_index=self.__exp2_indexes[0],
        #                                       mode="analyze").folder_path,
        #     "file_name": None,
        #     "legend_label": "t_{erase}",
        #     "start_t": start_t
        # }
        # self.__DefaultPlotSetting_x_axis_is_index = {
        #     "plot_t_list": plot_list,  # t_list
        #     "x_label": "t_{erase}",
        #     "y_label": None,
        #     "folder_path": AnalyzeNameSetting(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
        #                                       exp2_name=self.__exp2_name, exp2_index=self.__exp2_indexes[0],
        #                                       mode="analyze").folder_path,
        #     "file_name": None,
        #     "legend_label": "t"
        # }

    def plot(self):
        if self.__analyze_data_list[0].KL_div:
            self.__setting.y_label = "KL divergence"
            self.__plot_core()
        if self.__analyze_data_list[0].L1_norm:
            self.__setting.y_label = "L1 norm"
            self.__plot_core()
        if self.__analyze_data_list[0].L2_norm:
            self.__setting.y_label = "L2 norm"
            self.__plot_core()
        if self.__analyze_data_list[0].correlation_coefficient:
            self.__setting.y_label = "correlation coefficient"
            self.__plot_core()

    def __plot_core(self):
        # dataをまとめた後、dfに変換してplot関数へ渡す
        df = self.__marge_data_and_convert_to_df(self.__analyze_data_list, self.__exp2_indexes,
                                                 model=self.__setting.y_label)
        # x_axisに指定されたモードに応じてプロット方法を変える
        self.__setting.file_name = self.__get_file_name()
        if self.__setting.x_axis == "index":
            plot_x_axis_is_index(df=df, setting=self.__setting)
        elif self.__setting.x_axis == "t":
            plot_x_axis_is_t(df=df, setting=self.__setting)
        else:
            helper.print_warning("axisパラメータに不正値が入力されています")
            raise OSError

    def __get_file_name(self):
        if self.__setting.x_axis == "index":
            return f"{self.__setting.y_label}_{self.__setting.plot_indexes}"
        elif self.__setting.x_axis == "t":
            return f"{self.__setting.y_label}_start_t={self.__setting.start_t}_{self.__setting.plot_indexes}"
        else:
            helper.print_warning("axisパラメータに不正値が入力されています")
            raise OSError

    def __load_analyze_data(self):
        analyze_data_list = []
        for exp2_index in self.__exp2_indexes:
            setting = AnalyzeNameSetting(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
                                         exp2_name=self.__exp2_name, file_index=exp2_index)
            analyze_data = helper.load_file_by_error_handling(file_path=f"{setting.path_to_file}/{setting.file_name}")
            analyze_data_list.append(analyze_data)
        return analyze_data_list

    @staticmethod
    def __marge_data_and_convert_to_df(analyze_data_list, exp2_indexes, model):
        """複数のデータをまとめて一つのdfにする"""
        if model == "KL divergence":
            data_dict = {"t": analyze_data_list[0].t}  # 代表して0番目のanalyze_dataのtを使う
            for analyze_data, exp2_index in zip(analyze_data_list, exp2_indexes):
                data_dict = {**data_dict, **{f"{exp2_index}": analyze_data.KL_div}}
            return pd.DataFrame(data_dict)

        elif model == "L1 norm":
            data_dict = {"t": analyze_data_list[0].t}  # 代表して0番目のanalyze_dataのtを使う
            for analyze_data, exp2_index in zip(analyze_data_list, exp2_indexes):
                data_dict = {**data_dict, **{f"{exp2_index}": analyze_data.L1_norm}}
            return pd.DataFrame(data_dict)

        elif model == "L2 norm":
            data_dict = {"t": analyze_data_list[0].t}  # 代表して0番目のanalyze_dataのtを使う
            for analyze_data, exp2_index in zip(analyze_data_list, exp2_indexes):
                data_dict = {**data_dict, **{f"{exp2_index}": analyze_data.L2_norm}}
            return pd.DataFrame(data_dict)

        elif model == "correlation coefficient":
            data_dict = {"t": analyze_data_list[0].t}  # 代表して0番目のanalyze_dataのtを使う
            for analyze_data, exp2_index in zip(analyze_data_list, exp2_indexes):
                data_dict = {**data_dict, **{f"{exp2_index}": analyze_data.correlation_coefficient}}
            return pd.DataFrame(data_dict)


def plot_x_axis_is_index(df, setting: DefaultAnalyzePlotSetting):
    # dfのラベルをlabelを使って見やすくする
    df = change_df_index_name(df=df, legend_label=setting.legend_label)

    """plot_tステップ目のデータを抽出してプロットする"""
    ax = df.loc[f"$t={setting.plot_indexes[0]}$"].plot(grid=True, x="t=0", figsize=(8, 6))
    ax.set_xlabel(f"${setting.x_label}$", size=24, labelpad=5)
    ax.set_ylabel(f"${setting.y_label}$", size=24)

    for i in range(1, len(setting.plot_indexes)):
        df.loc[f"$t={setting.plot_indexes[i]}$"].plot(grid=True, x="t", figsize=(8, 6), ax=ax)  # 同じ表に次々とプロットしていく
    plt.legend()
    plt.savefig(f"{setting.path_to_file}/{setting.file_name}.png", dpi=400)
    ax.cla()
    plt.close()


def plot_x_axis_is_t(df, setting: DefaultAnalyzePlotSetting):
    # dfのラベルをlabelを使って見やすくする
    df = change_column_name(df=df, legend_label=setting.legend_label)

    """dfの中から指定したindexのものを抽出する"""
    select = []
    for index_ in setting.plot_indexes:
        s = f"${setting.legend_label}={index_}$"
        select.append(s)
    df = df[select]

    """start_tから先のものを抽出する"""
    # start_tのindex番号を取得する
    index = df.index.get_loc(setting.start_t)  # dfのt=start_tの行番号を取得する
    # index番号以降のデータを抽出する
    df = df[index:]

    """plotする"""
    ax = df.plot(grid=True, figsize=(8, 6))
    ax.set_xlabel(f"${setting.x_label}$", size=24, labelpad=5)
    ax.set_ylabel(f"${setting.y_label}$", size=24)
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()
    plt.savefig(f"{setting.path_to_file}/{setting.file_name}.png", dpi=400)


def change_df_index_name(df, legend_label):
    # index名を変更する
    df = df.set_index("t")  # 列名がtである列をindexとして使用する
    index_list = df.index.values  # 今の行名を全て取得する
    index_list = [f"${legend_label}={str(index)}$" for index in index_list]
    df = df.set_axis(index_list, axis='index')  # 行名を一括して書き換える
    return df


def change_column_name(df, legend_label):
    df = df.set_index("t")  # 列名がtである列をindexとして使用する
    # column名を変更する
    column_list = df.columns.values  # 今の列名を全て取得する
    for i in range(len(column_list)):
        column_list[i] = f"${legend_label}={int(column_list[i])}$"
    df = df.set_axis(column_list, axis='columns')  # 列名を一括して書き換える
    return df