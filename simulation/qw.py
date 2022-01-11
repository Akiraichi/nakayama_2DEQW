from simulation.conditions_factories.conditions_erase_t_factory import ConditionsEraseTFactory
from simulation.conditions_factories.conditions_single_factory import ConditionsSingleFactory
from simulation.simulation import SimulationQWAgent


class MaxTimeError(Exception):
    pass


class QW:
    def __init__(self, conditions):
        self.__conditions = conditions

    def simulate(self, start_step_t=0):
        simulation = SimulationQWAgent(conditions=self.__conditions, start_step_t=start_step_t)
        simulation.start_parallel_processing()

    @property
    def conditions(self):
        return self.__conditions


class GroverWalk2D(QW):
    def __init__(self):
        super().__init__(conditions=ConditionsSingleFactory.single_007_GroverWalk2D())


class ElectricGroverWalk2DAlongX(QW):
    def __init__(self):
        super().__init__(conditions=ConditionsSingleFactory.single_008_ElectricGroverWalk2DAlongX())


class ElectricGroverWalk2DAlongXY(QW):
    def __init__(self):
        super().__init__(conditions=ConditionsSingleFactory.single_009_ElectricGroverWalk2DAlongXY())


class EraseElectricGroverWalk2DAlongX(QW):
    def __init__(self, erase_t_list):
        super().__init__(
            conditions=ConditionsEraseTFactory.EraseT_005_EraseElectricGroverWalk2DAlongX(erase_t_list=erase_t_list))


class EraseElectricGroverWalk2DAlongXY(QW):
    def __init__(self, erase_t_list):
        super().__init__(
            conditions=ConditionsEraseTFactory.EraseT_006_EraseElectricGroverWalk2DAlongXY(erase_t_list=erase_t_list))


class HadamardWalk2D(QW):
    def __init__(self):
        super().__init__(conditions=ConditionsSingleFactory.single_001_HadamardWalk2D())


class ElectricHadamardWalk2DAlongX(QW):
    def __init__(self):
        super().__init__(conditions=ConditionsSingleFactory.single_002_ElectricHadamardWalk2DAlongX())


class ElectricHadamardWalk2DAlongXY(QW):
    def __init__(self):
        super().__init__(conditions=ConditionsSingleFactory.single_003_ElectricHadamardWalk2DAlongXY())


class EraseElectricHadamardWalk2DAlongX(QW):
    def __init__(self, erase_t_list):
        super().__init__(
            conditions=ConditionsEraseTFactory.EraseT_001_EraseElectricHadamardWalk2DAlongX(erase_t_list=erase_t_list))


class EraseElectricHadamardWalk2DAlongXY(QW):
    def __init__(self, erase_t_list):
        super().__init__(
            conditions=ConditionsEraseTFactory.EraseT_002_EraseElectricHadamardWalk2DAlongXY(erase_t_list=erase_t_list))


class DFTWalk2D(QW):
    def __init__(self):
        super().__init__(conditions=ConditionsSingleFactory.single_004_DFTWalk2D())


class ElectricDFTWalk2DAlongX(QW):
    def __init__(self):
        super().__init__(conditions=ConditionsSingleFactory.single_005_ElectricDFTWalk2DAlongX())


class ElectricDFTWalk2DAlongXY(QW):
    def __init__(self):
        super().__init__(conditions=ConditionsSingleFactory.single_006_ElectricDFTWalk2DAlongXY())


class EraseElectricDFTWalk2DAlongX(QW):
    def __init__(self, erase_t_list):
        super().__init__(
            conditions=ConditionsEraseTFactory.EraseT_003_EraseElectricDFTWalk2DAlongX(erase_t_list=erase_t_list))


class EraseElectricDFTWalk2DAlongXY(QW):
    def __init__(self, erase_t_list):
        super().__init__(
            conditions=ConditionsEraseTFactory.EraseT_004_EraseElectricDFTWalk2DAlongXY(erase_t_list=erase_t_list))
