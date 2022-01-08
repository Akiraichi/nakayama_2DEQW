import dataclasses

from config.config_visualization import DefaultPlotSetting
from data_analysis.visualization.plot_image import plot_image


class SimulationResultPlotter:
    def __init__(self, conditions, save_path_indexes):
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
