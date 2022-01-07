import pandas as pd
import matplotlib.pyplot as plt
from analyze.visualization.analyzer import AnalyzeData
from config.config import *
from helper import load_data_by_error_handling


class OptimizePlotter:
    def __init__(self, qw1, qw2, analyze_indexes, analyze_t):
        self.__exp1_name = qw1.conditions[0].exp_name
        self.__exp2_name = qw2.conditions[0].exp_name
        self.__exp1_index = 0
        self.__exp2_indexes = analyze_indexes
        self.__analyze_t = analyze_t

        # データをロードする
        self.__optimized_data_dict_list = []
        self.__load_data()

    def __load_data(self):
        for exp2_index in self.__exp2_indexes:
            setting = AnalyzeSetting(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
                                     exp2_name=self.__exp2_name, exp2_index=exp2_index,
                                     mode="optimize", analyze_t=self.__analyze_t)
            optimized_data_dict = load_data_by_error_handling(f"{setting.folder_path}/{setting.file_name}")
            self.__optimized_data_dict_list.append(optimized_data_dict)

    def print_optimized_result(self):
        for i, exp2_index in enumerate(self.__exp2_indexes):
            optimize_KL_div_list = self.__optimized_data_dict_list[i]["KL_div"]
            optimize_L1_norm_list = self.__optimized_data_dict_list[i]["L1_norm"]
            optimize_L2_norm_list = self.__optimized_data_dict_list[i]["L2_norm"]
            optimize_correlation_coefficient_list = self.__optimized_data_dict_list[i]["correlation_coefficient"]
            print(f"KL_div：")
            for optimize_KL_div in optimize_KL_div_list[:3]:
                print(optimize_KL_div)
            print(f"L1_norm：")
            for optimize_L1_norm in optimize_L1_norm_list[:3]:
                print(optimize_L1_norm)
            print(f"L2_norm：")
            for optimize_L2_norm in optimize_L2_norm_list[:3]:
                print(optimize_L2_norm)
            print(f"correlation_coefficient：")
            for optimize_correlation_coefficient in optimize_correlation_coefficient_list[:3]:
                print(optimize_correlation_coefficient)


class AnalyzePlotter:
    def __init__(self, qw1, qw2, analyze_indexes, plot_list, x_axis, start_t=None):
        self.__exp1_name = qw1.conditions[0].exp_name
        self.__exp2_name = qw2.conditions[0].exp_name
        self.__exp1_index = 0
        self.__exp2_indexes = analyze_indexes
        self.__plot_list = plot_list
        self.__x_axis = x_axis  # 横軸をtにするかindexにするかを指定する
        self.__analyze_data_list = self.__load_analyze_data()
        self.__DefaultPlotSetting_x_axis_is_t = {
            "plot_indexes": plot_list,  # t_erase_list
            "x_label": "t",
            "y_label": None,
            "folder_path": AnalyzeSetting(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
                                          exp2_name=self.__exp2_name, exp2_index=self.__exp2_indexes[0],
                                          mode="analyze").folder_path,
            "file_name": None,
            "legend_label": "t_{erase}",
            "start_t": start_t
        }
        self.__DefaultPlotSetting_x_axis_is_index = {
            "plot_t_list": plot_list,  # t_list
            "x_label": "t_{erase}",
            "y_label": None,
            "folder_path": AnalyzeSetting(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
                                          exp2_name=self.__exp2_name, exp2_index=self.__exp2_indexes[0],
                                          mode="analyze").folder_path,
            "file_name": None,
            "legend_label": "t"
        }

    def plot(self):
        if self.__analyze_data_list[0].KL_div:
            y_label = "KL divergence"
            self.__plot_core(model=y_label, y_label=y_label)
        if self.__analyze_data_list[0].L1_norm:
            y_label = "L1 norm"
            self.__plot_core(model=y_label, y_label=y_label)
        if self.__analyze_data_list[0].L2_norm:
            y_label = "L2 norm"
            self.__plot_core(model=y_label, y_label=y_label)
        if self.__analyze_data_list[0].correlation_coefficient:
            y_label = "correlation coefficient"
            self.__plot_core(model=y_label, y_label=y_label)

    def __plot_core(self, model, y_label):
        # dataをまとめた後、dfに変換してplot関数へ渡す
        df = self.__marge_data_and_convert_to_df(self.__analyze_data_list, self.__exp2_indexes, model=model)
        # x_axisに指定されたモードに応じてプロット方法を変える
        if self.__x_axis == "index":
            plot_x_axis_is_index(df=df,
                                 **{**self.__DefaultPlotSetting_x_axis_is_index,
                                    **{"y_label": y_label, "file_name": self.__get_file_name(ext=model)}})
        elif self.__x_axis == "t":
            plot_x_axis_is_t(df=df, **{**self.__DefaultPlotSetting_x_axis_is_t,
                                       **{"y_label": y_label, "file_name": self.__get_file_name(ext=model)}})
        else:
            print_warning("axisパラメータに不正値が入力されています")
            raise OSError

    def __get_file_name(self, ext):
        if self.__x_axis == "index":
            return f"{ext}_{self.__DefaultPlotSetting_x_axis_is_index['plot_t_list']}"
        elif self.__x_axis == "t":
            return f"{ext}_start_t={self.__DefaultPlotSetting_x_axis_is_t['start_t']}_{self.__DefaultPlotSetting_x_axis_is_t['plot_indexes']}"

    def __load_analyze_data(self):
        analyze_data_list = []
        for exp2_index in self.__exp2_indexes:
            setting = AnalyzeSetting(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
                                     exp2_name=self.__exp2_name, exp2_index=exp2_index, mode="analyze")
            analyze_data = AnalyzeData.load(folder_path=setting.folder_path, file_name=setting.file_name)
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


def plot_x_axis_is_index(df, plot_t_list, x_label, y_label, folder_path, file_name, legend_label):
    # dfのラベルをlabelを使って見やすくする
    df = change_df_index_name(df=df, legend_label=legend_label)

    """plot_tステップ目のデータを抽出してプロットする"""
    ax = df.loc[f"$t={plot_t_list[0]}$"].plot(grid=True, x="t=0", figsize=(8, 6))
    ax.set_xlabel(f"${x_label}$", size=24, labelpad=5)
    ax.set_ylabel(f"${y_label}$", size=24)

    for i in range(1, len(plot_t_list)):
        df.loc[f"$t={plot_t_list[i]}$"].plot(grid=True, x="t", figsize=(8, 6), ax=ax)  # 同じ表に次々とプロットしていく
    plt.legend()
    plt.savefig(f"{folder_path}/{file_name}.png", dpi=400)
    ax.cla()
    plt.close()


def plot_x_axis_is_t(df, plot_indexes, x_label, y_label, folder_path, file_name, start_t, legend_label):
    # dfのラベルをlabelを使って見やすくする
    df = change_column_name(df=df, legend_label=legend_label)

    """dfの中から指定したindexのものを抽出する"""
    select = []
    for index_ in plot_indexes:
        s = f"${legend_label}={index_}$"
        select.append(s)
    df = df[select]

    """start_tから先のものを抽出する"""
    # start_tのindex番号を取得する
    index = df.index.get_loc(start_t)  # dfのt=start_tの行番号を取得する
    # index番号以降のデータを抽出する
    df = df[index:]

    """plotする"""
    ax = df.plot(grid=True, figsize=(8, 6))
    ax.set_xlabel(f"${x_label}$", size=24, labelpad=5)
    ax.set_ylabel(f"${y_label}$", size=24)
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()
    plt.savefig(f"{folder_path}/{file_name}.png", dpi=400)


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
