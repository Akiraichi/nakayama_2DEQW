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


def execute_plot_var(exp_name, plot_exp_index_list):
    """
    概要
        量子ウォークの確率分布の分散を求める。
        2次元格子状の量子ウォークなので、x軸、y軸の2軸で確率分布の分散σを求める
    分散をどう求めるか？
        案1：例えば、x軸の分散を求めるのであれば、y軸に広がった確率分布全ての平均E[Y^2] - E[Y]^2で求まるのでは？
    処理の流れ
        （1）複数の実験をリストを使って引数に渡すと、リストにある実験全てについて処理される、という仕様であるため、
        まず、引数に渡されたリストの回数だけ以下の処理を実行する。そのために、リストでforを回す
        （2）実験環境ファイルを読み込み、その中にあるconditionといった実験環境がどのようなものであるかの情報を手に入れる
        （3）途中中断、途中実行された場合、既に完了した処理を再実行しないために、現在の実験が既にプロット完了しているかどうかを確認する
        （4）並列処理の準備をする。分散はmax_t_stepまでの全てで実行する。並列かするメリットがあるかはまだ不明だが、まずはやってみる
        以下、各並列処理の中
        （5）実験データをロードする
        （6）分散を求める
        （7）プロットする。保存する

    次やること
        分散処理させると、プロットする時にデータがなくても困るので、分散処理はやめておく。というか、分散処理させても分散処理させる方のオーベーヘッドの方が大きいと予想できる。
        思ったより、分散を求める処理はコストが小さい。
        ・分散処理をやめる
        ・プロットできるかの調整
        ・コードの確認など

    :param exp_name: exp_018といった実験名
    :param plot_exp_index_list: 使用用途未定
    :return: 横軸が時間ステップt、縦軸が分散σである、グラフ図
    """
    # plot_exp_index_listの要素数だけforを回す。それぞれのforループの中で並列処理を行う
    # plot_exp_index：plotしたいexp_indexのリスト
    # i：plotしたいexp_indexのリストに0から番号をつけたもの
    # 具体的な処理内容的には、simulation_dataフォルダ内の、00,01,02といったフォルダ名に対応させるためのもの
    for plot_exp_index in plot_exp_index_list:
        # 実験環境データを000.jbから代表して読みこむ
        save_data_object = joblib.load(f"{config_simulation_data_save_path(exp_name, plot_exp_index)}/000.jb")
        # 展開する
        condition = save_data_object["実験条件データ（condition）"]
        T = condition.T

        # plot_exp_indexのプロットが既に終了しているのかをチェックする。完了していたらスキップする
        # if check_plot_progress(exp_name, plot_exp_index, T):
        #     continue

        print(f"START：分散を求める処理：plot_exp_index={plot_exp_index}")

        """
        exp_nameのexp_indexに入っているデータファイルの全ての名前を教える
        Example
            simulation_data_file_names = glob.glob(f"{config_simulation_data_save_path(exp_name, plot_exp_index)}/*.jb")
            simulation_data_file_names.sort()  # 実験順にsortする。
            exp_019に入ってるあるsimulation_dataフォルダ内には000.jb,001.jbといったシミュレータションデータが入ってある。
            これら000.jb,001.jbといったシミュレータションデータの全てのファイル名をリストの形式で得る。
            sortすることで、000,001といったように番号順にリストの中で並べ替えられる
        """
        simulation_data_file_names = glob.glob(f"{config_simulation_data_save_path(exp_name, plot_exp_index)}/*.jb")
        simulation_data_file_names.sort()  # 実験順にsortする。

        var_x_list = []
        var_y_list = []
        var_all_list = []
        t_list = []
        # simulation_data_fileはt=0から1ずつ増えていきながら、t=ファイルの数まであるので、t_stepをenumerateの形で得ている。
        for t_step, simulation_data_file_name in enumerate(simulation_data_file_names):
            # t=t_stepのシミュレーションデータをロード
            save_data_object = joblib.load(simulation_data_file_name)
            condition = save_data_object["実験条件データ（condition）"]
            T = condition.T
            len_x = 2 * T + 1
            len_y = 2 * T + 1
            PSY = save_data_object["シミュレーションデータ"]

            # probability[x,y]として(x,y)座標の確率を求められる。
            probability = calculate_probability_distribution_at_time_t_memory_save(PSY, len_x, len_y)
            var_y = np.var(probability, axis=0)  # 行ごとの分散を求める。y軸方向の分散が求まる
            var_x = np.var(probability, axis=1)  # 列ごとの分散を求める。x軸方向の分散が求まる
            var_all = np.var(probability)
            # どこの場所の分散を求めるか？によって、変わるが、200はちょうどx=0、y=0の場所
            var_x_list.append(var_x[200])
            var_y_list.append(var_y[200])
            var_all_list.append(var_all)
            t_list.append(t_step)

        do_plot_var(exp_name, var_x_list, var_y_list, var_all_list, t_list, plot_exp_index)


def plot_dist_and_save(simulation_data_file_name, plot_path):
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

    # 実験データを手に入れたので、ここから分散を求めていく

    # # 格子点を作成
    # mesh_x, mesh_y = np.meshgrid(np.linspace(-T, T, 2 * T + 1), np.linspace(-T, T, 2 * T + 1), indexing="ij")
    # 確率の計算。probability[x,y]で全座標の確率が格納される
    probability = calculate_probability_distribution_at_time_t_memory_save(PSY, len_x, len_y)
    prob_y = np.var(probability, axis=0)  # 行ごとの分散を求める。y軸方向の分散が求まる
    prob_x = np.var(probability, axis=1)  # 列ごとの分散を求める。x軸方向の分散が求まる

    # 0埋めする
    t_index = str(t).zfill(3)
    # タイトルを設定
    title = f"$t={t}$"
    # plotする

    # do_plot_3d_gif(mesh_x, mesh_y, mesh_z, plot_path, f"{t_index}.png", title)
    print(f"t={t_index}：分散の可視化と保存：完了")


def do_plot_var(exp_name, var_x_list, var_y_list, var_all_list, t_list, plot_exp_index):
    fig = plt.figure(figsize=(4, 3), tight_layout=True, dpi=400)
    ax = fig.add_subplot(111, xlabel="t", ylabel="var")
    ax.scatter(t_list, var_all_list, c='blue')
    fig.savefig(f'{config_var_save_path(exp_name=exp_name)}/{plot_exp_index}.png')
    print(plot_exp_index)


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
