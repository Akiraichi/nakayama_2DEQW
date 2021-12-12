import numpy as np
from config.config import ConfigSimulation


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
        # numbaでコンパイルする際に、型をi8にしているので、初期値は0とする。
        self.erase_t = 0
        # 電場をどの程度ゆっくり消すか
        self.erase_time_step = 0


def set_grover_condition(condition):
    # シミュレーション条件
    condition.PSY_init = None
    condition.T = ConfigSimulation.MaxTimeStep  # 最大時間発展T
    condition.P = np.array([[-1 / 2, 1 / 2, 1 / 2, 1 / 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                           dtype=np.complex128)
    condition.Q = np.array([[0, 0, 0, 0], [1 / 2, -1 / 2, 1 / 2, 1 / 2], [0, 0, 0, 0], [0, 0, 0, 0]],
                           dtype=np.complex128)
    condition.R = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [1 / 2, 1 / 2, -1 / 2, 1 / 2], [0, 0, 0, 0]],
                           dtype=np.complex128)
    condition.S = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1 / 2, 1 / 2, 1 / 2, -1 / 2]],
                           dtype=np.complex128)


def set_hadamard_condition(condition):
    # シミュレーション条件
    condition.PSY_init = None
    condition.T = ConfigSimulation.MaxTimeStep  # 最大時間発展T
    condition.P = np.array([[1 / 2, 1 / 2, 1 / 2, 1 / 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                           dtype=np.complex128)
    condition.Q = np.array([[0, 0, 0, 0], [1 / 2, -1 / 2, 1 / 2, -1 / 2], [0, 0, 0, 0], [0, 0, 0, 0]],
                           dtype=np.complex128)
    condition.R = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [1 / 2, 1 / 2, -1 / 2, -1 / 2], [0, 0, 0, 0]],
                           dtype=np.complex128)
    condition.S = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1 / 2, -1 / 2, -1 / 2, 1 / 2]],
                           dtype=np.complex128)


def set_DFT_condition(condition):
    # シミュレーション条件
    condition.PSY_init = None
    condition.T = ConfigSimulation.MaxTimeStep  # 最大時間発展T
    condition.P = np.array([[1 / 2, 1 / 2, 1 / 2, 1 / 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                           dtype=np.complex128)
    condition.Q = np.array([[0, 0, 0, 0], [1 / 2, 1j / 2, -1 / 2, -1j / 2], [0, 0, 0, 0], [0, 0, 0, 0]],
                           dtype=np.complex128)
    condition.R = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [1 / 2, -1 / 2, 1 / 2, -1 / 2], [0, 0, 0, 0]],
                           dtype=np.complex128)
    condition.S = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1 / 2, -1j / 2, -1 / 2, 1j / 2]],
                           dtype=np.complex128)
