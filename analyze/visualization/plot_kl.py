# calc
import numpy as np
from simulation.simulation_core import calc_probability
# plot
import matplotlib.pyplot as plt
# config
from config.config import *
# misc
from analyze.visualization.plot_image import select_plot_t_step
import joblib
import glob
from numba import njit
from multiprocessing import Pool


def plot_kl(exp1_name, exp1_index, exp2_name, exp2_indexes, cut_circle_r=0):
    plotter = Plot_KL()
    plotter.set_up_conditions(exp1_name, exp1_index, exp2_name, exp2_indexes, cut_circle_r)
    plotter.start_parallel_processing()


class Plot_KL:
    def __init__(self):
        self.exp1_name = None
        self.exp2_name = None
        self.exp1_index = None
        self.exp2_indexes = None
        self.cut_circle_r = None

    def set_up_conditions(self, exp1_name, exp1_index, exp2_name, exp2_indexes, cut_circle_r):
        self.exp1_name = exp1_name
        self.exp2_name = exp2_name
        self.exp1_index = exp1_index
        self.exp2_indexes = exp2_indexes
        self.cut_circle_r = cut_circle_r

    def start_parallel_processing(self):
        # 並列処理させるために、各プロセスに渡す引数を生成する
        # 並列処理用の前処理
        arguments = []
        for exp2_index in self.exp2_indexes:
            arguments.append(
                [self.exp1_name, self.exp1_index, self.exp2_name, exp2_index, self.cut_circle_r])
        # 並列数
        p = Pool(ConfigSimulation.PlotParallelNum)
        # 並列処理開始
        p.map(Plot_KL.wrapper, arguments)
        print_finish("FINISH：KLダイバージェンス")
        # processをclose
        p.close()
        p.terminate()

    @staticmethod
    def wrapper(args):
        return Plot_KL.plot_image(*args)

    @staticmethod
    def plot_image(exp1_name, exp1_index, exp2_name, exp2_index, cut_circle_r):
        plotter = Main_KL_div()
        plotter.set_up(exp1_name, exp1_index, exp2_name, exp2_index, cut_circle_r)
        plotter.plot()


class Main_KL_div:
    def __init__(self):
        self.exp1_name = None
        self.exp2_name = None
        self.exp1_index = None
        self.exp2_index = None
        self.simulation_data_names_1 = None
        self.simulation_data_names_2 = None

        self.save_path_png = None
        self.save_path_csv = None
        self.save_path_csv_in_circle = None
        self.file_name = None
        self.file_name_only_in_circle = None

        self.KLdiv_list = None
        self.t_list = select_plot_t_step()
        self.title = None
        self.cut_circle_r = None

    def set_up(self, exp1_name, exp1_index, exp2_name, exp2_index, cut_circle_r):
        self.exp1_name = exp1_name
        self.exp2_name = exp2_name
        self.exp1_index = exp1_index
        self.exp2_index = str(exp2_index).zfill(4)

        self.simulation_data_names_1 = glob.glob(f"{config_simulation_data_save_path(exp1_name, exp1_index)}/*.jb")
        self.simulation_data_names_1.sort()  # 実験順にsortする。
        self.simulation_data_names_2 = glob.glob(f"{config_simulation_data_save_path(exp2_name, exp2_index)}/*.jb")
        self.simulation_data_names_2.sort()  # 実験順にsortする。

        print(f"exp_name_1のデータ数：{len(self.simulation_data_names_1)}")
        print(f"exp_name_2のデータ数：{len(self.simulation_data_names_2)}")

        self.cut_circle_r = cut_circle_r

        # title設定のために一つデータをロードする。
        condition = joblib.load(self.simulation_data_names_2[0])["実験条件データ（condition）"]
        folder_name = f'KL_{self.exp1_name}_{self.exp1_index}-{self.exp2_name}'
        if self.cut_circle_r != 0:  # 中心付近の確率分布をカットする場合は、保存フォルダ名にカットする半径rを加筆する
            folder_name = f'r={self.cut_circle_r}_' + folder_name
            # 中心付近の確率分布をカットしたKLダイバージェンスの保存先の設定
            self.save_path_csv_in_circle = config_KL_div_save_path(folder_name=folder_name, ext="csv_in_circle")

        # 保存先の設定
        # 通常のKLダイバージェンス
        self.save_path_png = config_KL_div_save_path(folder_name=folder_name, ext="png")
        self.save_path_csv = config_KL_div_save_path(folder_name=folder_name, ext="csv")

        # ファイル名を設定する
        self.file_name = folder_name + f"_{self.exp2_index}"
        self.file_name_only_in_circle = folder_name + "_InCircle_" + f"{self.exp2_index}"

        # プロットのタイトルを設定する
        self.title = f"{self.exp2_name}" + " " + "$t_{erase}$" + f"={condition.erase_t}"

    def plot(self):
        KLdiv_list = []
        KLdiv_in_circle_list = []
        for t_step in self.t_list:
            # t=t_stepのシミュレーションデータをロード
            p1 = get_probability(self.simulation_data_names_1, t_step)
            p2 = get_probability(self.simulation_data_names_2, t_step)

            KLdiv, kl_div_in_circle = get_kl_div(p1=p1, p2=p2, radius=self.cut_circle_r)
            if self.cut_circle_r != 0:
                KLdiv_in_circle_list.append(kl_div_in_circle)
            KLdiv_list.append(KLdiv)
            print(f"t={t_step}")

        if self.cut_circle_r != 0:
            self.save_csv_file(KLdiv_in_circle_list, self.save_path_csv_in_circle,
                               f"{self.file_name_only_in_circle}.csv")
        self.save_csv_file(KLdiv_list, self.save_path_csv, f"{self.file_name}.csv")

        # plotする
        do_plot_graph(f"{self.save_path_png}/{self.file_name}.png", KLdiv_list, self.t_list, self.title, xlabel="t",
                      ylabel="KL_div")

    def save_csv_file(self, KLdiv_list, folder_path, file_path):
        with open(f"{folder_path}/{file_path}", mode='w') as f:
            f.write(
                f"t,r={self.cut_circle_r}_{self.exp1_name}_{self.exp1_index}-{self.exp2_name}_{self.exp2_index}\n")
            for i in range(len(KLdiv_list)):
                s = f"{self.t_list[i]},{KLdiv_list[i]}\n"
                print(s)
                f.write(s)


def get_probability(simulation_data_file_names, index):
    save_data_object = joblib.load(simulation_data_file_names[index])
    condition = save_data_object["実験条件データ（condition）"]

    # エラーチェック
    if index != int(save_data_object["このシミュレーションデータが何ステップ目か（t）"]):
        print_warning("実験データをチェックしてください")

    T = condition.T
    len_x = 2 * T + 1
    len_y = 2 * T + 1
    PSY = save_data_object["シミュレーションデータ"]

    # probability[x,y]として(x,y)座標の確率を求められる。
    probability = calc_probability(PSY, len_x, len_y)
    return probability


@njit('Tuple((f8,f8))(f8[:,:],f8[:,:],i8)', cache=True)
def get_kl_div(p1, p2, radius):
    """
        概要
            量子ウォークの確率分布のKLダイバージェンスを求める。ただし中心が原点で直径が指定した値である円形領域では、KLダイバージェンスの値を0とする（領域内を無視する）
            また、その領域内のKLダイバージェンスを求める。
        引数
            p1,p2：大きさの等しい2次元リストp1[x,y]のように指定できること。
        返却値
            円形領域を無視した場合のKLダイバージェンスと、その円形領域のKLダイバージェンスを返却する
        """
    kl_div = 0  # 通常のKLダイバージェンス
    kl_div_cut = 0  # 中心付近の円形領域をカットした場合のKLダイバージェンス
    kl_div_in_circle = 0  # 中心付近の円形領域内のKL大ダイバージェンス

    len_x = p1.shape[1]
    len_y = p1.shape[0]
    T = len_x // 2
    for x in range(len_x):
        for y in range(len_y):
            if p2[x, y] == 0:
                continue
            if p1[x, y] == 0:
                continue
            # radiusが設定されていないなら、通常のKLダイバージェンスのみを求める
            if radius != 0:
                if (x - T) ** 2 + (y - T) ** 2 < radius ** 2:
                    # 円形内
                    kl_div_in_circle += p1[x, y] * np.log(p1[x, y] / p2[x, y])
                else:
                    # 円形外
                    kl_div += p1[x, y] * np.log(p1[x, y] / p2[x, y])
            else:
                # 全体
                kl_div += p1[x, y] * np.log(p1[x, y] / p2[x, y])
    print("in circle", kl_div_in_circle)  # デバッグ用
    return kl_div, kl_div_in_circle


def do_plot_graph(file_name, dates, t_list, title, xlabel, ylabel):
    fig = plt.figure(figsize=(4, 3), tight_layout=True, dpi=400)
    ax = fig.add_subplot(111, xlabel=xlabel, ylabel=ylabel)
    ax.set_title(title, size=24)
    ax.scatter(t_list, dates, c='blue')
    fig.savefig(file_name)
    print("FIN")
