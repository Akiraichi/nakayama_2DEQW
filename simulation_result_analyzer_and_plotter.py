from config.config_data_analyze import AnalyzeNameSetting, DefaultAnalyzeSetting, DefaultAnalyzeOptimizeSetting, \
    DefaultAnalyzePlotSetting, OptimizePlotSetting, AnalysisOptimizeSaveName
from data_analysis.data_analyze.analyzer import Analyzer, AnalyzeOptimizer
from data_analysis.data_analyze.plot_analyze import AnalyzePlotter, OptimizePlotter
from qw import *
import dataclasses


class SimulationResultAnalyzer:
    def __init__(self, qw1, qw2, _analyze_indexes):
        self.__exp1_name = qw1.conditions[0].exp_name  # 代表して0番目を使用
        self.__exp2_name = qw2.conditions[0].exp_name  # 代表して0番目を使用
        self.__exp1_index = 0  # 代表して0を使用
        self.__analyze_indexes = _analyze_indexes

    def analyze(self, options=None):
        _setting = DefaultAnalyzeSetting()
        if options is not None:
            _setting = dataclasses.replace(_setting, **options)
        analyzer_ = Analyzer(self.__exp1_name, self.__exp2_name, self.__exp1_index, self.__analyze_indexes,
                             setting=_setting)
        analyzer_.start_processing()

    def plot_x_axis_is_index(self, _plot_t_list, options=None):
        # デフォルト設定
        path_to_file = AnalyzeNameSetting(exp1_name=self.__exp1_name, exp2_name=self.__exp2_name,
                                          exp1_index=self.__exp1_index).path_to_file
        _setting = DefaultAnalyzePlotSetting(x_label="t_{erase}", y_label="", legend_label="t",
                                             plot_indexes=_plot_t_list, path_to_file=path_to_file,
                                             file_name="", x_axis="index")
        # オプション設定があれば適用
        if options is not None:
            _setting = dataclasses.replace(_setting, **options)

        plotter = AnalyzePlotter(self.__exp1_name, self.__exp2_name, self.__exp1_index, self.__analyze_indexes,
                                 _plot_t_list, _setting)
        plotter.plot()

    def plot_x_axis_is_t(self, _plot_indexes, start_t=0, options=None):
        """
        x軸に時間ステップtをとってプロットする
        Args:
            _plot_indexes:
            start_t: x軸の原点
            options:オプション設定
        """
        # デフォルト設定
        path_to_file = AnalyzeNameSetting(exp1_name=self.__exp1_name, exp2_name=self.__exp2_name,
                                          exp1_index=self.__exp1_index).path_to_file
        _setting = DefaultAnalyzePlotSetting(x_label="t", y_label="", legend_label="t_{erase}",
                                             plot_indexes=_plot_indexes, start_t=start_t, path_to_file=path_to_file,
                                             file_name="", x_axis="t")
        # オプション設定があれば適用
        if options is not None:
            _setting = dataclasses.replace(_setting, **options)

        plotter = AnalyzePlotter(self.__exp1_name, self.__exp2_name, self.__exp1_index, self.__analyze_indexes,
                                 _plot_indexes, _setting)
        plotter.plot()

    def analyze_for_optimization_t(self, analyze_t, options=None):
        """
        self.__qw1とself.__qw2の確率分布の類似性について、self.__analyze_indexesに指定された実験全てにおいて、analyze_tステップ目の
        qw2の確率分布と最も確率分布の近いqw1の時間ステップtを求める。
        Args:
            analyze_t: 調べる際の時間ステップ
            options:オプション設定

        Returns:

        """
        _setting = DefaultAnalyzeOptimizeSetting(analyze_t=analyze_t)
        if options is not None:
            _setting = dataclasses.replace(_setting, **options)
        analyzer_ = AnalyzeOptimizer(self.__exp1_name, self.__exp2_name, self.__exp1_index, self.__analyze_indexes,
                                     setting=_setting)
        analyzer_.optimize_t_all()

    def print_optimize_t(self, analyze_t):
        _setting = OptimizePlotSetting(x_label="", y_label="", title="", legend_label="",
                                       x_axis_data_list=self.__analyze_indexes,
                                       path_to_file="",
                                       y_axis_dates_list=[],
                                       file_name="", analyze_t=analyze_t, x_axis="")
        plotter = OptimizePlotter(self.__exp1_name, self.__exp2_name, self.__exp1_index, self.__analyze_indexes,
                                  setting=_setting)
        plotter.print_all_optimize_result()

    def plot_optimize_x_axis_is_index(self, analyze_t, options=None):
        save_name = AnalysisOptimizeSaveName(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
                                             exp2_name=self.__exp2_name, analyze_t=analyze_t)

        _setting = OptimizePlotSetting(x_label="t_{erase}", y_label="t", legend_label="rank",
                                       x_axis_data_list=self.__analyze_indexes,
                                       path_to_file=save_name.path_to_file, analyze_t=analyze_t, x_axis="index")
        # オプション設定があれば適用
        if options is not None:
            _setting = dataclasses.replace(_setting, **options)

        plotter = OptimizePlotter(self.__exp1_name, self.__exp2_name, self.__exp1_index, self.__analyze_indexes,
                                  setting=_setting)
        plotter.plot_optimize_result_x_axis_is_index()

    def plot_optimize_x_axis_is_rank(self, analyze_t, options=None):
        name_setting = AnalysisOptimizeSaveName(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
                                                exp2_name=self.__exp2_name, analyze_t=analyze_t)

        _setting = OptimizePlotSetting(x_label="rank", y_label="t", legend_label="t_{erase}",
                                       path_to_file=name_setting.path_to_file, analyze_t=analyze_t,
                                       x_axis="rank")
        _setting.x_axis_data_list = list(range(1, _setting.limit_rank + 1))
        # オプション設定があれば適用
        if options is not None:
            _setting = dataclasses.replace(_setting, **options)

        plotter = OptimizePlotter(self.__exp1_name, self.__exp2_name, self.__exp1_index, self.__analyze_indexes,
                                  setting=_setting)
        plotter.plot_optimize_result_x_axis_is_rank()


if __name__ == '__main__':
    # analyze_indexes = list(range(1, 101))
    # analyze_indexes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    analyze_indexes = [100]
    analyzer = SimulationResultAnalyzer(qw1=GroverWalk2D(),
                                        qw2=EraseElectricGroverWalk2DAlongXY(erase_t_list=analyze_indexes),
                                        _analyze_indexes=analyze_indexes)
    # analyze処理を実行
    # analyzer.analyze()
    # その結果をプロット
    # plot_indexes = analyze_indexes
    # plot_t_list = [200, 300, 400, 500, 600]
    # analyzer.plot_x_axis_is_index(_plot_t_list=plot_t_list)
    # analyzer.plot_x_axis_is_t(_plot_indexes=plot_indexes)

    # 最適な時間ステップを求める
    # analyzer.analyze_for_optimization_t(analyze_t=200, options={"t_list": list(range(1, 201))})
    # その結果をプロット
    # analyzer.print_optimize_t(analyze_t=200)
    # analyzer.plot_optimize_x_axis_is_index(analyze_t=600, options={"limit": 5})
    analyzer.plot_optimize_x_axis_is_rank(analyze_t=600)
