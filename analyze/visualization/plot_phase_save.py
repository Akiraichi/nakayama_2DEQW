import numpy as np
from analyze.visualization.plot_memory_save import do_plot_3d_gif, load_env_date
from config.config import *
import joblib
import glob
from simulation.algorithm_memory_save import calculate_probability_distribution_at_time_t_memory_save


def execute_plot_phase(exp_name, t_step):
    # 実験データの00、01みたいなのが全部でいくつあるのかをチェックし、フォルダー名を含んだパス名をfoldersに入れる。
    folder_path_list = glob.glob(f"{config_simulation_save_mamory_data_save_path(exp_name)}/*")
    folder_path_list.sort()

    # 実験環境の数（00や01とかのフォルダーの数）だけforを回す。それぞれのforループの中で処理を行う
    for index, folder_path in enumerate(folder_path_list):
        # 実験環境データの読みこみ
        T, condition, len_x, len_y = load_env_date(exp_name=exp_name, i=index)

        # 実験データの読み込み
        file_path = f"{folder_path}/{str(t_step).zfill(3)}.jb"  # 実験データへのパス
        try:
            # 実験データを取得
            PSY = joblib.load(file_path)
        except EOFError as e:
            print("PSY = joblib.load(file_name)で例外発生：")
            print(e)
            return

        print(f"{index}回目：可視化結果の保存：開始")
        # 格子点を作成
        mesh_x, mesh_y = np.meshgrid(np.linspace(-T, T, 2 * T + 1), np.linspace(-T, T, 2 * T + 1), indexing="ij")
        mesh_z = calculate_probability_distribution_at_time_t_memory_save(PSY, len_x, len_y)
        do_plot_3d_gif(mesh_x, mesh_y, mesh_z, path=config_plot_phase_save_path(exp_name=exp_name, plot_t_step=t_step),
                       file_name=f"{str(index).zfill(3)}.png", title=f"${condition.phi_latex}$")
        print(f"phi={condition.phi_latex}：可視化と保存：完了")
