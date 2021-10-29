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


def plot_kl(exp1_name, exp1_index, exp2_name, exp2_indexes):
    plotter = Plot_KL()
    plotter.set_up_conditions(exp1_name, exp1_index, exp2_name, exp2_indexes)
    plotter.start_parallel_processing()


class Plot_KL:
    def __init__(self):
        self.exp1_name = None
        self.exp2_name = None
        self.exp1_index = None
        self.exp2_indexes = None

    def set_up_conditions(self, exp1_name, exp1_index, exp2_name, exp2_indexes):
        self.exp1_name = exp1_name
        self.exp2_name = exp2_name
        self.exp1_index = exp1_index
        self.exp2_indexes = exp2_indexes

    def start_parallel_processing(self):
        # 並列処理させるために、各プロセスに渡す引数を生成する
        # 並列処理用の前処理
        arguments = []
        for exp2_index in self.exp2_indexes:
            arguments.append(
                [self.exp1_name, self.exp1_index, self.exp2_name, exp2_index])
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
    def plot_image(exp1_name, exp1_index, exp2_name, exp2_index):
        plotter = Main_KL_div()
        plotter.set_up(exp1_name, exp1_index, exp2_name, exp2_index)
        plotter.plot()


class Main_KL_div:
    def __init__(self):
        self.exp1_name = None
        self.exp2_name = None
        self.exp1_index = None
        self.exp2_index = None
        self.simulation_data_names_1 = None
        self.simulation_data_names_2 = None
        self.save_path = None
        self.KLdiv_list = None
        self.t_list = select_plot_t_step()
        self.title = None

    def set_up(self, exp1_name, exp1_index, exp2_name, exp2_index):
        self.exp1_name = exp1_name
        self.exp2_name = exp2_name
        self.exp1_index = exp1_index
        self.exp2_index = exp2_index

        self.simulation_data_names_1 = glob.glob(f"{config_simulation_data_save_path(exp1_name, exp1_index)}/*.jb")
        self.simulation_data_names_1.sort()  # 実験順にsortする。
        self.simulation_data_names_2 = glob.glob(f"{config_simulation_data_save_path(exp2_name, exp2_index)}/*.jb")
        self.simulation_data_names_2.sort()  # 実験順にsortする。

        print(f"exp_name_1のデータ数：{len(self.simulation_data_names_1)}")
        print(f"exp_name_2のデータ数：{len(self.simulation_data_names_2)}")

        # plot関係
        self.save_path = f'{config_KL_div_save_path()}/KL_{exp1_name}_index{exp1_index}-{exp2_name}_index{exp2_index}.png'

        # title設定のために一つデータをロードする。
        condition = joblib.load(self.simulation_data_names_2[0])["実験条件データ（condition）"]
        self.title = f"{self.exp2_name}" + " " + "$t_{erase}$" + f"={condition.erase_t}"

    def plot(self):
        KLdiv_list = []
        for t_step in self.t_list:
            # t=t_stepのシミュレーションデータをロード
            p1 = get_probability(self.simulation_data_names_1, t_step)
            p2 = get_probability(self.simulation_data_names_2, t_step)
            KLdiv = get_kl_div(p1=p1, p2=p2)
            KLdiv_list.append(KLdiv)
            print(f"t={t_step}")
        do_plot_graph(self.save_path, KLdiv_list, self.t_list, self.title, xlabel="t", ylabel="KL_div")


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


@njit('f8(f8[:,:],f8[:,:])', cache=True)
def get_kl_div(p1, p2):
    """
        概要
            量子ウォークの確率分布のKLダイバージェンスを求める
        処理の流れ
            （1）二つのprobabilityを引数から受け取る。その二つの確率分布のKLダイバージェンスを返却する
        引数
            p1,p2：大きさの等しい2次元リストp1[x,y]のように指定できること。
        """
    kl_div = 0
    # 属性shapeで形状（行数、列数）が取得可能。
    len_x = p1.shape[1]
    len_y = p1.shape[0]
    for x in range(len_x):
        for y in range(len_y):
            if p2[x, y] == 0:
                continue
            if p1[x, y] == 0:
                continue
            kl_div += p1[x, y] * np.log(p1[x, y] / p2[x, y])

    return kl_div


def do_plot_graph(file_name, dates, t_list, title, xlabel, ylabel):
    fig = plt.figure(figsize=(4, 3), tight_layout=True, dpi=400)
    ax = fig.add_subplot(111, xlabel=xlabel, ylabel=ylabel)
    ax.set_title(title, size=24)
    ax.scatter(t_list, dates, c='blue')
    fig.savefig(file_name)
    print("FIN")
