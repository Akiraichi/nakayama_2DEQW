import sys

from simulation.conditions_factories.conditions_base_factory import ConditionsBaseFactory
from helper import helper
from simulation.condition import ConditionNew, ConditionType


class ConditionsEraseTFactory(ConditionsBaseFactory):
    """
    erase_tのみを変えた場合のconditionを生成するクラス
    t=erase_tから通常の（電場のない）QWを開始する。
    例：erase_t=100
    ・・・
    t=99のEQWを実行して完了。
    t=100ではQWを実行して完了
    t=101ではQWを実行して完了
    ・・・
    t=TでQWを実行して終了。
    """

    def __init__(self):
        pass

    @staticmethod
    def EraseT_001_EraseElectricHadamardWalk2DAlongX(erase_t_list):
        exp_name = sys._getframe().f_code.co_name
        conditions = []
        phi = helper.return_phi(num=4)
        for erase_t in erase_t_list:
            c = ConditionNew.prepare(pattern=ConditionType.Hadamard, options={"exp_name": exp_name,
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
        phi = helper.return_phi(num=4)
        for erase_t in erase_t_list:
            c = ConditionNew.prepare(pattern=ConditionType.Hadamard, options={"exp_name": exp_name,
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
        phi = helper.return_phi(num=4)
        for erase_t in erase_t_list:
            c = ConditionNew.prepare(pattern=ConditionType.DFT, options={"exp_name": exp_name,
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
        phi = helper.return_phi(num=4)
        for erase_t in erase_t_list:
            c = ConditionNew.prepare(pattern=ConditionType.DFT, options={"exp_name": exp_name,
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
        phi = helper.return_phi(num=4)
        for erase_t in erase_t_list:
            c = ConditionNew.prepare(pattern=ConditionType.Grover, options={"exp_name": exp_name,
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
        phi = helper.return_phi(num=4)
        for erase_t in erase_t_list:
            c = ConditionNew.prepare(pattern=ConditionType.Grover, options={"exp_name": exp_name,
                                                                            "algorithm": 110,
                                                                            "exp_index": erase_t,
                                                                            "erase_t": erase_t,
                                                                            "phi": phi})
            conditions.append(c)
        return conditions
