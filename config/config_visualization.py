import os
from dataclasses import dataclass, field

from helper import helper


def plot_save_path(exp_name, plot_type, index=None):
    # 実験データの保存先のフォルダーがなければ作成する
    if index is None:
        path = f"result/{exp_name}/{plot_type}_{exp_name}"
    else:
        # index=実験した時の順番でつけた番号。0埋めする
        index = str(index).zfill(2)
        path = f"result/{exp_name}/{plot_type}_{exp_name}/{index}"
    os.makedirs(path, exist_ok=True)
    return path


@dataclass(frozen=True)
class DefaultPlotSetting:
    # プロットに関する共通設定を記入する。
    plot_type: str  # surfaceかheatmapかを指定
    conditions: list  # プロットしたい実験条件をリストで指定する
    save_path_indexes: list = field(default_factory=[0])  # TODO:これなんだっけ？
    plot_t_list: list = field(default_factory=helper.select_plot_t_step_by_100)  # プロットしたいtをlistの形式で指定する
    is_enlarge: bool = False  # Trueにした場合、最大時間ステップまでの範囲でプロットする
    parallel: bool = True  # Trueにした場合、並列処理を行う

    def __post_init__(self):
        """パラメータが適切かどうかチェック"""
        if len(self.conditions) != len(self.save_path_indexes):
            helper.print_warning("conditionの数とsave_path_indexの数が一致していません")
            raise OSError
