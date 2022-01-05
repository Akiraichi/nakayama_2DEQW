# config
import pandas as pd
import matplotlib.pyplot as plt
from analyze.visualization.analyzer import AnalyzeData
from config.config import *


class AnalyzePlotter:
    def __init__(self, qw1, qw2, analyze_indexes):
        self.__exp1_name = qw1.conditions[0].exp_name
        self.__exp2_name = qw2.conditions[0].exp_name
        self.__exp1_index = 0
        self.__exp2_indexes = analyze_indexes
        self.__analyze_data_list = self.__load_analyze_data()

    def plot_x_axis_is_t(self, plot_t_list):
        DefaultPlotSetting = {
            "plot_t_list": plot_t_list,
            "x_label": "t_{erase}",
            "folder_path": AnalyzeSetting(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
                                          exp2_name=self.__exp2_name, exp2_index=self.__exp2_indexes[0]).folder_path
            # 代表して0番にしておく
        }
        if self.__analyze_data_list[0].KL_div:
            df = self.__marge_data_and_convert_to_df(self.__analyze_data_list, self.__exp2_indexes, type="KL_div")
            plot_only_t_s(**{**DefaultPlotSetting, **{"df": df,
                                                      "y_label": "KL_divergence",
                                                      "file_name": "KL_divergence"}})
        if self.__analyze_data_list[0].L1_norm:
            df = self.__marge_data_and_convert_to_df(self.__analyze_data_list, self.__exp2_indexes, type="L1_norm")
            plot_only_t_s(**{**DefaultPlotSetting, **{"df": df,
                                                      "y_label": "L1_norm",
                                                      "file_name": "L1_norm"}})
        if self.__analyze_data_list[0].L2_norm:
            df = self.__marge_data_and_convert_to_df(self.__analyze_data_list, self.__exp2_indexes, type="L2_norm")
            plot_only_t_s(**{**DefaultPlotSetting, **{"df": df,
                                                      "y_label": "L2_norm",
                                                      "file_name": "L2_norm"}})
        if self.__analyze_data_list[0].correlation_coefficient:
            df = self.__marge_data_and_convert_to_df(self.__analyze_data_list, self.__exp2_indexes,
                                                     type="correlation_coefficient")
            plot_only_t_s(**{**DefaultPlotSetting, **{"df": df, "y_label": "correlation_coefficient",
                                                      "file_name": "correlation_coefficient"}})

    def __load_analyze_data(self):
        analyze_data_list = []
        for exp2_index in self.__exp2_indexes:
            setting = AnalyzeSetting(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
                                     exp2_name=self.__exp2_name, exp2_index=exp2_index)
            analyze_data = AnalyzeData.load(folder_path=setting.folder_path, file_name=setting.file_name)
            analyze_data_list.append(analyze_data)
        return analyze_data_list

    @staticmethod
    def __marge_data_and_convert_to_df(analyze_data_list, exp2_indexes, type):
        if type == "KL_div":
            data_dict = {"t": analyze_data_list[0].t}  # 代表して0番目のanalyze_dataのtを使う
            for analyze_data, exp2_index in zip(analyze_data_list, exp2_indexes):
                data_dict = {**data_dict, **{f"{exp2_index}": analyze_data.KL_div}}
            return change_df_index_name(data_dict=data_dict)

        elif type == "L1_norm":
            data_dict = {"t": analyze_data_list[0].t}  # 代表して0番目のanalyze_dataのtを使う
            for analyze_data, exp2_index in zip(analyze_data_list, exp2_indexes):
                data_dict = {**data_dict, **{f"{exp2_index}": analyze_data.L1_norm}}
            return change_df_index_name(data_dict=data_dict)

        elif type == "L2_norm":
            data_dict = {"t": analyze_data_list[0].t}  # 代表して0番目のanalyze_dataのtを使う
            for analyze_data, exp2_index in zip(analyze_data_list, exp2_indexes):
                data_dict = {**data_dict, **{f"{exp2_index}": analyze_data.L2_norm}}
            return change_df_index_name(data_dict=data_dict)

        elif type == "correlation_coefficient":
            data_dict = {"t": analyze_data_list[0].t}  # 代表して0番目のanalyze_dataのtを使う
            for analyze_data, exp2_index in zip(analyze_data_list, exp2_indexes):
                data_dict = {**data_dict, **{f"{exp2_index}": analyze_data.correlation_coefficient}}
            return change_df_index_name(data_dict=data_dict)


def change_df_index_name(data_dict):
    df = pd.DataFrame(data_dict)
    # 行名を変更する
    df = df.set_index("t")  # 列名がtである列をindexとして使用する
    index_list = df.index.values  # 今の行名を全て取得する
    index_list = ["t=" + str(index) for index in index_list]
    df = df.set_axis(index_list, axis='index')  # 行名を一括して書き換える
    return df


def plot_only_t_s(df, plot_t_list, x_label, y_label, folder_path, file_name):
    # プロットする
    ax = df.loc["t=" + str(plot_t_list[0])].plot(grid=True, x="t=0", figsize=(8, 6))  # plot_tステップ目のデータを抽出してプロットする
    ax.set_xlabel(f"${x_label}$", size=24, labelpad=5)
    ax.set_ylabel(f"${y_label}$", size=24)

    for i in range(1, len(plot_t_list)):
        df.loc["t=" + str(plot_t_list[i])].plot(grid=True, x="t", figsize=(8, 6), ax=ax)  # 同じ表に次々とプロットしていく
    plt.legend()
    plt.savefig(f"{folder_path}/{file_name}.png", dpi=400)
    ax.cla()
    plt.close()
