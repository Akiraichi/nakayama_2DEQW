import dataclasses

from config.config_visualization import DefaultPlotSetting, Plot3dSetting
from data_analysis.visualization.plot_image import plot_image, plot_image_group, create_3d_image_data_cmp_t
from simulation.conditions_factories.conditions_single_factory import ConditionsSingleFactory
from simulation.conditions_factories.conditions_erase_t_factory import ConditionsEraseTFactory


class SimulationResultPlotter:
    def __init__(self, conditions, save_path_indexes):
        """
        plot_t_listで指定されたtのプロットを行う。
        例：plot_t_list=[200]の場合
        0200.jbをプロットする。0200.jbは200ステップ目が完了した時点（つまり、t=200）のシステム全体の確率振幅ベクトルを保存したファイル
        例：ψ_{t=200}をプロットしたい場合
        plot_t_list=[200]とする。
        Args:
            conditions: 実験条件をリストで指定したもの
            save_path_indexes: 保存する際のフォルダ名に使うindexのリスト
        """
        self.__conditions = conditions
        self.__save_path_indexes = save_path_indexes

    def plot_surface(self, options=None):
        plot_type = "surface"
        _setting = DefaultPlotSetting(plot_type, self.__conditions, self.__save_path_indexes)
        if options is not None:
            _setting = dataclasses.replace(_setting, **options)
        plot_image(_setting=_setting)

    def plot_heatmap(self, options=None):
        plot_type = "heatmap"
        _setting = DefaultPlotSetting(plot_type, self.__conditions, self.__save_path_indexes)
        if options is not None:
            _setting = dataclasses.replace(_setting, **options)
        plot_image(_setting=_setting)

    def plot_3d_image_cmp_t(self, plot_t_list):
        """
        z軸を時間ステップtとした3d_heatmapを作成する。save_path_indexesで指定されたindex全てに対して実行
        Args:
            plot_t_list: z軸にプロットするtをリストで指定したもの

        Returns:

        """
        for i in range(len(self.__conditions)):
            exp_name = self.__conditions[i].exp_name
            _setting = Plot3dSetting(exp_name=exp_name, plot_type="heatmap", plot_t_list=plot_t_list,
                                     plot_index_list=self.__save_path_indexes, z_axis="t")
            create_3d_image_data_cmp_t(_setting)

    def plot_surface_group_by(self, t_of_plot_list):
        plot_type = "surface"
        _setting = DefaultPlotSetting(plot_type, self.__conditions, self.__save_path_indexes)
        options = {"plot_t_list": t_of_plot_list}
        _setting = dataclasses.replace(_setting, **options)
        plot_image_group(_setting=_setting)

    def plot_heatmap_group_by(self, t_of_plot_list):
        plot_type = "heatmap"
        _setting = DefaultPlotSetting(plot_type, self.__conditions, self.__save_path_indexes)
        options = {"plot_t_list": t_of_plot_list}
        _setting = dataclasses.replace(_setting, **options)
        plot_image_group(_setting=_setting)


if __name__ == '__main__':
    indexes = [0]
    # plotter = SimulationResultPlotter(
    #     conditions=ConditionsEraseTFactory.EraseT_005_EraseElectricGroverWalk2DAlongX(erase_t_list=indexes),
    #     save_path_indexes=indexes)
    plotter = SimulationResultPlotter(
        conditions=ConditionsSingleFactory.single_007_GroverWalk2D(),
        save_path_indexes=indexes)
    # plotter.plot_surface()
    # plotter.plot_heatmap(options={"plot_t_list": [118]})
    # plotter.plot_heatmap()

    # plotter.plot_heatmap_group_by(t_of_plot_list=[200] * len(indexes))
    plotter.plot_3d_image_cmp_t(plot_t_list=[10, 20, 30, 40, 50])
