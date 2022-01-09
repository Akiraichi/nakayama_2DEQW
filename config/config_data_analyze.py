import os
from dataclasses import InitVar, dataclass, field
from typing import List

from config.config_name import DefaultNameSetting
from helper import select_plot_t_step


@dataclass(frozen=True)
class AnalyzeNameSetting(DefaultNameSetting):
    file_index: int = 0  # file_name以外を使いたい時のためにデフォルト値を入れておく。
    folder_name: str = field(init=False)  # 保存する際のフォルダ名
    path_to_file: str = field(init=False)  # 保存する際のファイルまでのパス
    file_name: str = field(init=False)  # 保存する際のファイル名
    default_parent_folder_name: str = field(init=False, default="analyze")

    def __post_init__(self, exp1_name: str, exp1_index: int, exp2_name: str):
        super().__post_init__(exp1_name=exp1_name, exp1_index=exp1_index, exp2_name=exp2_name)
        object.__setattr__(self, "folder_name", self.default_folder_name)
        object.__setattr__(self, "path_to_file",
                           f"{self.default_top_folder_name}/{self.default_parent_folder_name}/{self.default_folder_name}")
        object.__setattr__(self, "file_name",
                           f"AnalyzeData_{self.default_file_name}_{str(self.file_index).zfill(4)}.jb")
        os.makedirs(self.path_to_file, exist_ok=True)


@dataclass(frozen=True)
class OptimizeNameSetting(DefaultNameSetting):
    """
    Optimizeに関する名前の設定を行うクラス
    """
    analyze_t: InitVar[int]  # 最適化処理を行なった時間ステップ
    file_index: InitVar[int] = 0  # ファイル名につけるindex
    folder_name: str = field(init=False)  # 保存する際のフォルダ名
    path_to_file: str = field(init=False)  # 保存する際のファイルまでのパス
    file_name: str = field(init=False)  # 保存する際のファイル名
    default_parent_folder_name: str = field(init=False, default="optimize")

    def __post_init__(self, exp1_name: str, exp1_index: int, exp2_name: str, analyze_t: int, file_index: int):
        super().__post_init__(exp1_name=exp1_name, exp1_index=exp1_index, exp2_name=exp2_name)
        object.__setattr__(self, "folder_name", self.default_folder_name)
        object.__setattr__(self, "path_to_file",
                           f"{self.default_top_folder_name}/{self.default_parent_folder_name}/{self.default_folder_name}")
        object.__setattr__(self, "file_name",
                           f"OptimizeData_{self.default_file_name}_{analyze_t}_{str(file_index).zfill(4)}.jb")
        os.makedirs(self.path_to_file, exist_ok=True)


@dataclass(frozen=True)
class DefaultAnalyzeSetting:
    parallel: bool = False  # 処理を並列化するかどうか。現状Falseのほうが高速
    t_list: List[int] = field(default_factory=select_plot_t_step)  # 解析を実行する時間ステップ
    enable_KL_divergence: bool = True  # KLダイバージェンスを求めるかどうか
    enable_L1_norm: bool = True  # L1ノルムを求めるかどうか（誤差の絶対値の和）
    enable_L2_norm: bool = True  # L2ノルムを求めるかどうか（二乗誤差の和）
    enable_correlation_coefficient: bool = True  # 相関係数を求めるかどうか


@dataclass(frozen=True)
class DefaultAnalyzeOptimizeSetting:
    parallel: bool = False  # 処理を並列化するかどうか。現状Falseのほうが高速
    t_list: List[int] = field(default_factory=select_plot_t_step)  # 解析を実行する時間ステップ
    analyze_t: int = 0
    enable_KL_divergence: bool = True  # KLダイバージェンスを求めるかどうか
    enable_L1_norm: bool = True  # L1ノルムを求めるかどうか（誤差の絶対値の和）
    enable_L2_norm: bool = True  # L2ノルムを求めるかどうか（二乗誤差の和）
    enable_correlation_coefficient: bool = True  # 相関係数を求めるかどうか


@dataclass
class DefaultOptimizePlotSetting:
    x_label: str
    y_label: str
    title: str
    x_axis_data_list: list
    y_axis_data_list: list
    path_to_file: str
    file_name: str
    analyze_t:int

    # @classmethod
    # def x_axis_is_index_prepare(cls, exp1_name, exp1_index, exp2_name, analyze_t, title, x_axis_data_list,
    #                             y_axis_data_list):
    #     x_label = "t_{erase}"
    #     y_label = "t"
    #     setting = OptimizeNameSetting(exp1_name=exp1_name, exp1_index=exp1_index,
    #                                   exp2_name=exp2_name, analyze_t=analyze_t)
    #     file_name = setting.file_name + "x_axis_is_index"
    #     return cls(x_label, y_label, title, x_axis_data_list, y_axis_data_list, setting.path_to_file, file_name)

    @classmethod
    def x_axis_is_rank_prepare(cls, exp1_name, exp1_index, exp2_name, analyze_t, title, x_axis_data_list,
                               y_axis_data_list):
        x_label = "rank"
        y_label = "t"
        setting = OptimizeNameSetting(exp1_name=exp1_name, exp1_index=exp1_index,
                                      exp2_name=exp2_name, analyze_t=analyze_t)
        file_name = setting.file_name + "x_axis_is_rank"
        return cls(x_label, y_label, title, x_axis_data_list, y_axis_data_list, setting.path_to_file, file_name)


@dataclass(frozen=True)
class DefaultOptimizeAnalysisPlotSetting:
    x_label: str
    y_label: str
    title: str
    x_axis_data_list: list
    y_axis_data_list: list
    path_to_file: str
    file_name: str


@dataclass
class DefaultAnalyzePlotSetting:
    x_label: str
    y_label: str
    legend_label: str
    plot_indexes: list
    path_to_file: str
    file_name: str
    x_axis: str
    start_t: int = 0  # 横軸がindexの場合は使用しないので0をデフォルト値として入れておく