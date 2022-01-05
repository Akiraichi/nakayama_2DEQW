import numpy as np
from config.config import ConfigSimulation, print_warning
import sympy


class ConditionNew:
    def __init__(self, **params):
        self.__params = params
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
            return cls(**{**DefaultGroverProps, **options})  # https://note.nkmk.me/python-dict-add-update/
        elif pattern == ConditionType.Hadamard:
            return cls(**{**DefaultHadamardProps, **options})
        elif pattern == ConditionType.DFT:
            return cls(**{**DefaultDFTProps, **options})
        else:
            print_warning("Conditionの設定がおかしいですよ！")
            raise OSError

    @property
    def T(self):
        return self.__params["T"]

    @property
    def P(self):
        return self.__params["P"]

    @property
    def Q(self):
        return self.__params["Q"]

    @property
    def R(self):
        return self.__params["R"]

    @property
    def S(self):
        return self.__params["S"]

    @property
    def PSY_init(self):
        return self.__params["PSY_init"]

    @property
    def algorithm(self):
        return self.__params["algorithm"]

    @property
    def phi(self):
        return self.__params["phi"]

    @property
    def phi_latex(self):
        return sympy.latex(self.__params["phi"])

    @property
    def exp_name(self):
        return self.__params["exp_name"]

    @property
    def exp_index(self):
        return self.__params["exp_index"]

    @property
    def erase_t(self):
        return self.__params["erase_t"]

    @property
    def erase_time_step(self):
        return self.__params["erase_time_step"]


class ConditionType:
    Grover = "Grover"
    Hadamard = "Hadamard"
    DFT = "DFT"


DefaultBaseProps = {
    "T": ConfigSimulation.MaxTimeStep,
    "algorithm": None,
    "phi": None,
    "exp_name": None,
    "exp_index": None,
    # numbaでコンパイルする際に、型をi8にしているので、初期値は0とする。
    "erase_t": 0,
    # 電場をどの程度ゆっくり消すか
    "erase_time_step": 0
}

DefaultGroverProps = {
    **DefaultBaseProps,
    "P": np.array([
        [-1 / 2, 1 / 2, 1 / 2, 1 / 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ], dtype=np.complex128),
    "Q": np.array([
        [0, 0, 0, 0],
        [1 / 2, -1 / 2, 1 / 2, 1 / 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ], dtype=np.complex128),
    "R": np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1 / 2, 1 / 2, -1 / 2, 1 / 2],
        [0, 0, 0, 0]
    ], dtype=np.complex128),
    "S": np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1 / 2, 1 / 2, 1 / 2, -1 / 2]
    ], dtype=np.complex128),
    "PSY_init": 1 / 2 * np.array([1, 1, -1, -1])
}

DefaultHadamardProps = {
    **DefaultBaseProps,
    "P": np.array([
        [1 / 2, 1 / 2, 1 / 2, 1 / 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ], dtype=np.complex128),
    "Q": np.array([
        [0, 0, 0, 0],
        [1 / 2, -1 / 2, 1 / 2, -1 / 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ], dtype=np.complex128),
    "R": np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1 / 2, -1 / 2, -1 / 2, 1 / 2],
        [0, 0, 0, 0]
    ], dtype=np.complex128),
    "S": np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1 / 2, 1 / 2, -1 / 2, -1 / 2]
    ], dtype=np.complex128),
    "PSY_init": 1 / 2 * np.array([1, -1, 1j, 1j])
}

DefaultDFTProps = {
    **DefaultBaseProps,
    "P": np.array([
        [1 / 2, 1 / 2, 1 / 2, 1 / 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ], dtype=np.complex128),
    "Q": np.array([
        [0, 0, 0, 0],
        [1 / 2, -1j / 2, -1 / 2, 1j / 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ], dtype=np.complex128),
    "R": np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1 / 2, -1 / 2, 1 / 2, -1 / 2],
        [0, 0, 0, 0]
    ], dtype=np.complex128),
    "S": np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1 / 2, 1j / 2, -1 / 2, -1j / 2]
    ], dtype=np.complex128),
    "PSY_init": 1 / 2 * np.array([1, -1, 1j, 1j])
}

if __name__ == '__main__':
    c = ConditionNew.prepare(pattern=ConditionType.Grover, options={"phi": 49})
    print(type(c))
