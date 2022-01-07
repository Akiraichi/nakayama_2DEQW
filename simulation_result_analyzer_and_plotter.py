from analyze.visualization.analyzer import Analyzer
from analyze.visualization.plot_analyze import AnalyzePlotter, OptimizePlotter
from qw import *

DefaultAnalyzeSetting = {
    "parallel": False,  # 処理を並列化するかどうか。現状Falseのほうが高速
    "KL_div": True,  # KLダイバージェンスを求めるかどうか
    "L1_norm": True,  # L1ノルムを求めるかどうか（誤差の絶対値の和）
    "L2_norm": True,  # L2ノルムを求めるかどうか（二乗誤差の和）
    "correlation_coefficient": True  # 相関係数を求めるかどうか
}


class SimulationResultAnalyzer:
    def __init__(self, qw1, qw2, analyze_indexes, options=None):
        self.__qw1 = qw1
        self.__qw2 = qw2
        self.__analyze_indexes = analyze_indexes
        if options is None:
            options = {}
        self.__options = {**DefaultAnalyzeSetting, **options}
        # パラメータをチェック
        self.__check_params()

    def __check_params(self):
        if self.__options is None:
            self.__options = {}

    def analyze(self):
        analyzer_ = Analyzer(self.__qw1, self.__qw2, self.__analyze_indexes, self.__options, mode="analyze")
        analyzer_.start_processing()

    def plot_x_axis_is_index(self, plot_t_list):
        plotter = AnalyzePlotter(self.__qw1, self.__qw2, self.__analyze_indexes, plot_t_list, x_axis="index")
        plotter.plot()

    def plot_x_axis_is_t(self, plot_indexes, start_t=0):
        plotter = AnalyzePlotter(self.__qw1, self.__qw2, self.__analyze_indexes, plot_indexes, x_axis="t",
                                 start_t=start_t)
        plotter.plot()

    def analyze_for_optimization_t(self, analyze_t):
        """
        self.__qw1とself.__qw2の確率分布の類似性について、self.__analyze_indexesに指定された実験全てにおいて、analyze_tステップ目の
        qw2の確率分布と最も確率分布の近いqw1の時間ステップtを求める。
        Args:
            analyze_t: 調べる際の時間ステップ

        Returns:

        """
        analyzer_ = Analyzer(self.__qw1, self.__qw2, self.__analyze_indexes, self.__options, mode="optimize")
        analyzer_.optimize_t(analyze_t=analyze_t)

    def plot_optimize_t(self, analyze_t):
        plotter = OptimizePlotter(self.__qw1, self.__qw2, self.__analyze_indexes, analyze_t)
        plotter.print_optimized_result()


if __name__ == '__main__':
    indexes = [50]
    analyzer = SimulationResultAnalyzer(qw1=GroverWalk2D(),
                                        qw2=EraseElectricGroverWalk2DAlongX(erase_t_list=indexes),
                                        analyze_indexes=indexes,
                                        options={"parallel": False})
    # analyzer.analyze()
    # analyzer.analyze_for_optimization_t(analyze_t=200)
    analyzer.plot_optimize_t(analyze_t=200)
    # t_list = [200, 300, 400, 500, 600]
    # analyzer.plot_x_axis_is_index(plot_t_list=t_list)
    # plot_indexes = [0]
    # analyzer.plot_x_axis_is_t(plot_indexes=plot_indexes, start_t=0)
