import numpy as np
import matplotlib.pyplot as plt
from config.config import *
import joblib
import glob
from simulation.algorithm import calculate_probability_distribution_at_time_t_memory_save
from numba import njit, jit
from multiprocessing import Pool
import config.config


def parallel_execute_plot_kl_div(exp_name_1, exp_index_1, exp_name_2, exp_index_2_list):
    # 並列処理用の前処理
    arguments = []
    for exp_index_2 in exp_index_2_list:
        arguments.append(
            [exp_name_1, exp_index_1, exp_name_2, exp_index_2])

    # 並列数
    p = Pool(config.config.Config_simulation.plot_parallel_num)
    # 並列処理開始
    p.map(wrapper_plot_and_save_memory_save, arguments)
    print_finish("execute_parallel_kl_div")
    # processをclose
    p.close()
    p.terminate()


# wrapper
def wrapper_plot_and_save_memory_save(args):
    return execute_plot_kl_div(*args)


def execute_plot_kl_div(exp_name_1, exp_index_1, exp_name_2, exp_index_2):
    """
    概要
        量子ウォークの確率分布のKLダイバージェンスを求める
    処理の流れ
        （1）データをロードする。
        （2）二つのprobabilityを引数から受け取る。その二つの確率分布のKLダイバージェンスを返却する
        （3）KLダイバージェンスの推移をプロットする
    """
    # 実験環境データを000.jbから代表して読みこむ
    # save_data_object_1 = joblib.load(f"{config_simulation_data_save_path(exp_name_1, exp_index_1)}/000.jb")
    # 展開する
    # condition_1 = save_data_object_1["実験条件データ（condition）"]
    print(
        f"START：KLダイバージェンスを求める処理：exp_name_1={exp_name_1},exp_index_1={exp_index_1},exp_name_2={exp_name_2},exp_index_2={exp_index_2}, ")

    simulation_data_file_names_1 = glob.glob(f"{config_simulation_data_save_path(exp_name_1, exp_index_1)}/*.jb")
    simulation_data_file_names_1.sort()  # 実験順にsortする。

    simulation_data_file_names_2 = glob.glob(f"{config_simulation_data_save_path(exp_name_2, exp_index_2)}/*.jb")
    simulation_data_file_names_2.sort()  # 実験順にsortする。

    KL_div_list = []
    # simulation_data_fileはt=0から1ずつ増えていきながら、t=ファイルの数まであるので、t_stepをenumerateの形で得ている。
    for t_step, _ in enumerate(simulation_data_file_names_1):
        # t=t_stepのシミュレーションデータをロード
        p_1 = get_probability(simulation_data_file_names_1, t_step)
        p_2 = get_probability(simulation_data_file_names_2, t_step)
        KL_div = get_KL_div(p1=p_1, p2=p_2)
        KL_div_list.append(KL_div)

    t_list = list(range(len(KL_div_list)))
    do_plot_kl_div(exp_name_1, exp_index_1, exp_name_2, exp_index_2, KL_div_list, t_list)


# 実験環境データの読みこみと展開
def load_env_date(exp_name, i):
    # データの取り出し
    env_data = joblib.load(
        f"{config_simulation_data_save_path(exp_name, i)}/{config_simulation_data_name(i)}")

    # 読み込んだオブジェクトを展開する
    T = env_data.T
    condition = env_data.condition
    len_x = env_data.len_x
    len_y = env_data.len_y
    return T, condition, len_x, len_y


@njit('f8(f8[:,:],f8[:,:])', cache=True)
def get_KL_div(p1, p2):
    """
        概要
            量子ウォークの確率分布のKLダイバージェンスを求める
        処理の流れ
            （1）二つのprobabilityを引数から受け取る。その二つの確率分布のKLダイバージェンスを返却する
        引数
            p1,p2：大きさの等しい2次元リストp1[x,y]のように指定できること。

        """
    kl_div = 0
    # 属性shapeで形状（行数、列数）が取得可能。
    for x in range(p1.shape[1]):
        for y in range(p1.shape[0]):
            if p2[x, y] == 0:
                continue
            kl_div += p1[x, y] * np.log(p1[x, y] / p2[x, y])

    return kl_div


def do_plot_kl_div(exp_name_1, exp_index_1, exp_name_2, exp_index_2, KL_div_list, t_list):
    fig = plt.figure(figsize=(4, 3), tight_layout=True, dpi=400)
    ax = fig.add_subplot(111, xlabel="t", ylabel="KL_div")
    ax.scatter(t_list, KL_div_list, c='blue')
    fig.savefig(f'{config_KL_div_save_path()}/KL_div_{exp_name_1}_{exp_index_1}-{exp_name_2}_{exp_index_2}.png')
    print("FIN")


def get_probability(simulation_data_file_names, index):
    save_data_object = joblib.load(simulation_data_file_names[index])
    condition = save_data_object["実験条件データ（condition）"]
    T = condition.T
    len_x = 2 * T + 1
    len_y = 2 * T + 1
    PSY = save_data_object["シミュレーションデータ"]
    # probability[x,y]として(x,y)座標の確率を求められる。
    probability = calculate_probability_distribution_at_time_t_memory_save(PSY, len_x, len_y)
    return probability
