from analyze.visualization.plot_memory_save import load_env_date
from config.config import *
import joblib
import glob
from simulation.algorithm_memory_save import calculate_probability_distribution_at_time_t_memory_save
import matplotlib.pyplot as plt
import seaborn as sns


def execute_plot_heatmap(exp_name, t_step):
    # 実験データの00、01みたいなのが全部でいくつあるのかをチェックし、フォルダー名を含んだパス名をfoldersに入れる。
    folder_path_list = glob.glob(f"{config_simulation_save_mamory_data_save_path(exp_name)}/*")
    folder_path_list.sort()

    # 実験環境の数（00や01とかのフォルダーの数）だけforを回す。それぞれのforループの中で処理を行う
    for i, folder_path in enumerate(folder_path_list):
        # 実験環境データの読みこみ
        T, condition, len_x, len_y = load_env_date(exp_name=exp_name, i=i)

        # 実験データの読み込み
        file_path = f"{folder_path}/{str(t_step).zfill(3)}.jb"  # 実験データへのパス
        try:
            # 実験データを取得
            PSY = joblib.load(file_path)
        except EOFError as e:
            print("PSY = joblib.load(file_name)で例外発生：")
            print(e)
            return

        # 確率を計算
        prob_list = calculate_probability_distribution_at_time_t_memory_save(PSY, len_x, len_y)
        print(f"{i}回目：可視化結果の保存：開始")
        plot_heat_map(prob_list=prob_list, path=config_heat_map_save_path(exp_name=exp_name, plot_t_step=t_step),
                      file_name=f"{str(i).zfill(3)}.png", title=f"${condition.phi_latex}$")
        print(f"phi={condition.phi_latex}：可視化と保存：完了")


def plot_heat_map(prob_list, path, file_name, title):
    """heatmapをプロットする"""
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    sns.heatmap(prob_list, square=True,cmap="hot")
    ax.set_title(title, size=24)
    plt.savefig(f"{path}/{file_name}", dpi=400, bbox_inches='tight')
    plt.close('all')
