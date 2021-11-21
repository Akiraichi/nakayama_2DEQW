# config
import numpy as np

from config.config import *
# misc
from analyze.visualization.plot_image import select_plot_t_step
import joblib
import glob
from numba import njit
from analyze.visualization.plot_kl import get_probability


def main_analyze(exp_name, exp_indexes, cut_circle_r, circle_inner_r, circle_outer_r, ext):
    analyzer = Analyzer(exp_name, exp_indexes, cut_circle_r, circle_inner_r, circle_outer_r)
    if ext == "prob":
        analyzer.analyze_prob()  # 確率の総和を解析
    elif ext == "var":
        analyzer.analyze_var()  # 確率の分散を解析
    elif ext == "all":
        analyzer.analyze_all()
    else:
        print_warning("該当するものがありません")


class Analyzer:
    def __init__(self, exp_name, exp_indexes, cut_circle_r, circle_inner_r, circle_outer_r):
        self.exp_name = exp_name
        self.exp_indexes = exp_indexes
        self.cut_circle_r = cut_circle_r
        self.circle_inner_r = circle_inner_r
        self.circle_outer_r = circle_outer_r

    def analyze_all(self):
        for i, exp_index in enumerate(self.exp_indexes):
            analyzer = AnalyzerCore(self.exp_name, exp_index, self.cut_circle_r, self.circle_inner_r,
                                    self.circle_outer_r)
            analyzer.analyze_probability()
            analyzer.save_prob_csv_file()
            print("確率計算完了")

            analyzer.analyze_probability()
            analyzer.save_var_csv_file()
            print("分散計算完了")
        print_finish("全体完了")

    def analyze_prob(self):
        for i, exp_index in enumerate(self.exp_indexes):
            analyzer = AnalyzerCore(self.exp_name, exp_index, self.cut_circle_r, self.circle_inner_r,
                                    self.circle_outer_r)
            analyzer.analyze_probability()
            analyzer.save_prob_csv_file()
        print_finish("確率計算")

    def analyze_var(self):
        """
        中心付近の確率分布を半径＝rの円の内部とする。
        中心付近の確率分布において確率の分散を求める
        """
        for i, exp_index in enumerate(self.exp_indexes):
            analyzer = AnalyzerCore(self.exp_name, exp_index, self.cut_circle_r, self.circle_inner_r,
                                    self.circle_outer_r)
            analyzer.analyze_probability()
            analyzer.save_var_csv_file()
        print_finish("分散の計算")


class AnalyzerCore:
    def __init__(self, exp_name, exp_index, cut_circle_r, circle_inner_r, circle_outer_r):
        self.exp_name = exp_name
        self.exp_index = str(exp_index).zfill(4)
        self.cut_circle_r = cut_circle_r
        self.circle_inner_r = circle_inner_r
        self.circle_outer_r = circle_outer_r
        self.t_list = select_plot_t_step()
        self.p_in_circle_list = []
        self.p_out_circle_list = []
        self.p_circle_list = []

        self.var_list = []

        # 設定するための関数を実行
        self.__set_data_names()
        self.__set_plot_option()

    def __set_data_names(self):
        self.simulation_data_names = glob.glob(
            f"{config_simulation_data_save_path(self.exp_name, self.exp_index)}/*.jb")
        self.simulation_data_names.sort()  # 実験順にsortする。
        print(f"exp_nameのデータ数：{len(self.simulation_data_names)}")

    def __set_plot_option(self):
        folder_name = f'cut_r={self.cut_circle_r}_inner_r={self.circle_inner_r}_outer_r={self.circle_outer_r}_{self.exp_name}'
        # 保存先の設定
        self.save_prob_csv_path = config_prob_save_path(folder_name=folder_name)
        self.save_var_csv_path = config_var_save_path(folder_name=folder_name)

        # ファイル名を設定する
        self.file_name = folder_name + f"_{self.exp_index}"

        # プロットのタイトルを設定する
        # title設定のために一つデータをロードする。
        condition = joblib.load(self.simulation_data_names[0])["実験条件データ（condition）"]
        self.title = f"{self.exp_name}" + " " + "$t_{erase}$" + f"={condition.erase_t}"

    def __load_data(self):
        self.p1_list = []
        for t_step in self.t_list:
            print(self.exp_index, f"t={t_step}")
            p1 = get_probability(self.simulation_data_names, t_step)  # 全体の確率分布
            self.p1_list.append(p1)
        print_finish("データの事前ロード")

    def analyze_probability(self):
        for i, t_step in enumerate(self.t_list):
            print(self.exp_index, f"t={t_step}")
            # p1 = get_probability(self.simulation_data_names, t_step)  # 全体の確率分布
            p1 = self.p1_list[i]
            p_in_circle, p_out_circle, p_circle = get_prob(prob=p1, radius=self.cut_circle_r,
                                                           circle_inner_r=self.circle_inner_r,
                                                           circle_outer_r=self.circle_outer_r)
            self.p_in_circle_list.append(p_in_circle)
            self.p_out_circle_list.append(p_out_circle)
            self.p_circle_list.append(p_circle)

    def save_prob_csv_file(self):
        with open(f"{self.save_prob_csv_path}/{self.file_name}.csv", mode='w') as f:
            f.write(
                f"t,in_circle_{self.exp_index},out_circle_{self.exp_index},circle_{self.exp_index}\n")
            for i in range(len(self.p_in_circle_list)):
                s = f"{self.t_list[i]},{self.p_in_circle_list[i]},{self.p_out_circle_list[i]},{self.p_circle_list[i]}\n"
                f.write(s)

    def analyze_var(self):
        for i, t_step in enumerate(self.t_list):
            print(self.exp_index, f"t={t_step}")
            p1 = self.p1_list[i]
            var = get_var(prob=p1, radius=self.cut_circle_r)
            self.var_list.append(var)

    def save_var_csv_file(self):
        with open(f"{self.save_var_csv_path}/{self.file_name}.csv", mode='w') as f:
            f.write(
                f"t,var_{self.exp_index}\n")
            for i in range(len(self.var_list)):
                s = f"{self.t_list[i]},{self.var_list[i]}\n"
                f.write(s)


@njit('Tuple((f8,f8,f8))(f8[:,:],i8,i8,i8)', cache=True)
def get_prob(prob, radius, circle_inner_r, circle_outer_r):
    p_out_circle = 0  # 円形外の確率の和
    p_in_circle = 0  # 円形内の確率の和
    p_circle = 0  # 円周付近の確率の和

    len_x = prob.shape[1]
    len_y = prob.shape[0]
    T = len_x // 2
    for x in range(len_x):
        for y in range(len_y):
            if (x - T) ** 2 + (y - T) ** 2 < radius ** 2:
                # 円形内
                p_in_circle += prob[x, y]
            else:
                # 円形外
                p_out_circle += prob[x, y]
            if circle_inner_r ** 2 < (x - T) ** 2 + (y - T) ** 2 < circle_outer_r ** 2:
                # 円周付近の領域内
                p_circle += prob[x, y]

    # print("in circle", kl_div_in_circle)  # デバッグ用
    return p_in_circle, p_out_circle, p_circle


# @njit('Tuple((f8,f8,f8))(f8[:,:],i8,i8,i8)', cache=True)
def get_var(prob, radius):
    """
    prob：確率分布
    radius：中心付近の確率分布を定義するための半径r
    circle_inner_r：円周の確率分布を定義するための内半径
    circle_outer_r：円周の確率分布を定義するための外半径
    """

    in_circle_p = []  # 中心付近の確率分布のリスト

    len_x = prob.shape[1]
    len_y = prob.shape[0]
    T = len_x // 2
    for x in range(len_x):
        for y in range(len_y):
            if (x - T) ** 2 + (y - T) ** 2 < radius ** 2:
                # 円形内の確率prob[x,y]について分散を求める。
                in_circle_p.append(prob[x, y])
    var = np.var(in_circle_p)  # 分散を求める
    return var
