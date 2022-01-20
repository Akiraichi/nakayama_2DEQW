import dataclasses

from config.config_visualization import DefaultPlotSetting, Plot3dSetting
from data_analysis.visualization.plot_image import plot_image, plot_image_group, plot_3d_image
from simulation.condition import ConditionNew
from simulation.conditions_factories.conditions_single_factory import ConditionsSingleFactory
from simulation.conditions_factories.conditions_erase_t_factory import ConditionsEraseTFactory
from typing import List


class SimulationResultPlotter:
    def __init__(self, conditions: List[ConditionNew], save_path_indexes):
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
        self.__save_path_indexes = save_path_indexes  # 不要ではある.conditionから持ってこれるから

    def plot_surface(self, options=None):
        plot_type = "surface"
        _setting = DefaultPlotSetting(plot_type, self.__conditions, 800, self.__save_path_indexes)
        if options is not None:
            _setting = dataclasses.replace(_setting, **options)
        plot_image(_setting=_setting)

    def plot_heatmap(self, options=None):
        plot_type = "heatmap"
        _setting = DefaultPlotSetting(plot_type, self.__conditions, 400, self.__save_path_indexes)
        if options is not None:
            _setting = dataclasses.replace(_setting, **options)
        plot_image(_setting=_setting)

    def plot_3d_images(self, plot_t_list, z_axis):
        """
        z軸を時間ステップtとした3d_heatmapを作成する。save_path_indexesで指定されたindex全てに対して実行
        Args:
            plot_t_list: z軸にプロットするtをリストで指定したもの
            z_axis:iかtを指定

        Returns:

        """
        _setting = Plot3dSetting(plot_type="heatmap", plot_t_list=plot_t_list, plot_index_list=self.__save_path_indexes,
                                 conditions=self.__conditions, z_axis=z_axis)
        plot_3d_image(_setting)

    def plot_surface_group_by(self, _t_of_plot_list, gif_only=False):
        plot_type = "surface"
        _setting = DefaultPlotSetting(plot_type, self.__conditions, 800, self.__save_path_indexes)
        options = {"plot_t_list": _t_of_plot_list}
        _setting = dataclasses.replace(_setting, **options)
        plot_image_group(_setting=_setting, gif_only=gif_only)

    def plot_heatmap_group_by(self, _t_of_plot_list, gif_only=False):
        plot_type = "heatmap"
        _setting = DefaultPlotSetting(plot_type, self.__conditions, 400, self.__save_path_indexes)
        options = {"plot_t_list": _t_of_plot_list}
        _setting = dataclasses.replace(_setting, **options)
        plot_image_group(_setting=_setting, gif_only=gif_only)


if __name__ == '__main__':
    # indexes = [0]
    # indexes = list(range(16, 256, 15))
    indexes = [16, 31, 46]
    plotter = SimulationResultPlotter(
        conditions=ConditionsEraseTFactory.EraseT_005_EraseElectricGroverWalk2DAlongX(erase_t_list=indexes),
        save_path_indexes=indexes)
    # plotter = SimulationResultPlotter(
    #     conditions=ConditionsSingleFactory.single_007_GroverWalk2D(),
    #     save_path_indexes=indexes)
    # plotter.plot_surface()
    # plotter.plot_heatmap(options={"plot_t_list": [118]})
    # plotter.plot_heatmap()
    t_of_plot_list = [100 + index for index in indexes]

    plotter.plot_heatmap_group_by(_t_of_plot_list=[200] * len(indexes))
    plotter.plot_surface_group_by(_t_of_plot_list=[200] * len(indexes))
    # plotter.plot_3d_images(plot_t_list=[15, 30, 45, 60, 75, 90, 105, 120, 135], z_axis="t")
    # plotter.plot_3d_images(plot_t_list=[15, 30, 45], z_axis="t")
    # plotter.plot_3d_images(plot_t_list=[200], z_axis="i")

    # indexes = [121]
    # indexes = list(range(16, 46, 15))
    # plotter = SimulationResultPlotter(
    #     conditions=ConditionsEraseTFactory.EraseT_005_EraseElectricGroverWalk2DAlongX(erase_t_list=indexes),
    #     save_path_indexes=indexes)
    # plotter.plot_3d_images(plot_t_list=list(range(15, 210, 15)), z_axis="t")
    # plotter.plot_3d_images(plot_t_list=list(range(60,660,60)), z_axis="t")
    # plotter.plot_3d_images(plot_t_list=list(range(30,630,30)), z_axis="t")
    # plotter.plot_3d_images(plot_t_list=[100, 200], z_axis="t")

    # indexes = list(range(16, 256, 15))
    # indexes = [121]
    # plotter = SimulationResultPlotter(
    #     conditions=ConditionsEraseTFactory.EraseT_006_EraseElectricGroverWalk2DAlongXY(erase_t_list=indexes),
    #     save_path_indexes=indexes)
    # plotter.plot_3d_images(plot_t_list=[120, 240, 360, 480, 600], z_axis="t")
    # plotter.plot_3d_images(plot_t_list=list(range(60, 660, 60)), z_axis="t")
    # plotter.plot_3d_images(plot_t_list=list(range(30, 630, 30)), z_axis="t")
    # plotter.plot_3d_images(plot_t_list=[600], z_axis="i")
