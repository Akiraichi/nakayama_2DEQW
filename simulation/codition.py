import numpy as np
from config.config import Config_simulation


class Condition:
    def __init__(self):
        self.T = None
        self.P = None
        self.Q = None
        self.R = None
        self.S = None
        self.PSY_init = None
        self.algorithm = None
        self.phi = None
        self.phi_latex = None
        self.exp_name = None
        self.exp_index = None
    # def set(self, exp):
    #     self.PSY_init = exp.PSY_init
    #     self.T = exp.T
    #     self.P = exp.P
    #     self.Q = exp.Q
    #     self.R = exp.R
    #     self.S = exp.S


def set_basic_condition(condition):
    # シミュレーション条件
    condition.PSY_init = None
    condition.T = Config_simulation.max_time_step  # 最大時間発展T
    condition.P = np.array([[-1 / 2, 1 / 2, 1 / 2, 1 / 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                           dtype=np.complex128)
    condition.Q = np.array([[0, 0, 0, 0], [1 / 2, -1 / 2, 1 / 2, 1 / 2], [0, 0, 0, 0], [0, 0, 0, 0]],
                           dtype=np.complex128)
    condition.R = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [1 / 2, 1 / 2, -1 / 2, 1 / 2], [0, 0, 0, 0]],
                           dtype=np.complex128)
    condition.S = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1 / 2, 1 / 2, 1 / 2, -1 / 2]],
                           dtype=np.complex128)
