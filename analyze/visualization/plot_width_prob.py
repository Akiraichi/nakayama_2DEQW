from analyze.visualization.plot_image import select_plot_t_step, select_plot_t_step_detail
from analyze.visualization.analyzer import do_plot_graph
from config.config import *
import joblib
import glob
from simulation.simulation_core import calc_probability


def plot_width_prob(exp_name, plot_exp_indexes=None):
    if plot_exp_indexes is None:
        plot_exp_indexes = [0]
    for plot_exp_index in plot_exp_indexes:
        plotter = WidthPlotter()
        plotter.set_up_conditions(exp_name=exp_name, plot_exp_index=plot_exp_index)
        plotter.start_processing()


class WidthPlotter:
    def __init__(self):
        self.exp_name = None
        self.plot_exp_index = None
        self.x_widths = []
        self.y_widths = []
        self.t_list = select_plot_t_step_detail()

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
        # self.file_name = None
        self.plot_save_path_x = None
        self.plot_save_path_y = None

    def set_up_conditions(self, exp_name, plot_exp_index):
        self.exp_name = exp_name
        self.plot_exp_index = plot_exp_index

    def start_processing(self):
        simulation_data_file_names = glob.glob(
            f"{config_simulation_data_save_path(self.exp_name, self.plot_exp_index)}/*.jb")
        simulation_data_file_names.sort()  # 実験順にsortする。

        for t in self.t_list:
            self.load_data(simulation_data_file_names[t])
            x_width, y_width = get_width(self.mesh_z, self.len_x, self.len_y)
            self.x_widths.append(x_width)
            self.y_widths.append(y_width)
        self.plot_image()

    def load_data(self, simulation_data_file_name):
        # データをロード
        simulation_data = joblib.load(simulation_data_file_name)
        # ロードしたデータを展開
        condition = simulation_data["実験条件データ（condition）"]
        self.T = condition.T
        self.len_x = 2 * self.T + 1
        self.len_y = 2 * self.T + 1
        self.t = simulation_data["このシミュレーションデータが何ステップ目か（t）"]
        self.PSY = simulation_data["シミュレーションデータ"]
        self.erase_t = condition.erase_t
        self.exp_index = condition.exp_index

        # plot処理で共通に使うもの
        self.phi_latex = condition.phi_latex
        self.t_index = str(self.t).zfill(4)
        self.title = f"{self.exp_name}-{self.exp_index}"
        self.mesh_z = calc_probability(self.PSY, self.len_x, self.len_y)
        self.plot_save_path_x = f"{config_prob_width_save_path()}/X_width_{self.exp_name}-{self.exp_index}.png"
        self.plot_save_path_y = f"{config_prob_width_save_path()}/Y_width_{self.exp_name}-{self.exp_index}.png"
        # self.plot_save_path = plot_save_path(self.exp_name, self.plot_type, self.exp_index)

    def plot_image(self):
        do_plot_graph(self.plot_save_path_x, self.x_widths, self.t_list, self.title, xlabel="t", ylabel="width")
        do_plot_graph(self.plot_save_path_y, self.y_widths, self.t_list, self.title, xlabel="t", ylabel="width")


def get_width(mesh_z, len_x, len_y):
    """x、y軸それぞれにおいて、確率分布の最大位置と最小位置の差を求める。"""
    threshold = 0.00000001  # 閾値
    x_max = 0
    x_min = 0
    y_max = 0
    y_min = 0

    # 初期値として見つかった値を一つ代入しておく
    for x in range(len_x):
        for y in range(len_y):
            if mesh_z[x, y] > threshold:
                x_max = x
                x_min = x
                y_max = y
                y_min = y
                break
        else:
            continue
        break

    for x in range(len_x):
        for y in range(len_y):
            if mesh_z[x, y] > threshold:
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y

    return x_max - x_min, y_max - y_min
