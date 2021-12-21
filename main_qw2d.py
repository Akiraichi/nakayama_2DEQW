# config
from analyze.visualization.analyze_prob import main_analyze
from analyze.visualization.plot_kl import plot_kl
# exp_setting
from analyze.visualization.plot_prob import plot_prob
from analyze.visualization.plot_width_prob import plot_width_prob
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
                self.selected_exp_indexes = [0]
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

    def run_plot_surface(self, is_enlarge, parallel, plot_only_ts=None):
        plot_image(exp_name=self.exp_name, plot_type="surface", plot_exp_indexes=self.selected_exp_indexes,
                   is_enlarge=is_enlarge, parallel=parallel, plot_only_ts=plot_only_ts)

    def run_plot_heatmap(self, is_enlarge, parallel, plot_only_ts=None):
        """
        plot_ony_ts：listの形式でプロットしたいtを指定すること
        """
        plot_image(exp_name=self.exp_name, plot_type="heatmap", plot_exp_indexes=self.selected_exp_indexes,
                   is_enlarge=is_enlarge, parallel=parallel, plot_only_ts=plot_only_ts)

    def run_gif_surface(self, plot_t_step=None):
        make_gif_image(exp_name=self.exp_name, plot_type="surface", plot_exp_indexes=self.selected_exp_indexes,
                       plot_t_step=plot_t_step)

    def run_gif_heatmap(self, plot_t_step=None):
        make_gif_image(exp_name=self.exp_name, plot_type="heatmap", plot_exp_indexes=self.selected_exp_indexes,
                       plot_t_step=plot_t_step)

    def run_kl_div(self, qw_obj, cut_circle_r, parallel):
        plot_kl(exp1_name=self.exp_name, exp1_index=0, exp2_name=qw_obj.exp_name,
                exp2_indexes=qw_obj.selected_exp_indexes, cut_circle_r=cut_circle_r, parallel=parallel)

    def run_kl_div_compare_t(self, qw_obj, cut_circle_r, parallel):
        plot_kl(exp1_name=self.exp_name, exp1_index=0, exp2_name=qw_obj.exp_name,
                exp2_indexes=qw_obj.selected_exp_indexes, cut_circle_r=cut_circle_r, parallel=parallel)

    def run_plot_width(self, cut_circle_r):
        # plot_width_prob(exp_name=self.exp_name, plot_exp_indexes=self.selected_exp_indexes)
        main_analyze(exp_name=self.exp_name, exp_indexes=self.selected_exp_indexes, cut_circle_r=cut_circle_r,
                     circle_inner_r=0, circle_outer_r=0, ext="width")

    def run_prob(self, cut_circle_r, circle_inner_r, circle_outer_r, parallel):
        # plot_prob(exp_name=self.exp_name, exp_indexes=self.selected_exp_indexes, cut_circle_r=cut_circle_r,
        #           circle_inner_r=circle_inner_r, circle_outer_r=circle_outer_r, parallel=parallel)
        main_analyze(exp_name=self.exp_name, exp_indexes=self.selected_exp_indexes, cut_circle_r=cut_circle_r,
                     circle_inner_r=circle_inner_r, circle_outer_r=circle_outer_r, ext="prob")

    def run_var(self, cut_circle_r):
        main_analyze(exp_name=self.exp_name, exp_indexes=self.selected_exp_indexes, cut_circle_r=cut_circle_r,
                     circle_inner_r=0, circle_outer_r=0, ext="var")

    def run_analyze(self, cut_circle_r, circle_inner_r, circle_outer_r):
        main_analyze(exp_name=self.exp_name, exp_indexes=self.selected_exp_indexes, cut_circle_r=cut_circle_r,
                     circle_inner_r=circle_inner_r, circle_outer_r=circle_outer_r, ext="all")


class GroverWalk2D(QW):
    def __init__(self):
        super().__init__(e1=exp_050, e2=exp_051)


class ElectricGroverWalk2DAlongX(QW):
    def __init__(self):
        super().__init__(e1=exp_052, e2=exp_053)


class ElectricGroverWalk2DAlongXY(QW):
    def __init__(self):
        super().__init__(e1=exp_054, e2=exp_055)


class EraseElectricGroverWalk2DAlongX(QW):
    def __init__(self, select_exp_indexes):
        super().__init__(e1=exp_019, e2=exp_021, select_exp_indexes=select_exp_indexes)


class EraseElectricGroverWalk2DAlongXY(QW):
    def __init__(self, select_exp_indexes):
        super().__init__(e1=exp_058, e2=exp_059, select_exp_indexes=select_exp_indexes)


class SlowEraseEQW(QW):
    """
    ゆっくり電場を消す電場量子ウォーク
    pi/60
    電場をどのくらいゆっくり消すかによって、実験を変えるのか、電場をどのくらいゆっくり消すかは固定にさせて、
    色々なパラメータで実験するのかを検討
    """

    def __init__(self, select_exp_indexes):
        super().__init__(e1=exp_023, e2=exp_024, select_exp_indexes=select_exp_indexes)


class SlowEraseEQW_erase_t_0(QW):
    """
    ゆっくり電場を消す電場量子ウォーク
    pi/60
    電場をどのくらいゆっくり消すか、電場を消す時間ステップ数を変更して実験する
    t=0で電場を消し始める
    """

    def __init__(self, erase_time_steps):
        super().__init__(e1=exp_025, e2=exp_026, select_exp_indexes=erase_time_steps)


class SlowEraseEQW_erase_t_200(QW):
    """
    ゆっくり電場を消す電場量子ウォーク
    pi/60
    電場をどのくらいゆっくり消すか、電場を消す時間ステップ数を変更して実験する
    t=200で電場を消し始める
    """

    def __init__(self, erase_time_steps):
        super().__init__(e1=exp_027, e2=exp_028, select_exp_indexes=erase_time_steps)


class HadamardWalk2D(QW):
    def __init__(self):
        super().__init__(e1=exp_030, e2=exp_031)


class ElectricHadamardWalk2DAlongX(QW):
    def __init__(self):
        super().__init__(e1=exp_032, e2=exp_033)


class ElectricHadamardWalk2DAlongXY(QW):
    def __init__(self):
        super().__init__(e1=exp_034, e2=exp_035)


class EraseElectricHadamardWalk2DAlongX(QW):
    def __init__(self, select_exp_indexes):
        super().__init__(e1=exp_036, e2=exp_037, select_exp_indexes=select_exp_indexes)


class EraseElectricHadamardWalk2DAlongXY(QW):
    def __init__(self, select_exp_indexes):
        super().__init__(e1=exp_038, e2=exp_039, select_exp_indexes=select_exp_indexes)


class DFTWalk2D(QW):
    def __init__(self):
        super().__init__(e1=exp_040, e2=exp_041)


class ElectricDFTWalk2DAlongX(QW):
    def __init__(self):
        super().__init__(e1=exp_042, e2=exp_043)


class ElectricDFTWalk2DAlongXY(QW):
    def __init__(self):
        super().__init__(e1=exp_044, e2=exp_045)


class EraseElectricDFTWalk2DAlongX(QW):
    def __init__(self, select_exp_indexes):
        super().__init__(e1=exp_046, e2=exp_047, select_exp_indexes=select_exp_indexes)


class EraseElectricDFTWalk2DAlongXY(QW):
    def __init__(self, select_exp_indexes):
        super().__init__(e1=exp_048, e2=exp_049, select_exp_indexes=select_exp_indexes)


if __name__ == '__main__':
    # test = [[1,2,3],
    #         [4,5,6],
    #         [7,8,9]]
    # np.flipud(test)

    # test = np.zeros([10, 10])
    # i = 0
    # for x in range(10):
    #     for y in range(10):
    #         test[x, y] = i
    #         i += 1
    # print(test)
    qw = GroverWalk2D()
    # qw2 = ElectricGroverWalk2DAlongX()
    # qw.run_analyze(cut_circle_r=10, circle_inner_r=10, circle_outer_r=20)
    # qw2 = ElectricGroverWalk2DAlongX()
    qw.run_simulation(start_step_t=0)
    # qw2.run_simulation(start_step_t=0)
    qw.run_plot_surface(is_enlarge=False, parallel=True, plot_only_ts=[1, 2, 3, 4, 5, 6, 7, 78, 8, 9, 99])
    # qw.run_gif_surface(plot_t_step=None)
    # qw.run_plot_heatmap(is_enlarge=False, parallel=True)
    # qw.run_gif_heatmap(plot_t_step=None)
    # qw.run_plot_width(cut_circle_r=100)

    # qw = ElectricHadamardWalk2DAlongX()
    # qw.run_simulation(start_step_t=0)
    # qw.run_plot_surface(is_enlarge=False, parallel=False)
    # qw.run_gif_surface(plot_t_step=None)

    # qw = ElectricDFTWalk2DAlongX()
    # qw.run_simulation(start_step_t=0)
    # qw.run_plot_surface(is_enlarge=False, parallel=False)
    # qw.run_gif_surface(plot_t_step=None)

    # qw = ElectricGroverWalk2DAlongXY()
    # qw.run_simulation(start_step_t=0)
    # qw.run_plot_surface(is_enlarge=False, parallel=False)
    # qw.run_gif_surface(plot_t_step=None)

    # erase_qw = EraseElectricDFTWalk2DAlongXY(select_exp_indexes=[10, 20, 30, 40])
    # erase_qw.run_simulation(start_step_t=0)
    # erase_qw.run_plot_surface(is_enlarge=False, parallel=False)
    # erase_qw.run_plot_heatmap(is_enlarge=False, parallel=False)
    # erase_qw.run_gif_surface(plot_t_step=None)
    # erase_qw.run_gif_heatmap(plot_t_step=None)
    # erase_qw.run_plot_width(cut_circle_r=100)
    # erase_qw.run_prob(cut_circle_r=20, circle_inner_r=30, circle_outer_r=50, parallel=False)
    # erase_qw.run_var(cut_circle_r=20)
    # erase_qw.run_analyze(cut_circle_r=20, circle_inner_r=30, circle_outer_r=50)

    # qw = GroverWalk2D()
    # qw.run_simulation(start_step_t=0)
    # qw.run_plot_surface(is_enlarge=False,parallel=True)
    # qw.run_plot_heatmap(is_enlarge=True)
    # qw.run_gif_surface(plot_t_step=None)
    # qw.run_gif_heatmap(plot_t_step=None)
    # qw.run_plot_width()
    #
    # erase_qw = EraseElectricGroverWalk2DAlongX(select_exp_indexes=[300, 400, 500, 599])
    # erase_qw.run_simulation(start_step_t=0)
    # erase_qw.run_plot_surface(is_enlarge=False)
    # erase_qw.run_plot_heatmap(is_enlarge=True, parallel=True)
    # erase_qw.run_gif_surface(plot_t_step=None)
    # erase_qw.run_gif_heatmap(plot_t_step=None)
    # erase_qw.run_plot_width(cut_circle_r=100)
    # erase_qw.run_prob(cut_circle_r=20, circle_inner_r=30, circle_outer_r=50, parallel=False)
    # erase_qw.run_var(cut_circle_r=20)
    # erase_qw.run_analyze(cut_circle_r=20, circle_inner_r=30, circle_outer_r=50)
    #
    # slow_erase_qw = SlowEraseEQW(select_exp_indexes=[0])
    # slow_erase_qw.run_simulation()
    # slow_erase_qw.run_plot_surface()
    # slow_erase_qw.run_gif_surface()
    # slow_erase_qw.run_plot_heatmap()
    # slow_erase_qw.run_gif_heatmap()
    #
    # slow_erase_qw_step_0 = SlowEraseEQW_erase_t_0(erase_time_steps=[100])
    # slow_erase_qw_step_0.run_simulation()
    # slow_erase_qw_step_0.run_plot_surface()
    # slow_erase_qw_step_0.run_gif_surface()
    # slow_erase_qw_step_0.run_plot_heatmap()
    # slow_erase_qw_step_0.run_gif_heatmap()
    #
    qw.run_kl_div(qw_obj=qw2, cut_circle_r=10, parallel=False)
