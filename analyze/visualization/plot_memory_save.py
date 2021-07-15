import numpy as np
import matplotlib.pyplot as plt

import config.config
from config.config import *
import joblib
from multiprocessing import Pool
import glob
from simulation.algorithm_memory_save import calculate_probability_distribution_at_time_t_memory_save


# 実験環境データの読みこみと展開
def load_env_date(exp_name, i):
    # データの取り出し
    env_data = joblib.load(
        f"{config_simulation_save_mamory_data_save_path(exp_name, i)}/{config_simulation_save_memory_data_name(i)}")

    # 読み込んだオブジェクトを展開する
    T = env_data.T
    condition = env_data.condition
    len_x = env_data.len_x
    len_y = env_data.len_y
    return T, condition, len_x, len_y


def check_plot_progress(exp_name, i, T):
    # plotがどこまで進んだかをチェックし途中から再開するために、
    # plotのindexのフォルダが既に存在しており、plot数が足りていたらそのplotはは既に終了しているとする。
    finished = False
    folder_path = config_plot_save_path(exp_name, i)
    file_list = glob.glob(f"{folder_path}/*")
    # シミュレーションによって生じたファイル数が必要な数に達しているかをチェックする。envファイルがあるので＋1する
    if T == len(file_list):
        finished = True
    return finished


# plotする
def execute_plot_memory_save_2(exp_name):
    """
    このプログラムでは必要なデータだけをロードしプロットします。ロードサイズがこれまでと比べ1/600〜1/400程度なので、
    並列処理で実行しても良いかと思います。
    """
    # 実験の00、01みたいなのが全部でいくつあるのかをチェックする
    folder_path_list = glob.glob(f"{config_simulation_save_mamory_data_save_path(exp_name)}/*")

    # 実験環境の数（00や01とかのフォルダーの数）だけforを回す。それぞれのforループの中で並列処理を行う
    for i, _ in enumerate(folder_path_list):
        # 実験環境データの読みこみ
        T, condition, len_x, len_y = load_env_date(exp_name=exp_name, i=i)

        # plotをするべきか、既に終了しているのかをチェックする
        if check_plot_progress(exp_name, i, T):
            print(f"{i}回目：既に完了しています")
            continue

        # 並列処理を行う。何を並列処理させるかというとプロット処理。どれからプロットしようと問題ないので並列処理できる
        print(f"{i}回目：可視化結果の保存：開始")
        # 並列処理用の前処理
        # 各並列プログラムに00や01といったフォルダに入っているplotファイルの名前を教える
        file_names = glob.glob(f"{config_simulation_save_mamory_data_save_path(exp_name, i)}/*.jb")
        file_names.sort()  # 実験順にsortする。

        # fast_plot = True
        # num = 4
        # if fast_plot:
        #     new_file_names = [file for i, file in enumerate(file_names) if i % num == 0]
        #     file_names = new_file_names

        arguments = []
        for t_step, file_name in enumerate(file_names):
            arguments.append(
                [file_name, len_x, len_y, T, config_plot_save_path(exp_name=exp_name, index=i), t_step, ])

        # 並列数
        p = Pool(config.config.Config_simulation.plot_parallel_num)
        # 並列処理開始
        p.map(wrapper_plot_and_save_memory_save, arguments)
        # processをclose
        p.close()
        p.terminate()


# wrapper
def wrapper_plot_and_save_memory_save(args):
    return plot_and_save_memory_save(*args)


def plot_and_save_memory_save(file_name, len_x, len_y, T, plot_path, t):
    try:
        # 実験データを取得
        PSY = joblib.load(file_name)
    except EOFError as e:
        print("PSY = joblib.load(file_name)で例外発生：")
        print(e)
        return

    # 格子点を作成
    mesh_x, mesh_y = np.meshgrid(np.linspace(-T, T, 2 * T + 1), np.linspace(-T, T, 2 * T + 1), indexing="ij")
    # 確率の計算
    mesh_z = calculate_probability_distribution_at_time_t_memory_save(PSY, len_x, len_y)
    # 0埋めする
    t_index = str(t).zfill(3)
    # タイトルを決める
    title = f"$t={t}$"
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


if __name__ == '__main__':
    from exp_setting.exp import *

    # y軸に電場を加える
    conditions, exp_name = exp_0000__debug_folder_changed_check_set()
    execute_plot_memory_save_2(exp_name)
