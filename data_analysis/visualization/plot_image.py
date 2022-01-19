from concurrent.futures import ProcessPoolExecutor

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from numba import njit
import joblib

from config.config_visualization import plot_save_path, DefaultPlotSetting, Plot3dSetting
from config.config_simulation import ConfigSimulationSetting, Env
from helper import helper
from simulation.simulation_algorithm import calc_probability

# 3次元プロット用
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors


@njit('Tuple((i8[:],i8[:],i8[:],f8[:]))(i8,i8,i8[:],f8[:,:,:])', cache=True)
def return_x_y_z_v_set_for_3d_plot(len_x, len_y, not_plot_t_list, p_list):
    index_count = 0
    len_list = len_x * len_y * len(not_plot_t_list)
    x_list = np.zeros(len_list, dtype=np.int64)
    y_list = np.zeros(len_list, dtype=np.int64)
    z_list = np.zeros(len_list, dtype=np.int64)
    value_list = np.zeros(len_list, dtype=np.float64)

    for i, t_index in enumerate(not_plot_t_list):
        for x in range(len_x):
            print("x=,", x, ",i=", i)
            for y in range(len_y):
                if round(p_list[i][x, y], 4) == 0.0:
                    continue
                x_list[index_count] = x
                y_list[index_count] = y
                z_list[index_count] = t_index
                value_list[index_count] = p_list[i][x, y]
                index_count += 1
    return x_list, y_list, z_list, value_list


def plot_image(_setting: DefaultPlotSetting):
    for i in range(len(_setting.conditions)):
        exp_name = _setting.conditions[i].exp_name
        save_path_index = _setting.save_path_indexes[i]

        plotter = Plotter(exp_mame=exp_name, save_path_index=save_path_index, setting=_setting)
        plotter.start_processing()
        helper.print_finish(f"exp_index={_setting.conditions[i].exp_index} {_setting.plot_type}")


def plot_image_group(_setting: DefaultPlotSetting):
    for i in range(len(_setting.conditions)):
        exp_name = _setting.conditions[i].exp_name
        save_path_index = _setting.save_path_indexes[i]

        simulation_data_file_names = helper.return_simulation_data_file_names(exp_name=exp_name,
                                                                              exp_index=save_path_index)
        plotter = MainPlotter(simulation_data_file_name=simulation_data_file_names[_setting.plot_t_list[i]],
                              exp_name=exp_name,
                              exp_index=save_path_index, plot_type=_setting.plot_type, is_enlarge=_setting.is_enlarge,
                              _save_path=plot_save_path(exp_name, _setting.plot_type, is_group=True))
        plotter.plot()
        helper.print_finish(f"exp_index={_setting.conditions[i].exp_index} {_setting.plot_type}")


def plot_3d_image(_setting: Plot3dSetting):
    # データが存在するかを確認。なければ作成し、プロットする
    data_dict = {}
    if _setting.z_axis == "t":
        for index in _setting.plot_index_list:
            while True:
                try:
                    data_dict = joblib.load(f"{_setting.path_to_file}/{_setting.file_name(index=index)}.jb")
                except FileNotFoundError as e:
                    print(e)
                    # ファイルがないので作成する
                    create_3d_image_data_cmp_t(_setting, index)
                else:
                    break
    elif _setting.z_axis == "i":
        for index in _setting.plot_t_list:
            while True:
                try:
                    data_dict = joblib.load(f"{_setting.path_to_file}/{_setting.file_name(index=index)}.jb")
                except FileNotFoundError as e:
                    print(e)
                    # ファイルがないので作成する
                    create_3d_image_data_cmp_i(_setting, index)
                else:
                    break
    else:
        helper.print_warning("z_axisの設定を間違えています")
        raise OSError

    if Env.ENV == "local":
        df_dict = {"x": data_dict["x_list"],
                   "y": data_dict["y_list"],
                   "z": data_dict["z_list"],
                   "v": data_dict["value_list"]}
        df = pd.DataFrame(df_dict)
        do_plot_3d_image_new(df)


def create_3d_image_data_cmp_t(_setting: Plot3dSetting, index):
    simulation_data_file_names = helper.return_simulation_data_file_names(exp_name=_setting.conditions[0].exp_name,
                                                                          exp_index=_setting.plot_index_list[0])
    # STEP(1.5)：後でlen_x,len_yを計算するために代表して0番のデータをロードする
    _simulation_data = helper.load_file_by_error_handling(simulation_data_file_names[0])
    _condition = _simulation_data["実験条件データ（condition）"]

    # STEP(2)：確率データを得る。そしてリストへappend
    p_list = []
    for _, t in enumerate(_setting.plot_t_list):
        simulation_data = helper.load_file_by_error_handling(simulation_data_file_names[t])
        condition = simulation_data["実験条件データ（condition）"]
        PSY = simulation_data["シミュレーションデータ"]
        p = calc_probability(PSY, calc_len_x(condition.T), calc_len_y(condition.T))
        p_list.append(p)
    # STEP(3)：データを加工する。プロット用のデータに変える
    x_list, y_list, z_list, value_list = return_x_y_z_v_set_for_3d_plot(calc_len_x(_condition.T),
                                                                        calc_len_y(_condition.T),
                                                                        np.array(_setting.plot_t_list),
                                                                        np.array(p_list))
    image_data_save(x_list, y_list, z_list, value_list, _setting, index)


def create_3d_image_data_cmp_i(_setting: Plot3dSetting, index):
    # STEP(2)：確率データを得る。そしてリストへappend
    p_list = []
    for i, exp_index in enumerate(_setting.plot_index_list):
        # STEP(1)：シミュレーションデータへのパスを得る
        simulation_data_file_names = helper.return_simulation_data_file_names(exp_name=_setting.conditions[i].exp_name,
                                                                              exp_index=exp_index)
        # データをロード
        simulation_data = helper.load_file_by_error_handling(simulation_data_file_names[_setting.plot_t_list[0]])
        condition = simulation_data["実験条件データ（condition）"]
        PSY = simulation_data["シミュレーションデータ"]
        # 確率を計算してappend
        p = calc_probability(PSY, calc_len_x(condition.T), calc_len_y(condition.T))
        p_list.append(p)

    # STEP(3)：データを加工する。プロット用のデータに変える
    x_list, y_list, z_list, value_list = return_x_y_z_v_set_for_3d_plot(calc_len_x(condition.T),
                                                                        calc_len_y(condition.T),
                                                                        np.array(_setting.plot_index_list),
                                                                        np.array(p_list))
    image_data_save(x_list, y_list, z_list, value_list, _setting, index)


def image_data_save(x_list, y_list, z_list, value_list, _setting: Plot3dSetting, index):
    # STEP(3)：データを保存する。プロットはローカルで行うため。
    data_dict = {
        "x_list": x_list,
        "y_list": y_list,
        "z_list": z_list,
        "value_list": value_list,
        "file_name": _setting.file_name,
        "path_to_file": _setting.path_to_file
    }
    helper.save_jb_file(data_dict, _setting.path_to_file, f"{_setting.file_name(index=index)}.jb")


def calc_len_x(_T):
    """2次元格子の長さを返す。正方形なのでx方向もy方向も同じ"""
    return 2 * _T + 1


def calc_len_y(_T):
    """2次元格子の長さを返す。正方形なのでx方向もy方向も同じ"""
    return 2 * _T + 1


def do_plot_3d_image(x_list, y_list, z_list, value_list, file_name, path_to_file):
    # step(3)：プロットする
    # creating figures
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # setting color bar
    color_map = cm.ScalarMappable(cmap=cm.gist_heat_r)
    color_map.set_array(value_list)

    # creating the heatmap
    ax.scatter(x_list, y_list, z_list, cmap="gist_heat_r", c=value_list, s=1)
    plt.colorbar(color_map)

    # adding title and labels
    ax.set_title("3D Heatmap")
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    plt.show()


def do_plot_3d_image_new(df):
    import plotly.express as px
    fig = px.scatter_3d(df, x='x', y='y', z='z',
                        color='v', symbol='z', color_continuous_scale='hot_r',opacity=0.7)
    fig.show()


class Plotter:
    def __init__(self, exp_mame, save_path_index, setting: DefaultPlotSetting):
        self.p = 0  # 何に使うんだっけ？
        self.__exp_name = exp_mame
        self.__save_path_index = save_path_index
        self.__setting = setting
        self.__not_plot_t_list = helper.check_finished_file(
            folder_path=plot_save_path(self.__exp_name, self.__setting.plot_type, self.__save_path_index),
            will_generate_index_list=self.__setting.plot_t_list, extension="png")

    def start_processing(self):
        simulation_data_file_names = helper.return_simulation_data_file_names(exp_name=self.__exp_name,
                                                                              exp_index=self.__save_path_index)
        if self.__setting.parallel:
            self.__start_parallel_processing(simulation_data_file_names)
        else:
            self.__start_single_processing(simulation_data_file_names)

    def __start_single_processing(self, simulation_data_file_names):
        for t in self.__not_plot_t_list:
            self.plot_image(simulation_data_file_names[t], self.__setting.plot_type, self.__setting.is_enlarge,
                            self.__exp_name, self.__save_path_index)

    def __start_parallel_processing(self, simulation_data_file_names):
        with ProcessPoolExecutor(max_workers=ConfigSimulationSetting.PlotParallelNum) as e:
            for t in self.__not_plot_t_list:
                e.submit(Plotter.plot_image, simulation_data_file_names[t], self.__setting.plot_type,
                         self.__setting.is_enlarge, self.__exp_name, self.__save_path_index)

    @staticmethod
    def plot_image(simulation_data_file_name, plot_type, is_enlarge, exp_name, exp_index):
        plotter = MainPlotter(simulation_data_file_name=simulation_data_file_name, exp_name=exp_name,
                              exp_index=exp_index, plot_type=plot_type, is_enlarge=is_enlarge)
        plotter.plot()


class MainPlotter:
    def __init__(self, simulation_data_file_name, exp_name, exp_index, plot_type, is_enlarge, _save_path=None):
        self.__plot_type = plot_type
        simulation_data = helper.load_file_by_error_handling(simulation_data_file_name)
        condition = simulation_data["実験条件データ（condition）"]
        self.__T = condition.T

        self.__t = simulation_data["このシミュレーションデータが何ステップ目か（t）"]
        self.__title = f"$t={self.__t}$," + "$t_{erase}$" + f"={condition.erase_t}"
        self.__t_index = str(self.__t).zfill(4)
        len_x = 2 * self.__T + 1
        len_y = 2 * self.__T + 1
        PSY = simulation_data["シミュレーションデータ"]
        self.__mesh_z = calc_probability(PSY, len_x, len_y)
        if _save_path is None:
            self.__file_name = f"{self.__t_index}"
            self.__plot_save_path = plot_save_path(exp_name, self.__plot_type, exp_index)
        else:
            self.__file_name = f"{exp_index}_{self.__t_index}"
            self.__plot_save_path = _save_path
        self.__is_enlarge = is_enlarge

    def plot(self):
        if self.__plot_type == "surface":
            self.__plot_surface()
        elif self.__plot_type == "heatmap":
            self.__plot_heatmap()
        else:
            helper.print_warning("正しいplot_typeを選んでください")
            return

    def __plot_surface(self):
        # t=0つまりプロット点が1点の時の3dplotにはバグがある。そのためパスする
        # https://stackoverflow.com/questions/65131880/matplotlib-projection-3d-levels-issue
        if self.__is_enlarge and int(self.__t) != 0:
            # 最大でもself.tしか量子ウォーカーは進めないので、-self.t~self.tまでの切り取る
            max_x = self.__T - int(self.__t)
            max_y = self.__T - int(self.__t)
            if max_x != 0:  # max_xやmax_yが0になるとスライスできないから
                self.__mesh_z = self.__mesh_z[max_y:-max_y, max_x:-max_x]
            # 格子点を作成
            t_int = int(self.__t)
            mesh_x, mesh_y = np.meshgrid(np.linspace(-t_int, t_int, 2 * t_int + 1),
                                         np.linspace(-t_int, t_int, 2 * t_int + 1))

        else:
            # 格子点を作成
            mesh_x, mesh_y = np.meshgrid(np.linspace(-self.__T, self.__T, 2 * self.__T + 1),
                                         np.linspace(-self.__T, self.__T, 2 * self.__T + 1))
        do_plot_surface(mesh_x, mesh_y, self.__mesh_z, self.__plot_save_path, self.__file_name, self.__title)
        print(f"t={self.__t_index}：可視化と保存：完了")

    def __plot_heatmap(self):
        # 最大でもself.tしか量子ウォーカーは進めないので、-self.t~self.tまでの切り取る
        if self.__is_enlarge:
            max_x = self.__T - int(self.__t)
            max_y = self.__T - int(self.__t)
            if max_x != 0:  # max_xやmax_yが0になるとスライスできないから
                self.__mesh_z = self.__mesh_z[max_y:-max_y, max_x:-max_x]

        do_plot_heatmap(self.__mesh_z, self.__plot_save_path, self.__file_name, self.__title, self.__is_enlarge)
        print(f"t={self.__t_index}：可視化と保存：完了")


def do_plot_surface(mesh_x, mesh_y, mesh_z, path, file_name, title):
    fig = plt.figure(figsize=(4, 3), tight_layout=True, dpi=800)
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
    helper.Google_Drive_OS_error_wrapper(plt.savefig, f"{path}/{file_name}", dpi=800, bbox_inches='tight')
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
        x_len_max = ConfigSimulationSetting.MaxTimeStep
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
    helper.Google_Drive_OS_error_wrapper(plt.savefig, f"{path}/{file_name}", dpi=800, bbox_inches='tight')
    # メモリ解放
    fig.clf()
    ax.cla()
    plt.close()
