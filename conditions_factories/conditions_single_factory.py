from conditions_factories.conditions_base_factory import ConditionsBaseFactory
from helper import helper
from simulation.condition import ConditionNew, ConditionType
import sys


class ConditionsSingleFactory(ConditionsBaseFactory):
    """
    erase_tのみを変えた場合のconditionを生成するクラス
    """

    def __init__(self):
        pass

    @staticmethod
    def single_001_HadamardWalk2D():
        exp_name = sys._getframe().f_code.co_name
        conditions = []
        phi = helper.return_phi(num=0)
        c = ConditionNew.prepare(pattern=ConditionType.Hadamard, options={"exp_name": exp_name,
                                                                          "algorithm": 2,
                                                                          "exp_index": 0,
                                                                          "phi": phi})
        conditions.append(c)

        return conditions

    @staticmethod
    def single_002_ElectricHadamardWalk2DAlongX():
        exp_name = sys._getframe().f_code.co_name
        conditions = []
        phi = helper.return_phi(num=4)
        c = ConditionNew.prepare(pattern=ConditionType.Hadamard, options={"exp_name": exp_name,
                                                                          "algorithm": 3,
                                                                          "exp_index": 0,
                                                                          "phi": phi})
        conditions.append(c)

        return conditions

    @staticmethod
    def single_003_ElectricHadamardWalk2DAlongXY():
        exp_name = sys._getframe().f_code.co_name
        conditions = []
        phi = helper.return_phi(num=4)
        c = ConditionNew.prepare(pattern=ConditionType.Hadamard, options={"exp_name": exp_name,
                                                                          "algorithm": 5,
                                                                          "exp_index": 0,
                                                                          "phi": phi})
        conditions.append(c)

        return conditions

    @staticmethod
    def single_004_DFTWalk2D():
        exp_name = sys._getframe().f_code.co_name
        conditions = []
        phi = helper.return_phi(num=0)
        c = ConditionNew.prepare(pattern=ConditionType.DFT, options={"exp_name": exp_name,
                                                                     "algorithm": 2,
                                                                     "exp_index": 0,
                                                                     "phi": phi})
        conditions.append(c)

        return conditions

    @staticmethod
    def single_005_ElectricDFTWalk2DAlongX():
        exp_name = sys._getframe().f_code.co_name
        conditions = []
        phi = helper.return_phi(num=4)
        c = ConditionNew.prepare(pattern=ConditionType.DFT, options={"exp_name": exp_name,
                                                                     "algorithm": 3,
                                                                     "exp_index": 0,
                                                                     "phi": phi})
        conditions.append(c)

        return conditions

    @staticmethod
    def single_006_ElectricDFTWalk2DAlongXY():
        exp_name = sys._getframe().f_code.co_name
        conditions = []
        phi = helper.return_phi(num=4)
        c = ConditionNew.prepare(pattern=ConditionType.DFT, options={"exp_name": exp_name,
                                                                     "algorithm": 5,
                                                                     "exp_index": 0,
                                                                     "phi": phi})
        conditions.append(c)

        return conditions

    @staticmethod
    def single_007_GroverWalk2D():
        exp_name = sys._getframe().f_code.co_name
        conditions = []
        phi = helper.return_phi(num=0)
        c = ConditionNew.prepare(pattern=ConditionType.Grover, options={"exp_name": exp_name,
                                                                        "algorithm": 2,
                                                                        "exp_index": 0,
                                                                        "phi": phi})
        conditions.append(c)

        return conditions

    @staticmethod
    def single_008_ElectricGroverWalk2DAlongX():
        exp_name = sys._getframe().f_code.co_name
        conditions = []
        phi = helper.return_phi(num=4)
        c = ConditionNew.prepare(pattern=ConditionType.Grover, options={"exp_name": exp_name,
                                                                        "algorithm": 3,
                                                                        "exp_index": 0,
                                                                        "phi": phi})
        conditions.append(c)

        return conditions

    @staticmethod
    def single_009_ElectricGroverWalk2DAlongXY():
        exp_name = sys._getframe().f_code.co_name
        conditions = []
        phi = helper.return_phi(num=4)
        c = ConditionNew.prepare(pattern=ConditionType.Grover, options={"exp_name": exp_name,
                                                                        "algorithm": 5,
                                                                        "exp_index": 0,
                                                                        "phi": phi})
        conditions.append(c)

        return conditions


if __name__ == '__main__':
    pass
