import sys

from conditions_factories.conditions_base_factory import ConditionsBaseFactory
from helper import return_phi
from simulation.condition import Condition, ConditionType


class ConditionsEraseTFactory(ConditionsBaseFactory):
    """
    erase_tのみを変えた場合のconditionを生成するクラス
    """

    def __init__(self):
        pass

    @staticmethod
    def EraseT_001_EraseElectricHadamardWalk2DAlongX(erase_t_list):
        exp_name = sys._getframe().f_code.co_name
        conditions = []
        phi = return_phi(num=4)
        for erase_t in erase_t_list:
            c = Condition.prepare(pattern=ConditionType.Hadamard, options={"exp_name": exp_name,
                                                                           "algorithm": 100,
                                                                           "exp_index": erase_t,
                                                                           "erase_t": erase_t,
                                                                           "phi": phi})
            conditions.append(c)
        return conditions

    @staticmethod
    def EraseT_002_EraseElectricHadamardWalk2DAlongXY(erase_t_list):
        exp_name = sys._getframe().f_code.co_name
        conditions = []
        phi = return_phi(num=4)
        for erase_t in erase_t_list:
            c = Condition.prepare(pattern=ConditionType.Hadamard, options={"exp_name": exp_name,
                                                                           "algorithm": 110,
                                                                           "exp_index": erase_t,
                                                                           "erase_t": erase_t,
                                                                           "phi": phi})
            conditions.append(c)
        return conditions

    @staticmethod
    def EraseT_003_EraseElectricDFTWalk2DAlongX(erase_t_list):
        exp_name = sys._getframe().f_code.co_name
        conditions = []
        phi = return_phi(num=4)
        for erase_t in erase_t_list:
            c = Condition.prepare(pattern=ConditionType.Hadamard, options={"exp_name": exp_name,
                                                                           "algorithm": 100,
                                                                           "exp_index": erase_t,
                                                                           "erase_t": erase_t,
                                                                           "phi": phi})
            conditions.append(c)
        return conditions

    @staticmethod
    def EraseT_004_EraseElectricDFTWalk2DAlongXY(erase_t_list):
        exp_name = sys._getframe().f_code.co_name
        conditions = []
        phi = return_phi(num=4)
        for erase_t in erase_t_list:
            c = Condition.prepare(pattern=ConditionType.Hadamard, options={"exp_name": exp_name,
                                                                           "algorithm": 110,
                                                                           "exp_index": erase_t,
                                                                           "erase_t": erase_t,
                                                                           "phi": phi})
            conditions.append(c)
        return conditions

    @staticmethod
    def EraseT_005_EraseElectricGroverWalk2DAlongX(erase_t_list):
        exp_name = sys._getframe().f_code.co_name
        conditions = []
        phi = return_phi(num=4)
        for erase_t in erase_t_list:
            c = Condition.prepare(pattern=ConditionType.Grover, options={"exp_name": exp_name,
                                                                         "algorithm": 100,
                                                                         "exp_index": erase_t,
                                                                         "erase_t": erase_t,
                                                                         "phi": phi})
            conditions.append(c)
        return conditions

    @staticmethod
    def EraseT_006_EraseElectricGroverWalk2DAlongXY(erase_t_list):
        exp_name = sys._getframe().f_code.co_name
        conditions = []
        phi = return_phi(num=4)
        for erase_t in erase_t_list:
            c = Condition.prepare(pattern=ConditionType.Hadamard, options={"exp_name": exp_name,
                                                                           "algorithm": 110,
                                                                           "exp_index": erase_t,
                                                                           "erase_t": erase_t,
                                                                           "phi": phi})
            conditions.append(c)
        return conditions

