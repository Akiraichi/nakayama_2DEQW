import glob
import sympy
import joblib
import zlib
import termcolor

from config.config_simulation import ConfigSimulationSetting, config_simulation_data_save_path
from simulator.simulation_algorithm import calc_probability


def return_simulation_data_file_names(exp_name, exp_index):
    """
    GoogleDriveで、うまく動作するように、チェック処理を追加している。
    return: exp_nameのexp_index以下にある全jbファイルのパスのリストを返却する。この際、
    max_time_stepとファイル数を比較することで全て抽出できているかをチェックする
    """
    count = 0
    while True:
        simulation_data_file_names = glob.glob(
            f"{config_simulation_data_save_path(exp_name=exp_name, str_t=None, index=exp_index)}**/*.jb")
        simulation_data_file_names.sort()  # 実験順にsortする。
        if len(simulation_data_file_names) == ConfigSimulationSetting.MaxTimeStep + 1:
            # シミュレーションデータ全てのpathをgrobできているかのチェック
            break
        count += 1
        if count == 3:
            # そもそもデータがない可能性がある
            print_warning("データがありません！")
            print(f"データへのパス：{config_simulation_data_save_path(exp_name=exp_name, str_t=None, index=exp_index)}")
            raise OSError
    return simulation_data_file_names


def load_file_by_error_handling(file_path):
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


def save_jb_file(data_dict, path_to_file, file_name):
    save_path = f"{path_to_file}/{file_name}"
    joblib.dump(data_dict, save_path, compress=3)


def get_probability(simulation_data_file_names, index):
    save_data_object = load_file_by_error_handling(simulation_data_file_names[index])
    # save_data_object = joblib.load(simulation_data_file_names[index])
    condition = save_data_object["実験条件データ（condition）"]

    # エラーチェック
    if index != int(save_data_object["このシミュレーションデータが何ステップ目か（t）"]):
        print_warning("実験データをチェックしてください")
        print(f"実験データのパス：{simulation_data_file_names[index]}")
    T = condition.T

    len_x = 2 * T + 1
    len_y = 2 * T + 1
    PSY = save_data_object["シミュレーションデータ"]

    # probability[x,y]として(x,y)座標の確率を求められる。
    probability = calc_probability(PSY, len_x, len_y)
    return probability


def check_finished_file(folder_path: str, will_generate_index_list: list, extension: str):
    """
    処理が完了しているかを確認し、処理できていないファイルのみ処理する。
    """
    # すでに生成されたファイルのファイル名の一覧を取得する
    generated_file_names = glob.glob(f"{folder_path}/*.{extension}")

    # すでに生成されたファイルのindexの一覧を求める
    generated_index_list = [extract_index_from_file_name(generated_file_name, extension) for generated_file_name in
                            generated_file_names]

    # 共通しない要素のうち、まだ処理されていないものを取得
    not_generated_index_list = set(will_generate_index_list) - set(generated_index_list)

    # 実行状況に応じて、状況を報告
    if not_generated_index_list:
        for not_generated_index in not_generated_index_list:
            print_warning(f"index={not_generated_index}：完了していません")
    else:
        for generated_index in generated_index_list:
            print_green_text(f"index={generated_index}：既に完了")

    return not_generated_index_list


def extract_index_from_file_name(file_name, extension):
    """
    abcde_0000.jbのようなファイルにおいて、0000を抽出する
    Args:
        file_name: file名
        extension: fileの拡張子

    Returns:

    """
    len_extension = len(extension)  # 拡張子の文字数
    len_index = 4  # example 0000.jb の場合indexは4文字
    index = int(file_name[-(len_extension + 1 + len_index):-(len_extension + 1)])
    return index


def print_warning(text):
    warning = '*' * 30 + '\n'
    warning += '*{:^28}*\n'.format('Warning')
    warning += '*' * 30 + '\n'
    colored_warning = termcolor.colored(warning, 'red')
    print(colored_warning)
    print(termcolor.colored(text, 'red'))


def print_finish(text):
    notice = '-' * 30 + '\n'
    notice += '|{:^28}|\n'.format(f'Finish：{text}')
    notice += '-' * 30 + '\n'
    colored_warning = termcolor.colored(notice, 'green')
    print(colored_warning)


def print_green_text(text):
    colored_text = termcolor.colored(text, 'green')
    print(colored_text)


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


def select_plot_t_step():
    # どのデータ抽出するかを選択する
    t_list = None
    if ConfigSimulationSetting.MaxTimeStep == 2000:
        t_list = list(range(0, 2020, 20))
    elif ConfigSimulationSetting.MaxTimeStep == 600:
        t_list = list(range(0, 605, 5))
    elif ConfigSimulationSetting.MaxTimeStep == 200:
        t_list = list(range(0, 205, 5))
    elif ConfigSimulationSetting.MaxTimeStep == 100:
        t_list = list(range(0, 105, 5))
    return t_list


def select_plot_t_step_detail():
    # どのデータ抽出するかを選択する
    t_list = None
    if ConfigSimulationSetting.MaxTimeStep == 2000:
        t_list = list(range(0, 2005, 5))
    elif ConfigSimulationSetting.MaxTimeStep == 600:
        t_list = list(range(0, 605, 5))
    elif ConfigSimulationSetting.MaxTimeStep == 200:
        t_list = list(range(0, 205, 5))
    elif ConfigSimulationSetting.MaxTimeStep == 100:
        t_list = list(range(0, 105, 5))
    return t_list


def select_plot_t_step_by_100():
    # どのデータ抽出するかを選択する
    t_list = None
    if ConfigSimulationSetting.MaxTimeStep == 2000:
        t_list = list(range(0, 2100, 100))
    elif ConfigSimulationSetting.MaxTimeStep == 600:
        t_list = [100, 200, 300, 400, 500, 600]
    elif ConfigSimulationSetting.MaxTimeStep == 200:
        t_list = list(range(0, 205, 5))
    elif ConfigSimulationSetting.MaxTimeStep == 100:
        t_list = list(range(0, 105, 5))
    return t_list
