import dataclasses

import numpy as np
from config.config_simulation import ConfigSimulationSetting
from helper.helper import print_warning
import sympy
from dataclasses import dataclass, asdict


class Condition:
    """旧形式"""

    def __init__(self):
        self.T = None
        # self.P = None
        # self.Q = None
        # self.R = None
        # self.S = None
        # self.PSY_init = None
        # self.algorithm = None
        # self.phi = None
        self.phi_latex = None
        self.exp_name = None
        self.exp_index = None
        # numbaでコンパイルする際に、型をi8にしているので、初期値は0とする。
        self.erase_t = 0
        # 電場をどの程度ゆっくり消すか
        # self.erase_time_step = 0


@dataclass(frozen=True)
class ConditionNew:
    T: int
    algorithm: int
    phi: float
    phi_latex: str
    exp_name: str
    exp_index: int
    erase_t: int
    erase_time_step: int
    P: np.ndarray
    Q: np.ndarray
    R: np.ndarray
    S: np.ndarray
    PSY_init: np.ndarray

    def __post_init__(self):
        object.__setattr__(self, "phi_latex", sympy.latex(self.phi))
        print(f"t = {self.erase_t}")  # erase_tの中身を確認するため

    @classmethod
    def prepare(cls, pattern, options=None):
        """

        Args:
            pattern: ConditionType から一つ指定する
            options: プロパティの上書きしたいものを指定する

        Returns: Condition Instanceを返す

        """
        if options is None:
            options = {}
        if pattern == ConditionType.Grover:
            _obj = DefaultGroverProps()
        elif pattern == ConditionType.Hadamard:
            _obj = DefaultHadamardProps()
        elif pattern == ConditionType.DFT:
            _obj = DefaultDFTProps()
        else:
            print_warning("Conditionの設定がおかしいですよ！")
            raise OSError
        _obj = dataclasses.replace(_obj, **options)  # optionで設定された内容に上書きする
        return cls(**asdict(_obj))


@dataclass(frozen=True)
class ConditionType:
    Grover: str = "Grover"
    Hadamard: str = "Hadamard"
    DFT: str = "DFT"


@dataclass(frozen=True)
class DefaultBaseProps:
    T: int = ConfigSimulationSetting.MaxTimeStep
    algorithm: int = None
    phi: float = None
    phi_latex: str = None  # phiをlatex表記したもの
    exp_name: str = None
    exp_index: int = None
    # numbaでコンパイルする際に、型をi8にしているので、初期値は0とする。
    erase_t: int = 0
    # 電場をどの程度ゆっくり消すか
    erase_time_step: int = 0


@dataclass(frozen=True)
class DefaultGroverProps(DefaultBaseProps):
    P: np.ndarray = np.array([
        [-1 / 2, 1 / 2, 1 / 2, 1 / 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]], dtype=np.complex128)
    Q: np.ndarray = np.array([
        [0, 0, 0, 0],
        [1 / 2, -1 / 2, 1 / 2, 1 / 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0]], dtype=np.complex128)
    R: np.ndarray = np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1 / 2, 1 / 2, -1 / 2, 1 / 2],
        [0, 0, 0, 0]], dtype=np.complex128)
    S: np.ndarray = np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1 / 2, 1 / 2, 1 / 2, -1 / 2]], dtype=np.complex128)
    PSY_init: np.ndarray = 1 / 2 * np.array([1, 1, -1, -1])


@dataclass(frozen=True)
class DefaultHadamardProps(DefaultBaseProps):
    P: np.ndarray = np.array([
        [1 / 2, 1 / 2, 1 / 2, 1 / 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]], dtype=np.complex128)
    Q: np.ndarray = np.array([
        [0, 0, 0, 0],
        [1 / 2, -1 / 2, 1 / 2, -1 / 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0]], dtype=np.complex128)
    R: np.ndarray = np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1 / 2, -1 / 2, -1 / 2, 1 / 2],
        [0, 0, 0, 0]], dtype=np.complex128)
    S: np.ndarray = np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1 / 2, 1 / 2, -1 / 2, -1 / 2]], dtype=np.complex128)
    PSY_init: np.ndarray = 1 / 2 * np.array([1, -1, 1j, 1j])


@dataclass(frozen=True)
class DefaultDFTProps(DefaultBaseProps):
    P: np.ndarray = np.array([
        [1 / 2, 1 / 2, 1 / 2, 1 / 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]], dtype=np.complex128)
    Q: np.ndarray = np.array([
        [0, 0, 0, 0],
        [1 / 2, -1j / 2, -1 / 2, 1j / 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0]], dtype=np.complex128)
    R: np.ndarray = np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1 / 2, -1 / 2, 1 / 2, -1 / 2],
        [0, 0, 0, 0]], dtype=np.complex128)
    S: np.ndarray = np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1 / 2, 1j / 2, -1 / 2, -1j / 2]], dtype=np.complex128)
    PSY_init: np.ndarray = 1 / 2 * np.array([1, -1, 1j, 1j])


if __name__ == '__main__':
    c = ConditionNew.prepare(pattern=ConditionType.Grover, options={"phi": 49})
    print(type(c))
