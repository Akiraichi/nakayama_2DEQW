# config
from config.config import *
# misc
from analyze.visualization.plot_image import select_plot_t_step
import joblib
import glob
from numba import njit
from multiprocessing import Pool
from analyze.visualization.plot_kl import get_probability


def plot_prob(exp_name, exp_indexes, cut_circle_r, circle_inner_r, circle_outer_r):
    plotter = PlotProb(exp_name, exp_indexes, cut_circle_r, circle_inner_r, circle_outer_r)
    plotter.start_processing(parallel=False)


class PlotProb:
    def __init__(self, exp_name, exp_indexes, cut_circle_r, circle_inner_r, circle_outer_r):
        self.exp_name = exp_name
        self.exp_indexes = exp_indexes
        self.cut_circle_r = cut_circle_r
        self.circle_inner_r = circle_inner_r
        self.circle_outer_r = circle_outer_r

    def __start_parallel_processing(self):
        # 並列処理させるために、各プロセスに渡す引数を生成する
        # 並列処理用の前処理
        arguments = []
        for exp_index in self.exp_indexes:
            arguments.append(
                [self.exp_name, exp_index, self.cut_circle_r, self.circle_inner_r, self.circle_outer_r])
        # 並列数
        p = Pool(ConfigSimulation.PlotParallelNum)
        # 並列処理開始
        p.map(PlotProb.wrapper, arguments)
        # processをclose
        p.close()
        p.terminate()

    def start_processing(self, parallel=False):
        if parallel:
            self.__start_parallel_processing()
        else:
            for i, exp_index in enumerate(self.exp_indexes):
                plotter = MainPlotProb(self.exp_name, exp_index, self.cut_circle_r, self.circle_inner_r,
                                       self.circle_outer_r)
                plotter.plot()
                print(i, "番目の処理")
        print_finish("確率計算")

    @staticmethod
    def wrapper(args):
        return PlotProb.plot_image(*args)

    @staticmethod
    def plot_image(exp_name, exp_index, cut_circle_r, circle_inner_r, circle_outer_r):
        plotter = MainPlotProb(exp_name, exp_index, cut_circle_r, circle_inner_r, circle_outer_r)
        plotter.plot()


class MainPlotProb:
    def __init__(self, exp_name, exp_index, cut_circle_r, circle_inner_r, circle_outer_r):
        self.exp_name = exp_name
        self.exp_index = str(exp_index).zfill(4)
        self.simulation_data_names = glob.glob(f"{config_simulation_data_save_path(exp_name, exp_index)}/*.jb")
        self.simulation_data_names.sort()  # 実験順にsortする。
        self.cut_circle_r = cut_circle_r
        self.circle_inner_r = circle_inner_r
        self.circle_outer_r = circle_outer_r
        self.t_list = select_plot_t_step()
        print(f"exp_nameのデータ数：{len(self.simulation_data_names)}")

        # title設定のために一つデータをロードする。
        condition = joblib.load(self.simulation_data_names[0])["実験条件データ（condition）"]

        folder_name = f'cut_r={self.cut_circle_r}_inner_r={self.circle_inner_r}_outer_r={self.circle_outer_r}_{self.exp_name}'

        # 保存先の設定
        self.save_path_csv = config_prob_save_path(folder_name=folder_name)
        # ファイル名を設定する
        self.file_name = folder_name + f"_{self.exp_index}"

        # プロットのタイトルを設定する
        self.title = f"{self.exp_name}" + " " + "$t_{erase}$" + f"={condition.erase_t}"

    def plot(self):
        p_in_circle_list = []
        p_out_circle_list = []
        p_circle_list = []
        for t_step in self.t_list:
            # t=t_stepのシミュレーションデータをロード
            p1 = get_probability(self.simulation_data_names, t_step)  # 全体の確率分布
            p_in_circle, p_out_circle, p_circle = get_prob(prob=p1, radius=self.cut_circle_r,
                                                           circle_inner_r=self.circle_inner_r,
                                                           circle_outer_r=self.circle_outer_r)
            p_in_circle_list.append(p_in_circle)
            p_out_circle_list.append(p_out_circle)
            p_circle_list.append(p_circle)
            print(f"t={t_step}")

        self.save_csv_file(p_in_circle_list, p_out_circle_list, p_circle_list, self.save_path_csv,
                           f"{self.file_name}.csv")

        # # plotする
        # do_plot_graph(f"{self.save_path_png}/{self.file_name}.png", KLdiv_list, self.t_list, self.title, xlabel="t",
        #               ylabel="KL_div")

    def save_csv_file(self, p_in_circle_list, p_out_circle_list, p_circle_list, folder_path, file_path):
        with open(f"{folder_path}/{file_path}", mode='w') as f:
            f.write(
                f"t,in_circle_{self.exp_index},out_circle_{self.exp_index},circle_{self.exp_index}\n")
            for i in range(len(p_in_circle_list)):
                s = f"{self.t_list[i]},{p_in_circle_list[i]},{p_out_circle_list[i]},{p_circle_list[i]}\n"
                # print(s)　# デバッグ
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