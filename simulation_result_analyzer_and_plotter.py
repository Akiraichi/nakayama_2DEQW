from analyze.visualization.analyzer import Analyzer
from analyze.visualization.plot_analyze import AnalyzePlotter
from qw import *

DefaultAnalyzeSetting = {
    "parallel": False,  # 処理を並列化するかどうか。現状Falseのほうが高速
    "KL_div": True,  # KLダイバージェンスを求めるかどうか
    "L1_norm": True,  # L1ノルムを求めるかどうか（誤差の絶対値の和）
    "L2_norm": True,  # L2ノルムを求めるかどうか（二乗誤差の和）
    "correlation_coefficient": False  # 相関係数を求めるかどうか
}


class SimulationResultAnalyzer:
    def __init__(self, qw1, qw2, analyze_indexes, options):
        self.__qw1 = qw1
        self.__qw2 = qw2
        self.__analyze_indexes = analyze_indexes
        self.__options = {**DefaultAnalyzeSetting, **options}
        # パラメータをチェック
        self.__check_params()

    def __check_params(self):
        if self.__options is None:
            self.__options = {}

    def analyze(self):
        analyzer_ = Analyzer(self.__qw1, self.__qw2, self.__analyze_indexes, self.__options)
        analyzer_.start_processing()

    def plot(self):
        plotter = AnalyzePlotter(self.__qw1, self.__qw2, self.__analyze_indexes)
        plotter.plot_x_axis_is_t(plot_t_list=[50, 100, 200])


if __name__ == '__main__':
    indexes = [10, 50, 100]
    analyzer = SimulationResultAnalyzer(qw1=GroverWalk2D(),
                                        qw2=EraseElectricGroverWalk2DAlongX(erase_t_list=indexes),
                                        analyze_indexes=indexes,
                                        options={"parallel": True})
    # analyzer.analyze()
    analyzer.plot()
