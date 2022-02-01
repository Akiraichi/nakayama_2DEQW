import os
import sys
from dataclasses import dataclass, field

from config.config_name import DefaultNameSetting


@dataclass(frozen=True)
class CloudSimulationSetting:
    # MaxTimeStep: int = 600
    MaxTimeStep: int = 1300
    SimulationParallelNum: int = 4
    PlotParallelNum: int = 4


@dataclass(frozen=True)
class Env:
    if 'google.colab' in sys.modules:
        ENV = "colab"
    else:
        ENV = "local"


@dataclass(frozen=True)
class LocalSimulationSetting:
    MaxTimeStep: int = 600
    # MaxTimeStep: int = 200
    SimulationParallelNum: int = 4
    PlotParallelNum: int = 4


@dataclass(frozen=True)
class ConfigSimulationSetting:
    if Env.ENV == "colab":
        # google colab環境
        MaxTimeStep: int = field(init=False, default=CloudSimulationSetting.MaxTimeStep)
        SimulationParallelNum: int = field(init=False, default=CloudSimulationSetting.SimulationParallelNum)
        PlotParallelNum: int = field(init=False, default=CloudSimulationSetting.PlotParallelNum)
    elif Env.ENV == "local":
        # local環境
        MaxTimeStep: int = field(init=False, default=LocalSimulationSetting.MaxTimeStep)
        SimulationParallelNum: int = field(init=False, default=LocalSimulationSetting.SimulationParallelNum)
        PlotParallelNum: int = field(init=False, default=LocalSimulationSetting.PlotParallelNum)
    else:
        print("環境設定を間違えています")
        raise OSError


def config_simulation_data_save_path(exp_name, str_t=None, index=None):
    # 実験データの保存先のフォルダーがなければ作成する
    name = DefaultNameSetting(exp1_name="", exp1_index=0, exp2_name="")
    top_folder = name.default_top_folder_name
    if index is None:
        path = f"{top_folder}/{exp_name}/simulation_data_{exp_name}/"
    elif str_t is None:
        index = str(index).zfill(2)
        path = f"{top_folder}/{exp_name}/simulation_data_{exp_name}/{index}/"
    else:
        # index=実験した時の順番でつけた番号。0埋めする
        index = str(index).zfill(2)
        path = f"{top_folder}/{exp_name}/simulation_data_{exp_name}/{index}/{str_t[:2]}/"
    os.makedirs(path, exist_ok=True)
    return path
