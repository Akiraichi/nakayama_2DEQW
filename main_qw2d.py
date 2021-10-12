# config
from config.config import Config_simulation, print_warning
# exp_setting
from exp_setting.exp import *
# simulation
from simulation.simulation import start_simulation_2dqw
# plot
from analyze.visualization.plot_image import *
from analyze.visualization.plot_kl import execute_plot_kl_div, parallel_execute_plot_kl_div
from analyze.visualization.plot_var import execute_plot_var

# gif
from analyze.visualization.make_gif import make_gif_image, make_gif_surface_by_phase, make_gif_heatmap_by_phase


#
# def erase_eqw_simulation():
#     # 電場を消し去る場合のシミュレーション
#     # select_exp_index_list = list(range(10, 21))
#     select_exp_index_list = [3]
#     # erase_tステップ目から電場を消し去る
#     erase_t = 100
#     print(select_exp_index_list)
#     selected_conditions, exp_name = exp_017(exp_index_list=select_exp_index_list, erase_t=erase_t)
#     execute_simulation(exact_condition_list=selected_conditions)
#
#     plot_all(select_exp_index_list=select_exp_index_list, exp_name=exp_name)
#
#
# def eqw_simulation():
#     # 電場を消し去らない場合のシミュレーション
#     select_exp_index_list = [3]
#     print(select_exp_index_list)
#     selected_conditions, exp_name = exp_016_01_00_x_set(exp_index_list=select_exp_index_list)
#     execute_simulation(exact_condition_list=selected_conditions)
#     plot_all(select_exp_index_list=select_exp_index_list, exp_name=exp_name)


# def plot_all(select_exp_index_list, exp_name):
#     # plotしたいexp_nameのexp_indexを指定する
#     select_plot_exp_index = select_exp_index_list
#     execute_plot_surface(exp_name=exp_name, plot_exp_index_list=select_plot_exp_index)
#     make_gif_surface(exp_name=exp_name, plot_exp_index_list=select_plot_exp_index)
#
#     execute_plot_surface_by_phase(exp_name=exp_name, plot_t_step=100)
#     make_gif_surface_by_phase(exp_name=exp_name, plot_t_step=100)
#
#     execute_plot_heatmap_by_phase(exp_name=exp_name, plot_t_step=100)
#     make_gif_heatmap_by_phase(exp_name=exp_name, plot_t_step=100)

class Normal_qw:
    """
    通常の量子ウォーク
    """

    def __init__(self):
        if Config_simulation.max_time_step == 600 or Config_simulation.max_time_step == 100:
            self.selected_conditions, self.exp_name = exp_018()
        elif Config_simulation.max_time_step == 2000:
            self.selected_conditions, self.exp_name = exp_022()
        else:
            print_warning("Config_simulation.max_time_stepを確認してください")
            return

    def run_simulation(self):
        start_simulation_2dqw(exp_conditions=self.selected_conditions)

    def run_plot_surface(self):
        plot_image(exp_name=self.exp_name, plot_type="surface")

    def run_plot_heatmap(self):
        plot_image(exp_name=self.exp_name, plot_type="heatmap")

    def run_gif_surface(self):
        make_gif_image(exp_name=self.exp_name, plot_type="surface")

    def run_gif_heatmap(self):
        make_gif_image(exp_name=self.exp_name, plot_type="heatmap")

    def run_kl_div(self):
        pass


class Erase_EQW:
    """
    電場量子ウォーク
    pi/60
    """
    def __init__(self, select_exp_indexes):
        self.selected_exp_indexes = select_exp_indexes
        if Config_simulation.max_time_step == 600 or Config_simulation.max_time_step == 100:
            self.selected_conditions, self.exp_name = exp_019(exp_index_list=select_exp_indexes)
        elif Config_simulation.max_time_step == 2000:
            self.selected_conditions, self.exp_name = exp_021(exp_index_list=select_exp_indexes)
        else:
            print_warning("Config_simulation.max_time_stepを確認してください")
            return

    def run_simulation(self):
        start_simulation_2dqw(exp_conditions=self.selected_conditions)

    def run_plot_surface(self):
        plot_image(exp_name=self.exp_name, plot_type="surface", plot_exp_indexes=self.selected_exp_indexes)

    def run_plot_heatmap(self):
        plot_image(exp_name=self.exp_name, plot_type="heatmap", plot_exp_indexes=self.selected_exp_indexes)

    def run_gif_surface(self):
        make_gif_image(exp_name=self.exp_name, plot_type="surface", plot_exp_indexes=self.selected_exp_indexes)

    def run_gif_heatmap(self):
        make_gif_image(exp_name=self.exp_name, plot_type="heatmap", plot_exp_indexes=self.selected_exp_indexes)

    def run_kl_div(self):
        pass


# plot_image(exp_name=exp_name, plot_type="surface")
# make_gif_image(exp_name=exp_name, plot_type="heatmap")
# plot_image_only_t(exp_name=exp_name, plot_t_step=100, plot_type="heatmap")

# execute_plot_heatmap_by_phase(exp_name=exp_name, plot_t_step=100)
# make_gif_heatmap_by_phase(exp_name=exp_name, plot_t_step=100)
# execute_plot_var(exp_name=exp_name, plot_exp_index_list=select_plot_exp_index)


#
# def e1(select_exp_index_list, continue_t):
#     """
#     このerase_t_listでのexp_019のまとめ実行
#     つまりpi/60の電場をかけた電場量子ウォークの電場を途中で消し去った場合
#     """
#     selected_conditions, exp_name = exp_019(exp_index_list=select_exp_index_list)
#     execute_simulation(exact_condition_list=selected_conditions, continue_t=continue_t)
#
#     execute_plot_surface(exp_name=exp_name, plot_exp_index_list=select_exp_index_list)
#     make_gif_surface(exp_name=exp_name, plot_exp_index_list=select_exp_index_list)
#
#     # plot_t_step = 100
#     # execute_plot_heatmap_by_phase(exp_name=exp_name, exp_index_list=[10, 20, 30], plot_t_step=plot_t_step)
#     # make_gif_heatmap_by_phase(exp_name=exp_name, plot_t_step=plot_t_step)
#
#     # execute_plot_heatmap_by_phase(exp_name=exp_name, plot_t_step=600)
#     # make_gif_heatmap_by_phase(exp_name=exp_name, plot_t_step=600)
#     # execute_plot_var(exp_name=exp_name, plot_exp_index_list=select_plot_exp_index)
#
#
# def e2():
#     """
#     このerase_t_listでのexp_016_01_00_x_setのまとめ実行。
#     つまりpi/60の電場をかけて電場量子ウォーク
#     """
#     # 電場ありのシミュレーション
#     select_exp_index_list = [3]
#     selected_conditions, exp_name = exp_016_01_00_x_set(exp_index_list=select_exp_index_list)
#     execute_simulation(exact_condition_list=selected_conditions)
#
#     # plotしたいexp_nameのexp_indexを指定する
#     select_plot_exp_index = select_exp_index_list
#     execute_plot_surface(exp_name=exp_name, plot_exp_index_list=select_plot_exp_index)
#     make_gif_surface(exp_name=exp_name, plot_exp_index_list=select_plot_exp_index)
#
#     # execute_plot_surface_by_phase(exp_name=exp_name, plot_t_step=200)
#     # make_gif_surface_by_phase(exp_name=exp_name, plot_t_step=100)
#
#     # execute_plot_heatmap_by_phase(exp_name=exp_name, plot_t_step=100)
#     # make_gif_heatmap_by_phase(exp_name=exp_name, plot_t_step=100)
#
#
# def e3(select_exp_index_list):
#     """
#     KLダイバージェンスを求める。
#     電場のない量子ウォークと電場を途中で消した場合とのKLダイバージェンス
#     :return:
#     """
#     exp_index_1 = 0
#     selected_conditions_1, exp_name_1 = exp_018()
#     selected_conditions_2, exp_name_2 = exp_019(exp_index_list=select_exp_index_list)
#
#     parallel_execute_plot_kl_div(exp_name_1, exp_index_1, exp_name_2, exp_index_2_list=select_exp_index_list)
#
#
# def e4():
#     """
#     KLダイバージェンスを求める。
#     電場のない量子ウォークと電場のある量子ウォークとのKLダイバージェンス
#     :return:
#     """
#     exp_index_1 = 0
#     selected_conditions_1, exp_name_1 = exp_018()
#
#     select_exp_index_list = [3]
#     exp_index_2 = 3
#     selected_conditions, exp_name_2 = exp_016_01_00_x_set(exp_index_list=select_exp_index_list)
#
#     execute_plot_kl_div(exp_name_1=exp_name_1, exp_index_1=exp_index_1, exp_name_2=exp_name_2,
#                         exp_index_2=exp_index_2)


#
# def e1_1000step(select_exp_index_list):
#     selected_conditions, exp_name = exp_020(exp_index_list=select_exp_index_list)
#     execute_simulation(exact_condition_list=selected_conditions)
#
#
# def e1_2000step(select_exp_index_list, continue_t):
#     selected_conditions, exp_name = exp_021(exp_index_list=select_exp_index_list)
#     execute_simulation(exact_condition_list=selected_conditions, continue_t=continue_t)

#
# def e3_2000step(select_exp_index_list):
#     """
#     KLダイバージェンスを求める。
#     電場のない量子ウォークと電場を途中で消した場合とのKLダイバージェンス
#     :return:
#     """
#     exp_index_1 = 0
#     selected_conditions_1, exp_name_1 = exp_022()
#     selected_conditions_2, exp_name_2 = exp_021(exp_index_list=select_exp_index_list)
#
#     parallel_execute_plot_kl_div(exp_name_1, exp_index_1, exp_name_2, exp_index_2_list=select_exp_index_list)
#

# def all_heat_map_plot(exp_name, exp_index_list, plot_t_step_list):
#     """
#     exp_index_listの中のexp_index全てについて、plot_t_step_listで指定したplot_t_step全てについてheatmapを作成する
#     """
#     for plot_t_step in plot_t_step_list:
#         execute_plot_heatmap_by_phase(exp_name=exp_name, exp_index_list=exp_index_list, plot_t_step=plot_t_step)
#         make_gif_heatmap_by_phase(exp_name=exp_name, plot_t_step=plot_t_step)


if __name__ == '__main__':
    qw = Erase_EQW(select_exp_indexes=[10, 20])
    qw.run_simulation()
    qw.run_plot_surface()
    qw.run_gif_surface()
    qw.run_plot_heatmap()
    qw.run_gif_heatmap()
    qw.run_kl_div()
