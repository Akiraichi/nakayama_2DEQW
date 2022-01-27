import helper.helper
from config.config_data_analyze import AnalyzeNameSetting, DefaultAnalyzeSetting, DefaultAnalyzeOptimizeSetting, \
    DefaultAnalyzePlotSetting, OptimizePlotSetting, AnalysisOptimizeSaveName
from data_analysis.data_analyze.analyzer import Analyzer, AnalyzeOptimizer
from data_analysis.data_analyze.plot_analyze import AnalyzePlotter, OptimizePlotter
from simulation.qw import *
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

    def analyze_for_optimization_t(self, _analyze_t, options=None, _qw1_data=None):
        """
        self.__qw1とself.__qw2の確率分布の類似性について、self.__analyze_indexesに指定された実験全てにおいて、analyze_tステップ目の
        qw2の確率分布と最も確率分布の近いqw1の時間ステップtを求める。
        Args:
            _analyze_t: 調べる際の時間ステップ
            options:オプション設定
            _qw1_data: 事前にロードしない場合にセットするためのqw1の確率分布のデータ

        Returns:

        """
        _setting = DefaultAnalyzeOptimizeSetting(analyze_t=_analyze_t)
        if options is not None:
            _setting = dataclasses.replace(_setting, **options)
        analyzer_ = AnalyzeOptimizer(self.__exp1_name, self.__exp2_name, self.__exp1_index, self.__analyze_indexes,
                                     setting=_setting)
        if not _setting.enable_load_qw1_data:
            # 共通データの事前ロードを実行しないのであれば
            analyzer_.set_qw1_data(qw1_data=_qw1_data)
        analyzer_.optimize_t_all()

    def analyze_for_optimize_t_return_qw1_data(self, _analyze_t):
        # STEP1 analyze_tまでのqw1データをロードする
        _setting = DefaultAnalyzeOptimizeSetting(analyze_t=_analyze_t)
        _setting = dataclasses.replace(_setting, **{"t_list": list(range(1, 1 + _analyze_t)),
                                                    "enable_load_qw1_data": False})
        analyzer_ = AnalyzeOptimizer(self.__exp1_name, self.__exp2_name, self.__exp1_index, self.__analyze_indexes,
                                     setting=_setting)
        return analyzer_.return_qw1_data()

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

    def plot_optimize_changed_x_is_analyze_t(self, analyze_t_list, options=None):
        """
        各analyze_tにおいて、最適な時間ステップは何かをプロットする。
        すなわち、t_erase=600において最適な時間ステップが500であるなら、t_erase=550では最適な時間ステップは450であるだろう。
        x軸をanalyze_t, y軸を最適な時間ステップとしてプロットする。
        Args:
            options:

        Returns:

        """
        analyze_t = 200
        save_name = AnalysisOptimizeSaveName(exp1_name=self.__exp1_name, exp1_index=self.__exp1_index,
                                             exp2_name=self.__exp2_name, analyze_t=analyze_t)
        _setting = OptimizePlotSetting(x_label="t_{erase}", y_label="t", legend_label="rank",
                                       x_axis_data_list=self.__analyze_indexes,
                                       path_to_file=save_name.path_to_plot_file, analyze_t=analyze_t, x_axis="index")
        # オプション設定があれば適用
        if options is not None:
            _setting = dataclasses.replace(_setting, **options)
        plotter = OptimizePlotter(self.__exp1_name, self.__exp2_name, self.__exp1_index, self.__analyze_indexes,
                                  setting=_setting)
        plotter.plot_optimize_result_analyze_t_changed(analyze_t_list)

    def Find_time_step_max_indicator(self, _plot_indexes, options=None):
        """電場を消してから指標の最大値がくるまでの時間ステップ数を求める"""
        # デフォルト設定
        path_to_file = AnalyzeNameSetting(exp1_name=self.__exp1_name, exp2_name=self.__exp2_name,
                                          exp1_index=self.__exp1_index).path_to_file
        _setting = DefaultAnalyzePlotSetting(x_label="t_{erase}", y_label="", legend_label="t",
                                             plot_indexes=_plot_indexes, path_to_file=path_to_file,
                                             file_name="", x_axis="index")
        # オプション設定があれば適用
        if options is not None:
            _setting = dataclasses.replace(_setting, **options)

        plotter = AnalyzePlotter(self.__exp1_name, self.__exp2_name, self.__exp1_index, self.__analyze_indexes,
                                 _plot_indexes, _setting)
        plotter.find_time_step_max_indicator()

    def Find_max_indicator(self, _plot_indexes, options=None):
        """電場を消してから指標の最大値がくるまでの時間ステップ数を求める"""
        # デフォルト設定
        path_to_file = AnalyzeNameSetting(exp1_name=self.__exp1_name, exp2_name=self.__exp2_name,
                                          exp1_index=self.__exp1_index).path_to_file
        _setting = DefaultAnalyzePlotSetting(x_label="t_{erase}", y_label="", legend_label="t",
                                             plot_indexes=_plot_indexes, path_to_file=path_to_file,
                                             file_name="", x_axis="index")
        # オプション設定があれば適用
        if options is not None:
            _setting = dataclasses.replace(_setting, **options)

        plotter = AnalyzePlotter(self.__exp1_name, self.__exp2_name, self.__exp1_index, self.__analyze_indexes,
                                 _plot_indexes, _setting)
        plotter.find_max_step_max_indicator()


if __name__ == '__main__':
    # analyze_indexes = list(range(16, 256, 15))
    analyze_indexes = list(range(16, 122, 15))
    # analyze_indexes = list(range(16, 362, 15))
    # analyze_indexes = list(range(31, 392, 30))
    # analyze_indexes = list(range(31, 362, 30))
    # analyze_indexes = list(range(121, 256, 15))
    # analyze_indexes = list(range(2, 122))
    # analyze_indexes = list(range(2, 242))
    # analyze_indexes = list(range(10, 110,10))
    # analyze_indexes = [31, 61, 91]
    # analyze_indexes = [16, 31, 46, 61, 76, 91, 106, 121, 136] + list(range(151, 482, 30)) + [541]
    # analyze_indexes = [16, 31, 46, 61, 76, 91, 106, 121]
    analyzer = SimulationResultAnalyzer(qw1=GroverWalk2D(),
                                        qw2=EraseElectricGroverWalk2DAlongX(erase_t_list=analyze_indexes),
                                        _analyze_indexes=analyze_indexes)
    # analyze処理を実行
    # analyzer.analyze()
    # その結果をプロット
    # plot_indexes = analyze_indexes
    # plot_t_list = [200, 400, 600]
    # analyzer.plot_x_axis_is_index(_plot_t_list=plot_t_list)
    # analyzer.plot_x_axis_is_t(_plot_indexes=analyze_indexes, start_t=200)
    # 電場を消してから指標の最大値がくるまでの時間ステップ数を求める
    # analyzer.Find_time_step_max_indicator(plot_indexes)
    # analyzer.Find_max_indicator(plot_indexes)

    # 最適な時間ステップを求める
    # analyze_t = 600
    # analyzer.analyze_for_optimization_t(_analyze_t=analyze_t, options={"t_list": list(range(1, analyze_t+1))})
    # その結果をプロット
    # analyzer.print_optimize_t(analyze_t=200)
    # analyzer.plot_optimize_x_axis_is_index(analyze_t=1300, options={"limit": 1})
    # analyzer.plot_optimize_x_axis_is_rank(analyze_t=1300)

    analyze_t_list = list(range(20, 601, 10))
    # qw1_data = analyzer.analyze_for_optimize_t_return_qw1_data(_analyze_t=max(analyze_t_list))
    # for analyze_t in analyze_t_list:
    #     analyzer.analyze_for_optimization_t(_analyze_t=analyze_t, options={"t_list": list(range(1, 1 + analyze_t)),
    #                                                                        "enable_load_qw1_data": False},
    #                                         _qw1_data=qw1_data)
    #     helper.helper.print_green_text(f"analyze_t={analyze_t}：完了")
    # analyzer.plot_optimize_changed_x_is_analyze_t(analyze_t_list)

    # for analyze_t in analyze_t_list:
    #     analyzer.analyze_for_optimization_t(_analyze_t=analyze_t, options={"t_list": list(range(1, 201))})
    analyzer.plot_optimize_changed_x_is_analyze_t(analyze_t_list)
