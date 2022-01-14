import dataclasses

from config.config_visualization import DefaultPlotSetting
from data_analysis.visualization.plot_image import plot_image, Plotter
from simulation.conditions_factories.conditions_single_factory import ConditionsSingleFactory
from simulation.conditions_factories.conditions_erase_t_factory import ConditionsEraseTFactory


class SimulationResultPlotter:
    def __init__(self, conditions, save_path_indexes):
        """

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

    def plot_3d_image(self, options=None):
        plot_type = "3d_heatmap"
        _setting = DefaultPlotSetting(plot_type, self.__conditions, self.__save_path_indexes)
        if options is not None:
            _setting = dataclasses.replace(_setting, **options)

        for i in range(len(_setting.conditions)):
            exp_name = _setting.conditions[i].exp_name
            save_path_index = _setting.save_path_indexes[i]

            _plotter = Plotter(exp_mame=exp_name, save_path_index=save_path_index, setting=_setting)
            _plotter.plot_3d_image()


if __name__ == '__main__':
    indexes = [90]
    plotter = SimulationResultPlotter(
        conditions=ConditionsEraseTFactory.EraseT_005_EraseElectricGroverWalk2DAlongX(erase_t_list=[90]),
        save_path_indexes=indexes)
    # plotter.plot_surface()
    # plotter.plot_heatmap()

    plotter.plot_3d_image(options={"plot_t_list": list(range(20, 205, 5))})
    # plotter.plot_3d_image()