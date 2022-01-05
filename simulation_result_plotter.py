# from analyze.visualization.analyzer import analyze
from conditions_factories.conditions_erase_t_factory import ConditionsEraseTFactory
from conditions_factories.conditions_single_factory import ConditionsSingleFactory
from analyze.visualization.plot_image import *
from analyze.visualization.make_gif import output_gif_image

DefaultPlotSetting = {
    "is_enlarge": False,  # Trueにした場合、最大時間ステップまでの範囲でプロットする
    "parallel": True,  # Trueにした場合、並列処理を行う
    "plot_only_ts": select_plot_t_step_by_100(),  # プロットしたいtをlistの形式で指定する
    "plot_type": None,
}


class SimulationResultPlotter:
    """
    Simulationの結果データを元にプロットする関数
    """

    def __init__(self, conditions, save_path_indexes=None, options=None):
        """
        Args:
            conditions: プロットしたい実験条件をリストで指定する
        """

        self.__conditions = conditions
        self.__save_path_indexes = save_path_indexes
        self.__options = options
        self.__check_params()

    def __check_params(self):
        """パラメータが適切かどうかチェック"""
        if self.__options is None:
            self.__options = {}
        if self.__save_path_indexes is None:
            self.__save_path_indexes = [0]
        if len(self.__conditions) != len(self.__save_path_indexes):
            print_warning("conditionの数とsave_path_indexの数が一致していません")
            raise OSError

    def plot_surface(self):
        self.__options["plot_type"] = "surface"
        plot_image(conditions=self.__conditions, save_path_indexes=self.__save_path_indexes,
                   **{**DefaultPlotSetting, **self.__options})

    def plot_heatmap(self):
        self.__options["plot_type"] = "heatmap"
        plot_image(conditions=self.__conditions, save_path_indexes=self.__save_path_indexes,
                   **{**DefaultPlotSetting, **self.__options})

    # def output_gif_surface(self, save_path_indexes=None, options=None):
    #     output_gif_image(exp_name=self.__exp_name, plot_type="surface",
    #                      plot_exp_indexes=save_path_indexes,
    #                      plot_t_step=plot_t_step)
    #
    # def output_gif_heatmap(self, save_path_indexes=None, options=None
    #                        ):
    #     output_gif_image(exp_name=self.__exp_name, plot_type="heatmap",
    #                      plot_exp_indexes=save_path_indexes,
    #                      plot_t_step=plot_t_step)

    # def kl_div(self, qw_obj):
    #     """
    #     conditionsで指定されている実験条件において、qw_obj と確率分布の差を比較する。
    #     Args:
    #         qw_obj:
    #
    #     Returns:
    #
    #     """
    #     analyze(conditions = self.__conditions, )
    # plot_kl(exp1_name=self.exp_name, exp1_index=0, exp2_name=qw_obj.exp_name,
    #         exp2_indexes=qw_obj.selected_exp_indexes, cut_circle_r=cut_circle_r, parallel=parallel)
    #
    # def kl_div_compare_t(self, qw_obj, cut_circle_r, parallel):
    #     plot_kl(exp1_name=self.exp_name, exp1_index=0, exp2_name=qw_obj.exp_name,
    #             exp2_indexes=qw_obj.selected_exp_indexes, cut_circle_r=cut_circle_r, parallel=parallel)
    #
    # def plot_width(self, cut_circle_r):
    #     # plot_width_prob(exp_name=self.exp_name, plot_exp_indexes=self.selected_exp_indexes)
    #     main_analyze(exp_name=self.exp_name, exp_indexes=self.selected_exp_indexes, cut_circle_r=cut_circle_r,
    #                  circle_inner_r=0, circle_outer_r=0, ext="width")
    #
    # def prob(self, cut_circle_r, circle_inner_r, circle_outer_r, parallel):
    #     # plot_prob(exp_name=self.exp_name, exp_indexes=self.selected_exp_indexes, cut_circle_r=cut_circle_r,
    #     #           circle_inner_r=circle_inner_r, circle_outer_r=circle_outer_r, parallel=parallel)
    #     main_analyze(exp_name=self.exp_name, exp_indexes=self.selected_exp_indexes, cut_circle_r=cut_circle_r,
    #                  circle_inner_r=circle_inner_r, circle_outer_r=circle_outer_r, ext="prob")
    #
    # def var(self, cut_circle_r):
    #     main_analyze(exp_name=self.exp_name, exp_indexes=self.selected_exp_indexes, cut_circle_r=cut_circle_r,
    #                  circle_inner_r=0, circle_outer_r=0, ext="var")
    #
    # def analyze(self, cut_circle_r, circle_inner_r, circle_outer_r):
    #     main_analyze(exp_name=self.exp_name, exp_indexes=self.selected_exp_indexes, cut_circle_r=cut_circle_r,
    #                  circle_inner_r=circle_inner_r, circle_outer_r=circle_outer_r, ext="all")
