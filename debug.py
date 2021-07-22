from exp_setting.exp import *
from config.config import *
import joblib
import glob


def check_simulation_data(obj_a, obj_b):
    """
    Example:
    obj_a=[exp_name, exp_index]
    obj_b=[exp_name, exp_index]
    obj_aとobj_bのシミュレーションデータが完全に一致するかチェックします
    :param obj_a:env使わない方。古い方
    :param obj_b:
    :return:
    """
    exp_index_a_list = obj_a[0]
    exp_name_a = obj_a[1]

    exp_index_b_list = obj_b[0]
    exp_name_b = obj_b[1]

    for k in range(len(exp_index_b_list)):
        # データをロードする
        # exp_nameにある全実験フォルダーへのpath。sortもする。
        simulation_data_file_names_a = glob.glob(
            f"{config_simulation_data_save_path(exp_name_a, exp_index_a_list[k])}/*.jb")
        simulation_data_file_names_a.sort()  # 実験順にsortする。

        simulation_data_file_names_b = glob.glob(
            f"{config_simulation_data_save_path(exp_name_b, exp_index_b_list[k])}/*.jb")
        simulation_data_file_names_b.sort()  # 実験順にsortする。
        T = len(simulation_data_file_names_a) - 1
        for t in range(T + 1):
            psy_a_obj = joblib.load(simulation_data_file_names_a[t])
            psy_a = psy_a_obj["シミュレーションデータ"]
            psy_b = joblib.load(simulation_data_file_names_b[t])
            # 各成分をチェックする
            for x in range(2 * T + 1):
                for y in range(2 * T + 1):
                    for i in range(4):
                        right = psy_a[x, y, i]
                        test = psy_b[x, y, i]
                        if right != test:
                            print_warning(f"異なる：t={t}：x={x}：y={y}：right - test={right - test}")
            print_green_text(f"t={t}回目終わり")
        print_green_text(f"k={k}回目終わり")


if __name__ == '__main__':
    select_exp_index = list(range(10, 21))
    _, exp_name = exp_016_01_00_x_set_debug(select_exp_index)
    _, exp_name2 = exp_016_01_00_x_set(1, 21)
    check_simulation_data([select_exp_index, exp_name], [select_exp_index, exp_name2])
