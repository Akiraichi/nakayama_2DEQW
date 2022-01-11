import numpy as np
import matplotlib.pyplot as plt
import joblib
import glob

from config.config_simulation import config_simulation_data_save_path
from simulator.simulation_algorithm import calc_probability


# 実験環境データの読みこみと展開
# def load_env_date(exp_name, i):
#     # データの取り出し
#     env_data = joblib.load(
#         f"{config_simulation_data_save_path(exp_name, i)}/{config_simulation_data_name(i)}")
#
#     # 読み込んだオブジェクトを展開する
#     T = env_data.T
#     condition = env_data.condition
#     len_x = env_data.len_x
#     len_y = env_data.len_y
#     return T, condition, len_x, len_y


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
            probability = calc_probability(PSY, len_x, len_y)
            var_y = np.var(probability, axis=0)  # 行ごとの分散を求める。y軸方向の分散が求まる
            var_x = np.var(probability, axis=1)  # 列ごとの分散を求める。x軸方向の分散が求まる
            var_all = np.var(probability)
            # どこの場所の分散を求めるか？によって、変わるが、200はちょうどx=0、y=0の場所
            var_x_list.append(var_x[200])
            var_y_list.append(var_y[200])
            var_all_list.append(var_all)
            t_list.append(t_step)
        do_plot_var(exp_name, var_x_list, var_y_list, var_all_list, t_list, plot_exp_index)


def do_plot_var(exp_name, var_x_list, var_y_list, var_all_list, t_list, plot_exp_index):
    fig = plt.figure(figsize=(4, 3), tight_layout=True, dpi=400)
    ax = fig.add_subplot(111, xlabel="t", ylabel="var")
    ax.scatter(t_list, var_all_list, c='blue')
    fig.savefig(f'{config_var_save_path(exp_name=exp_name)}/{plot_exp_index}.png')
    print(plot_exp_index)
