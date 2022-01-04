from conditions_factories.conditions_erase_t_factory import ConditionsEraseTFactory
from conditions_factories.conditions_single_factory import ConditionsSingleFactory
from qw import EraseElectricGroverWalk2DAlongX
from simulation_result_plotter import SimulationResultPlotter

if __name__ == '__main__':
    """シミュレーション"""
    # qw = GroverWalk2D()
    # qw = EraseElectricGroverWalk2DAlongX(erase_t_list=[10, 50, 100])
    #
    # qw.simulate(start_step_t=0)

    """データの解析"""
    indexes = [10, 50, 100]
    plotter = SimulationResultPlotter(
        conditions=ConditionsEraseTFactory.EraseT_005_EraseElectricGroverWalk2DAlongX(erase_t_list=indexes),
        save_path_indexes=indexes, options={"parallel": False})

    # plotter = SimulationResultPlotter(conditions=ConditionsSingleFactory.single_007_GroverWalk2D())
    plotter.plot_surface()
