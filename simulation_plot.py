import dataclasses

from config.config_visualization import DefaultPlotSetting
from data_analysis.visualization.plot_image import plot_image
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


if __name__ == '__main__':
    indexes = [0]
    plotter = SimulationResultPlotter(conditions=ConditionsSingleFactory().single_007_GroverWalk2D(),
                                      save_path_indexes=indexes)
    plotter.plot_heatmap()
