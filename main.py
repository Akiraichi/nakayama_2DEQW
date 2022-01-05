from conditions_factories.conditions_erase_t_factory import ConditionsEraseTFactory
from conditions_factories.conditions_single_factory import ConditionsSingleFactory
from qw import EraseElectricGroverWalk2DAlongX, GroverWalk2D
from simulation_result_analyzer_and_plotter import SimulationResultAnalyzer
from simulation_result_plotter import SimulationResultPlotter

if __name__ == '__main__':
    """シミュレーション"""
    # qw = GroverWalk2D()
    qw = EraseElectricGroverWalk2DAlongX(erase_t_list=[10, 50, 100])
    #
    qw.simulate(start_step_t=0)

    """データの可視化"""
    # indexes = [10, 50, 100]
    # plotter = SimulationResultPlotter(
    #     conditions=ConditionsEraseTFactory.EraseT_005_EraseElectricGroverWalk2DAlongX(erase_t_list=indexes),
    #     save_path_indexes=indexes, options={"parallel": False})

    # plotter = SimulationResultPlotter(conditions=ConditionsSingleFactory.single_007_GroverWalk2D())
    # plotter.plot_surface()

    """データの確率分布の類似度を求めてプロット"""
    indexes = [10, 50, 100]
    analyzer = SimulationResultAnalyzer(qw1=GroverWalk2D(),
                                        qw2=EraseElectricGroverWalk2DAlongX(erase_t_list=indexes),
                                        analyze_indexes=indexes,
                                        options={"parallel": True})
    # analyzer.analyze()
    t_list = [10, 20, 50, 100]
    analyzer.plot_x_axis_is_index(plot_t_list=t_list)
    plot_indexes = [50, 100]
    analyzer.plot_x_axis_is_t(plot_indexes=plot_indexes, start_t=50)
