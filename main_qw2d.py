# config
from analyze.visualization.plot_kl import plot_kl
# exp_setting
from exp_setting.exp import *
# simulation
from simulation.simulation import start_simulation_2dqw
# plot
from analyze.visualization.plot_image import *
# gif
from analyze.visualization.make_gif import make_gif_image


class Normal_qw:
    """
    通常の量子ウォーク
    """

    def __init__(self):
        self.index = 0
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

    def run_kl_div(self, qw_obj):
        plot_kl(exp1_name=self.exp_name, exp1_index=self.index, exp2_name=qw_obj.exp_name,
                exp2_indexes=qw_obj.selected_exp_indexes)


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

    def run_gif_surface(self, plot_t_step=None):
        make_gif_image(exp_name=self.exp_name, plot_type="surface", plot_exp_indexes=self.selected_exp_indexes,
                       plot_t_step=plot_t_step)

    def run_gif_heatmap(self, plot_t_step=None):
        make_gif_image(exp_name=self.exp_name, plot_type="heatmap", plot_exp_indexes=self.selected_exp_indexes,
                       plot_t_step=plot_t_step)


if __name__ == '__main__':
    qw = Normal_qw()
    # qw.run_simulation()
    # qw.run_plot_surface()
    # qw.run_gif_surface()
    # qw.run_gif_surface(plot_t_step=2000)
    # qw.run_plot_heatmap()
    # qw.run_gif_heatmap()
    # qw.run_gif_heatmap(plot_t_step=2000)
    erase_qw = Erase_EQW(select_exp_indexes=[10, 20, 30, 40])
    qw.run_kl_div(qw_obj=erase_qw)
