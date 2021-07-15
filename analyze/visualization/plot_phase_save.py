import numpy as np
from analyze.visualization.plot_memory_save import do_plot_3d_gif, load_env_date
from config.config import *
import joblib
import glob
from simulation.algorithm_memory_save import calculate_probability_distribution_at_time_t_memory_save


def execute_plot_phase(exp_name, t_step):
    """
    このプログラムではt_stepステップ目のデータだけをロードしプロットします。
    """
    # 実験データの00、01みたいなのが全部でいくつあるのかをチェックし、フォルダー名を含んだパス名をfoldersに入れる。
    # この時点では順番は適当だがプロットする順番は適当で良いから別に良い（ファイル名は順番に関係ない）
    folder_path_list = glob.glob(f"{config_simulation_save_mamory_data_save_path(exp_name)}/*")

    # 実験環境の数（00や01とかのフォルダーの数）だけforを回す。それぞれのforループの中で処理を行う
    for i, folder_path in enumerate(folder_path_list):
        # 実験環境データの読みこみ
        T, condition, len_x, len_y = load_env_date(exp_name=exp_name, i=i)
        print(f"{i}回目：可視化結果の保存：開始")
        plot_path = config_plot_phase_save_path(exp_name=exp_name, plot_t_step=t_step)  # プロットの保存場所へのパス
        file_path = f"{folder_path}/{str(t_step).zfill(3)}.jb"  # 実験データへのパス
        plot_phase(file_path, len_x, len_y, T, plot_path, i, phi=condition.phi_latex)


def plot_phase(file_path, len_x, len_y, T, plot_path, index, phi):
    try:
        # 実験データを取得
        PSY = joblib.load(file_path)
    except EOFError as e:
        print("PSY = joblib.load(file_name)で例外発生：")
        print(e)
        return
    # 格子点を作成
    mesh_x, mesh_y = np.meshgrid(np.linspace(-T, T, 2 * T + 1), np.linspace(-T, T, 2 * T + 1), indexing="ij")
    # 確率を計算
    mesh_z = calculate_probability_distribution_at_time_t_memory_save(PSY, len_x, len_y)
    # タイトルを設定する
    title = f"${phi}$"
    # plot
    do_plot_3d_gif(mesh_x, mesh_y, mesh_z, plot_path, f"{str(index).zfill(3)}.png", title)
    print(f"phi={phi}：可視化と保存：完了")


if __name__ == '__main__':
    from exp_setting.exp import *

    conditions, exp_name = exp_0000__debug_folder_changed_check_set()
    plot_t_step = 99
    execute_plot_phase(exp_name, plot_t_step)
