import numpy as np
import matplotlib.pyplot as plt

from config.config import *
from multiprocessing import Pool
import glob

from helper import load_data_by_error_handling, return_simulation_data_file_names
from simulation.simulation_core import calc_probability

import seaborn as sns
import pandas as pd


def plot_image(conditions, save_path_indexes, **params):
    for i in range(len(conditions)):
        plotter = Plotter(exp_mame=conditions[i].exp_name, save_path_index=save_path_indexes[i], params=params)
        plotter.start_processing()


class Plotter:
    def __init__(self, exp_mame, save_path_index, params):
        self.__exp_name = exp_mame

        self.p = 0  # 何に使うんだっけ？

        self.__save_path_index = save_path_index
        self.__t_list = params["plot_t_list"]
        self.__is_enlarge = params["is_enlarge"]
        self.__plot_type = params["plot_type"]
        self.__parallel = params["parallel"]

        self.__not_plot_t_list = self.check_finished(plot_type=self.__plot_type)

    def start_processing(self):
        simulation_data_file_names = return_simulation_data_file_names(exp_name=self.__exp_name,
                                                                       exp_index=self.__save_path_index)
        if self.__parallel:
            self.__start_parallel_processing(simulation_data_file_names)
        else:
            self.__start_single_processing(simulation_data_file_names)

    def __start_single_processing(self, simulation_data_file_names):
        for t in self.__not_plot_t_list:
            self.plot_image(simulation_data_file_names[t], self.__plot_type, self.__is_enlarge)

    def __start_parallel_processing(self, simulation_data_file_names):
        arguments = []
        for t in self.__not_plot_t_list:
            arguments.append([simulation_data_file_names[t], self.__plot_type, self.__is_enlarge])
        with Pool(ConfigSimulation.PlotParallelNum) as p:
            p.starmap(func=Plotter.plot_image, iterable=arguments)
        print_finish(self.__plot_type)

    def check_finished(self, plot_type):
        """
        plotが完了しているかを確認し、plotできていないファイルのみplotする。
        """
        path = plot_save_path(self.__exp_name, plot_type, self.__save_path_index)

        plot_files = glob.glob(f"{path}/*")  # すでにプロットされたファイルの一覧
        plotted_t_list = []  # すでにプロットされたtの一覧
        for plot_file in plot_files:
            extract_t = int(plot_file[-8:-4])
            plotted_t_list.append(extract_t)

        # 共通しない要素のうち、まだプロットされていないものを取得
        not_plot_t_list = set(self.__t_list) - set(plotted_t_list)

        if not not_plot_t_list:
            print_green_text(f"exp_index={self.__save_path_index}：既に完了")
        else:
            print_warning(f"exp_index={self.__save_path_index}：完了していません")
        return not_plot_t_list

    @staticmethod
    def plot_image(simulation_data_file_name, plot_type, is_enlarge):
        plotter = MainPlotter()
        plotter.load_data(simulation_data_file_name, plot_type, is_enlarge)
        plotter.plot()


class MainPlotter:
    def __init__(self):
        self.plot_type = None
        self.simulation_data_file_name = None
        self.simulation_data = None
        self.T = None
        self.len_x = None
        self.len_y = None
        self.t = None
        self.PSY = None
        self.erase_t = None
        self.exp_name = None
        self.exp_index = None

        # plot処理で共通に使うもの
        self.phi_latex = None
        self.t_index = None
        self.title = None
        self.mesh_z = None
        self.file_name = None
        self.plot_save_path = None
        self.is_enlarge = None

    def load_data(self, simulation_data_file_name, plot_type, is_enlarge):
        self.plot_type = plot_type
        self.is_enlarge = is_enlarge
        # データをロード
        simulation_data = load_data_by_error_handling(simulation_data_file_name)
        # simulation_data = joblib.load(simulation_data_file_name)
        # ロードしたデータを展開
        condition = simulation_data["実験条件データ（condition）"]
        self.T = condition.T
        self.len_x = 2 * self.T + 1
        self.len_y = 2 * self.T + 1
        self.t = simulation_data["このシミュレーションデータが何ステップ目か（t）"]
        self.PSY = simulation_data["シミュレーションデータ"]
        self.erase_t = condition.erase_t
        self.exp_name = condition.exp_name
        self.exp_index = condition.exp_index

        # plot処理で共通に使うもの
        self.phi_latex = condition.phi_latex
        self.t_index = str(self.t).zfill(4)
        self.title = f"$t={self.t}$," + "$t_{erase}$" + f"={self.erase_t}"
        self.mesh_z = calc_probability(self.PSY, self.len_x, self.len_y)
        self.file_name = f"{self.t_index}.png"
        self.plot_save_path = plot_save_path(self.exp_name, self.plot_type, self.exp_index)

    def plot(self):
        if self.plot_type == "surface":
            self.__plot_surface()
        elif self.plot_type == "heatmap":
            self.__plot_heatmap()
        else:
            print_warning("正しいplot_typeを選んでください")
            return

    def __plot_surface(self):
        # t=0つまりプロット点が1点の時の3dplotにはバグがある。そのためパスする
        # https://stackoverflow.com/questions/65131880/matplotlib-projection-3d-levels-issue
        if self.is_enlarge and int(self.t) != 0:
            # 最大でもself.tしか量子ウォーカーは進めないので、-self.t~self.tまでの切り取る
            max_x = self.T - int(self.t)
            max_y = self.T - int(self.t)
            if max_x != 0:  # max_xやmax_yが0になるとスライスできないから
                self.mesh_z = self.mesh_z[max_y:-max_y, max_x:-max_x]
            # 格子点を作成
            t_int = int(self.t)
            mesh_x, mesh_y = np.meshgrid(np.linspace(-t_int, t_int, 2 * t_int + 1),
                                         np.linspace(-t_int, t_int, 2 * t_int + 1))

        else:
            # 格子点を作成
            mesh_x, mesh_y = np.meshgrid(np.linspace(-self.T, self.T, 2 * self.T + 1),
                                         np.linspace(-self.T, self.T, 2 * self.T + 1))
        do_plot_surface(mesh_x, mesh_y, self.mesh_z, self.plot_save_path, self.file_name, self.title)
        print(f"t={self.t_index}：可視化と保存：完了")

    def __plot_heatmap(self):
        # 最大でもself.tしか量子ウォーカーは進めないので、-self.t~self.tまでの切り取る
        if self.is_enlarge:
            max_x = self.T - int(self.t)
            max_y = self.T - int(self.t)
            if max_x != 0:  # max_xやmax_yが0になるとスライスできないから
                self.mesh_z = self.mesh_z[max_y:-max_y, max_x:-max_x]

        do_plot_heatmap(self.mesh_z, self.plot_save_path, self.file_name, self.title, self.is_enlarge)
        print(f"t={self.t_index}：可視化と保存：完了")


def do_plot_surface(mesh_x, mesh_y, mesh_z, path, file_name, title):
    fig = plt.figure(figsize=(4, 3), tight_layout=True, dpi=400)
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.set_xlabel("$x$", size=24, labelpad=10)
    ax.set_ylabel("$y$", size=24)
    ax.set_zlabel("$p$", size=24, labelpad=15)
    # 軸メモリの調整
    ax.tick_params(labelsize=12)
    # タイトルを設定
    ax.set_title(title, size=24)
    # 曲面を描画
    ax.plot_surface(mesh_x, mesh_y, mesh_z, cmap="summer")
    plt.savefig(f"{path}/{file_name}", dpi=400, bbox_inches='tight')
    # メモリ解放
    fig.clf()
    ax.cla()
    plt.close()


def do_plot_heatmap(prob_list, path, file_name, title, is_enlarge):
    """heatmapをプロットする"""
    # プロット用のデータフレームの作成
    x_len = prob_list.shape[0]
    if is_enlarge:
        x_len_max = prob_list.shape[0] // 2
    else:
        x_len_max = ConfigSimulation.MaxTimeStep
    """
    現在のprob_listは[x,y]で(x,y)座標の確率を取得できるリストとなっている。
    heatmapの仕様上、リストの左上はheatmapの左上に表示される。
    左から右へプラス、下から上へプラス、この方が良いだろう。
    そのためには、行列を反転させれば、良さそうだ。
    上下反転させる。
    """
    prob_list = np.flipud(prob_list).copy()  # メモリをシェアーすると、他の処理でprob_list使うとき、バグが発生しそうなので、（クラスで共有しているし）やめておく
    index = [str(x_len_max - k) for k in range(x_len)]
    columns = [str(k - x_len_max) for k in range(x_len)]
    df = pd.DataFrame(prob_list, index=index, columns=columns)

    # figureを作成しプロットする
    fig = plt.figure(figsize=(16, 12), tight_layout=True)
    ax = fig.add_subplot(1, 1, 1)
    img = sns.heatmap(df, square=True, cmap="gist_heat_r")
    # sns.heatmap(df, square=True, cmap="Blues")
    img.set_xlabel("$x$", fontsize=20)
    img.set_ylabel("$y$", fontsize=20)
    ax.set_title(title, size=24)
    plt.show()
    plt.savefig(f"{path}/{file_name}", dpi=800, bbox_inches='tight')
    # メモリ解放
    fig.clf()
    ax.cla()
    plt.close()


def check_plot_progress(exp_name, plot_exp_index, T):
    # plotがどこまで進んだかをチェックし途中から再開するために、
    # plotのindexのフォルダが既に存在しており、plot数が足りていたらそのplotはは既に終了しているとする。
    finished = False
    folder_path = plot_save_path(exp_name, plot_exp_index)
    file_list = glob.glob(f"{folder_path}/*")

    need_file_num = T + 1
    file_num = len(file_list)
    print(f"exp_index={plot_exp_index}のデータ数：{file_num}")
    print(f"必要なデータ数：{need_file_num}")

    if need_file_num == file_num:
        print_green_text(f"plot_exp_index={plot_exp_index}：既に完了")
        finished = True
    return finished


def select_plot_t_step():
    # どのデータ抽出するかを選択する
    t_list = None
    if ConfigSimulation.MaxTimeStep == 2000:
        t_list = list(range(0, 2020, 20))
    elif ConfigSimulation.MaxTimeStep == 600:
        t_list = list(range(0, 605, 5))
    elif ConfigSimulation.MaxTimeStep == 200:
        t_list = list(range(0, 205, 5))
    elif ConfigSimulation.MaxTimeStep == 100:
        t_list = list(range(0, 105, 5))
    return t_list


def select_plot_t_step_detail():
    # どのデータ抽出するかを選択する
    t_list = None
    if ConfigSimulation.MaxTimeStep == 2000:
        t_list = list(range(0, 2005, 5))
    elif ConfigSimulation.MaxTimeStep == 600:
        t_list = list(range(0, 605, 5))
    elif ConfigSimulation.MaxTimeStep == 200:
        t_list = list(range(0, 205, 5))
    elif ConfigSimulation.MaxTimeStep == 100:
        t_list = list(range(0, 105, 5))
    return t_list


def select_plot_t_step_by_100():
    # どのデータ抽出するかを選択する
    t_list = None
    if ConfigSimulation.MaxTimeStep == 2000:
        t_list = list(range(0, 2100, 100))
    elif ConfigSimulation.MaxTimeStep == 600:
        t_list = [100, 200, 300, 400, 500, 600]
    elif ConfigSimulation.MaxTimeStep == 200:
        t_list = list(range(0, 205, 5))
    elif ConfigSimulation.MaxTimeStep == 100:
        t_list = list(range(0, 105, 5))
    return t_list
