import glob

from config.config import ConfigSimulation, config_simulation_data_save_path


def return_simulation_data_file_names(exp_name, exp_index):
    """
    GoogleDriveで、うまく動作するように、チェック処理を追加している。
    return: exp_nameのplot_exp_index以下にある全jbファイルのパスのリストを返却する。この際、
    max_time_stepとファイル数を比較することで全て抽出できているかをチェックする
    """
    while True:
        simulation_data_file_names = glob.glob(
            f"{config_simulation_data_save_path(exp_name=exp_name, str_t=None, index=exp_index)}**/*.jb")
        simulation_data_file_names.sort()  # 実験順にsortする。
        if len(simulation_data_file_names) == ConfigSimulation.MaxTimeStep + 1:
            # シミュレーションデータ全てのpathをgrobできているかのチェック
            break
