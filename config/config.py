import os
import termcolor
import sys


class ConfigSimulation:
    moduleList = sys.modules
    ENV_COLAB = False

    if 'google.colab' in moduleList:
        ENV_COLAB = True

    if ENV_COLAB:
        print("Execute in google_colab")
        # 実験条件の設定
        MaxTimeStep = 600  # 最大時間ステップ数
        # シミュレーションの並列数
        SimulationParallelNum = 4
        # plotの並列数
        PlotParallelNum = 4
    else:
        print("Execute in local")
        # 実験条件の設定
        MaxTimeStep = 200  # 最大時間ステップ数
        # シミュレーションの並列数
        SimulationParallelNum = 4
        # plotの並列数
        PlotParallelNum = 4


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


# 実験データの保存場所。タイムステップごとに分割
def config_simulation_data_save_path(exp_name, str_t=None, index=None):
    # 実験データの保存先のフォルダーがなければ作成する
    if index is None:
        path = f"result/{exp_name}/simulation_data_{exp_name}/"
    elif str_t is None:
        index = str(index).zfill(2)
        path = f"result/{exp_name}/simulation_data_{exp_name}/{index}/"
    else:
        # index=実験した時の順番でつけた番号。0埋めする
        index = str(index).zfill(2)
        path = f"result/{exp_name}/simulation_data_{exp_name}/{index}/{str_t[:2]}/"
    os.makedirs(path, exist_ok=True)
    return path


# 保存する実験環境データの名前
def config_simulation_data_name(index):
    # index=実験した時の順番でつけた番号。0埋めする
    index = str(index).zfill(2)
    return f"{index}_env.env"


# プロットの保存場所
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


class AnalyzeSetting:
    def __init__(self, exp1_name, exp1_index, exp2_name, exp2_index):
        self.__exp1_name = exp1_name
        self.__exp2_name = exp2_name
        self.__exp1_index = exp1_index
        self.__exp2_index = exp2_index

        self.__setting_save_folder_path()
        self.__setting_save_file_name()

    def __setting_save_folder_path(self):
        # 保存場所の設定
        self.__folder_name = f'{self.__exp1_name}_{self.__exp1_index}_{self.__exp2_name}'
        self.__folder_path = f"result/analyze/{self.__folder_name}"  # AnalyzeDataの保存場所
        os.makedirs(self.__folder_path, exist_ok=True)

    def __setting_save_file_name(self):
        # 保存ファイル名の設定
        str_exp2_index = str(self.__exp2_index).zfill(4)
        self.__file_name = f"AnalyzeData_{self.__folder_name}_{str_exp2_index}.jb"

    @property
    def folder_name(self):
        return self.__folder_name

    @property
    def folder_path(self):
        return self.__folder_path

    @property
    def file_name(self):
        return self.__file_name


# 確率の保存場所
def config_prob_save_path(folder_name):
    # 実験データの保存先のフォルダーがなければ作成する
    path = f"result/prob/{folder_name}"
    os.makedirs(path, exist_ok=True)
    return path


# 分散の保存場所
def config_var_save_path(folder_name):
    # 実験データの保存先のフォルダーがなければ作成する
    path = f"result/var/{folder_name}"
    os.makedirs(path, exist_ok=True)
    return path


# 確率分布幅の保存場所
def config_width_save_path(folder_name):
    # 実験データの保存先のフォルダーがなければ作成する
    path = f"result/width/{folder_name}"
    os.makedirs(path, exist_ok=True)
    return path


# 結合後のgifの保存場所
def gif_save_path(exp_name, plot_type):
    # 実験データの保存先のフォルダーがなければ作成する
    path = f"result/{exp_name}/gif_{plot_type}_{exp_name}/"
    os.makedirs(path, exist_ok=True)
    return path
