import glob
import sympy

import joblib
import zlib
from config.config import ConfigSimulation, config_simulation_data_save_path, print_warning
from simulation.simulation_core import calc_probability


def return_simulation_data_file_names(exp_name, exp_index):
    """
    GoogleDriveで、うまく動作するように、チェック処理を追加している。
    return: exp_nameのplot_exp_index以下にある全jbファイルのパスのリストを返却する。この際、
    max_time_stepとファイル数を比較することで全て抽出できているかをチェックする
    """
    count = 0
    while True:
        simulation_data_file_names = glob.glob(
            f"{config_simulation_data_save_path(exp_name=exp_name, str_t=None, index=exp_index)}**/*.jb")
        simulation_data_file_names.sort()  # 実験順にsortする。
        if len(simulation_data_file_names) == ConfigSimulation.MaxTimeStep + 1:
            # シミュレーションデータ全てのpathをgrobできているかのチェック
            break
        count += 1
        if count == 3:
            # そもそもデータがない可能性がある
            print_warning("データがありません！")
            raise OSError
    return simulation_data_file_names


def load_data_by_error_handling(file_path):
    while True:
        try:
            data = joblib.load(file_path)
        except zlib.error as e:
            print_warning(e)
            import time
            time.sleep(60)
        except OSError as e:
            print_warning(e)
            import time
            time.sleep(60)
        else:
            break
    return data


def return_phi(num):
    """

    Args:
        num: xに代入する数値

    Returns: xにnumを代入した結果。phi = num*π/240

    """
    x = sympy.Symbol('x')
    phi = x * sympy.pi / 240
    phi = phi.subs(x, num)
    phi = float(phi.evalf())
    return phi


def save_jb_file(data_dict, folder_path, file_path):
    save_path = f"{folder_path}/{file_path}"
    joblib.dump(data_dict, save_path, compress=3)


def get_probability(simulation_data_file_names, index):
    save_data_object = load_data_by_error_handling(simulation_data_file_names[index])
    # save_data_object = joblib.load(simulation_data_file_names[index])
    condition = save_data_object["実験条件データ（condition）"]

    # エラーチェック
    if index != int(save_data_object["このシミュレーションデータが何ステップ目か（t）"]):
        print_warning("実験データをチェックしてください")

    T = condition.T
    len_x = 2 * T + 1
    len_y = 2 * T + 1
    PSY = save_data_object["シミュレーションデータ"]

    # probability[x,y]として(x,y)座標の確率を求められる。
    probability = calc_probability(PSY, len_x, len_y)
    return probability
