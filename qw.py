# simulation
from conditions_factories.conditions_erase_t_factory import ConditionsEraseTFactory
from conditions_factories.conditions_single_factory import ConditionsSingleFactory
from simulation.simulation import SimulationQWAgent


class MaxTimeError(Exception):
    pass


class QW:
    def __init__(self, conditions):
        self.__conditions = conditions

    def simulate(self, start_step_t=0):
        simulation = SimulationQWAgent(conditions=self.__conditions, start_step_t=start_step_t)
        simulation.start_parallel_processing()


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


# class SlowEraseEQW(QW):
#     """
#     ゆっくり電場を消す電場量子ウォーク
#     pi/60
#     電場をどのくらいゆっくり消すかによって、実験を変えるのか、電場をどのくらいゆっくり消すかは固定にさせて、
#     色々なパラメータで実験するのかを検討
#     """
#
#     def __init__(self, select_exp_indexes):
#         super().__init__(e1=exp_023, e2=exp_024, select_exp_indexes=select_exp_indexes)
#
#
# class SlowEraseEQW_erase_t_0(QW):
#     """
#     ゆっくり電場を消す電場量子ウォーク
#     pi/60
#     電場をどのくらいゆっくり消すか、電場を消す時間ステップ数を変更して実験する
#     t=0で電場を消し始める
#     """
#
#     def __init__(self, erase_time_steps):
#         super().__init__(e1=exp_025, e2=exp_026, select_exp_indexes=erase_time_steps)
#
#
# class SlowEraseEQW_erase_t_200(QW):
#     """
#     ゆっくり電場を消す電場量子ウォーク
#     pi/60
#     電場をどのくらいゆっくり消すか、電場を消す時間ステップ数を変更して実験する
#     t=200で電場を消し始める
#     """
#
#     def __init__(self, erase_time_steps):
#         super().__init__(e1=exp_027, e2=exp_028, select_exp_indexes=erase_time_steps)


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
