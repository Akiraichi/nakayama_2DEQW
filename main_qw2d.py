# config
from analyze.visualization.plot_kl import plot_kl
# exp_setting
from exp_setting.exp import *
# simulation
from simulation.simulation import start_simulation_2dqw
# plot
from analyze.visualization.plot_image import *
from analyze.visualization.make_gif import make_gif_image


class MaxTimeError(Exception):
    pass


class QW:
    def __init__(self, e1, e2, select_exp_indexes=None):
        self.selected_exp_indexes = select_exp_indexes
        if ConfigSimulation.MaxTimeStep == 600 or ConfigSimulation.MaxTimeStep == 100 \
                or ConfigSimulation.MaxTimeStep == 200:
            if select_exp_indexes is None:
                self.selected_conditions, self.exp_name = e1()
            else:
                self.selected_conditions, self.exp_name = e1(select_exp_indexes)
        elif ConfigSimulation.MaxTimeStep == 2000:
            if select_exp_indexes is None:
                self.selected_conditions, self.exp_name = e2()
            else:
                self.selected_conditions, self.exp_name = e2(select_exp_indexes)
        else:
            raise MaxTimeError(ConfigSimulation.MaxTimeStep)

    def run_simulation(self, start_step_t=0):
        start_simulation_2dqw(exp_conditions=self.selected_conditions, start_step_t=start_step_t)

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

    def run_kl_div(self, qw_obj):
        plot_kl(exp1_name=self.exp_name, exp1_index=0, exp2_name=qw_obj.exp_name,
                exp2_indexes=qw_obj.selected_exp_indexes)


class Normal_QW(QW):
    """
    通常の量子ウォーク
    """

    def __init__(self):
        super().__init__(e1=exp_018, e2=exp_022)


class Erase_EQW(QW):
    """
    電場量子ウォーク
    pi/60
    """

    def __init__(self, select_exp_indexes):
        super().__init__(e1=exp_019, e2=exp_021, select_exp_indexes=select_exp_indexes)


class SlowEraseEQW(QW):
    """
    ゆっくり電場を消す電場量子ウォーク
    pi/60
    電場をどのくらいゆっくり消すかによって、実験を変えるのか、電場をどのくらいゆっくり消すかは固定にさせて、
    色々なパラメータで実験するのかを検討
    """

    def __init__(self, select_exp_indexes):
        super().__init__(e1=exp_023, e2=exp_024, select_exp_indexes=select_exp_indexes)


if __name__ == '__main__':
    qw = SlowEraseEQW(select_exp_indexes=[0])
    qw.run_simulation()
    qw.run_plot_surface()
    qw.run_gif_surface()
    # qw.run_gif_surface(plot_t_step=100)
    # qw.run_plot_heatmap()
    # qw.run_gif_heatmap()
    # qw.run_gif_heatmap(plot_t_step=100)

    # erase_qw = Erase_EQW(select_exp_indexes=[20])
    # erase_qw.run_simulation()
    # erase_qw.run_plot_surface()
    # erase_qw.run_gif_surface(plot_t_step=100)

    # qw.run_kl_div(qw_obj=erase_qw)
