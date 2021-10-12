import numpy as np
import matplotlib.pyplot as plt

import config.config
from config.config import *
import joblib
from multiprocessing import Pool
import glob
from simulation.algorithm import calculate_probability_distribution_at_time_t_memory_save


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


def check_plot_progress(exp_name, plot_exp_index, T):
    # plotがどこまで進んだかをチェックし途中から再開するために、
    # plotのindexのフォルダが既に存在しており、plot数が足りていたらそのplotはは既に終了しているとする。
    finished = False
    folder_path = config_plot_save_path(exp_name, plot_exp_index)
    file_list = glob.glob(f"{folder_path}/*")

    need_file_num = T + 1
    file_num = len(file_list)
    print(f"exp_index={plot_exp_index}のデータ数：{file_num}")
    print(f"必要なデータ数：{need_file_num}")

    if need_file_num == file_num:
        print_green_text(f"plot_exp_index={plot_exp_index}：既に完了")
        finished = True
    return finished


# plotする
def execute_plot_surface(exp_name, plot_exp_index_list):
    # plot_exp_index_listの要素数だけforを回す。それぞれのforループの中で並列処理を行う
    # plot_exp_index：plotしたいexp_indexのリスト
    # i：plotしたいexp_indexのリストに0から番号をつけたもの
    for plot_exp_index in plot_exp_index_list:
        # 実験環境データを000.jbから代表して読みこむ
        save_data_object = joblib.load(f"{config_simulation_data_save_path(exp_name, plot_exp_index)}/000.jb")
        # 展開する
        condition = save_data_object["実験条件データ（condition）"]
        T = condition.T

        # plot_exp_indexのプロットが既に終了しているのかをチェックする。完了していたらスキップする
        # if check_plot_progress(exp_name, plot_exp_index, T):
        #     continue

        # 並列処理を行う。何を並列処理させるかというとプロット処理。どれからプロットしようと問題ないので並列処理できる
        print(f"START：プロット：plot_exp_index={plot_exp_index}")

        # 並列処理用の前処理
        # 各並列プログラムにexp_nameのexp_indexに入っているデータファイルの全ての名前を教える
        simulation_data_file_names = glob.glob(f"{config_simulation_data_save_path(exp_name, plot_exp_index)}/*.jb")
        simulation_data_file_names.sort()  # 実験順にsortする。

        # どのデータ抽出するかを選択する
        t_list = list(range(0, 100, 5))
        if Config_simulation.max_time_step == 2000:
            t_list += list(range(100, 2050, 50))
        elif Config_simulation.max_time_step == 600:
            t_list += list(range(100, 620, 20))
        elif Config_simulation.max_time_step == 200:
            t_list += list(range(100, 205, 5))
        elif Config_simulation.max_time_step == 100:
            pass

        arguments = []
        # simulation_data_file_name＝実験データのtステップとはしない。ファイル名はファイル名以上の意味と持たない。
        for t_step in t_list:
            arguments.append(
                [simulation_data_file_names[t_step], config_plot_save_path(exp_name=exp_name, index=plot_exp_index)])

        # 並列数
        p = Pool(config.config.Config_simulation.plot_parallel_num)
        # 並列処理開始
        p.map(wrapper_plot_and_save_memory_save, arguments)
        print_finish("execute_plot_surface")
        # processをclose
        p.close()
        p.terminate()


# wrapper
def wrapper_plot_and_save_memory_save(args):
    return plot_and_save(*args)


def plot_and_save(simulation_data_file_name, plot_path):
    """
    :param simulation_data_file_name: plotするデータファイルの名前（exp_nameのexp_indexに入っている）
    :param plot_path: plotした画像の保存場所
    :return:
    """
    # データをロード
    save_data_object = joblib.load(simulation_data_file_name)
    # 展開
    condition = save_data_object["実験条件データ（condition）"]
    T = condition.T
    len_x = 2 * T + 1
    len_y = 2 * T + 1
    t = save_data_object["このシミュレーションデータが何ステップ目か（t）"]
    PSY = save_data_object["シミュレーションデータ"]

    # 格子点を作成
    mesh_x, mesh_y = np.meshgrid(np.linspace(-T, T, 2 * T + 1), np.linspace(-T, T, 2 * T + 1), indexing="ij")
    # 確率の計算
    mesh_z = calculate_probability_distribution_at_time_t_memory_save(PSY, len_x, len_y)
    # 0埋めする
    t_index = str(t).zfill(3)
    # タイトルを設定
    erase_t = condition.erase_t
    title = f"$t={t},erase_t={erase_t}$"
    # plotする
    do_plot_3d_gif(mesh_x, mesh_y, mesh_z, plot_path, f"{t_index}.png", title)
    print(f"t={t_index}：可視化と保存：完了")


def do_plot_3d_gif(mesh_x, mesh_y, mesh_z, path, file_name, title):
    fig = plt.figure(figsize=(4, 3), tight_layout=True, dpi=400)
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.set_xlabel("$x$", size=24, labelpad=10)
    ax.set_ylabel("$y$", size=24)
    ax.set_zlabel("$p$", size=24, labelpad=15)
    # 軸メモリの調整
    ax.tick_params(labelsize=24)
    # タイトルを設定
    ax.set_title(title, size=24)
    # 曲面を描画
    ax.plot_surface(mesh_x, mesh_y, mesh_z, cmap="summer")
    plt.savefig(f"{path}/{file_name}", dpi=400, bbox_inches='tight')
    # メモリ解放
    fig.clf()
    ax.cla()
    plt.close()
