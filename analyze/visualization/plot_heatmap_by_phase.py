from analyze.visualization.plot_surface import load_env_date
from config.config import *
import joblib
import glob
from simulation.algorithm import calculate_probability_distribution_at_time_t_memory_save
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def execute_plot_heatmap_by_phase(exp_name, t_step):
    """
        exp_nameの中にある全実験（全exp_index）のt_step目のみをプロットする
        :param exp_name:
        :param t_step:
        :return:
        """
    # exp_nameにある全実験フォルダーへのpath。sortもする。
    simulation_data_folder_path_list = glob.glob(f"{config_simulation_data_save_path(exp_name)}/*")
    simulation_data_folder_path_list.sort()

    # 各exp_indexのt_step目をプロット
    for simulation_data_folder_path in simulation_data_folder_path_list:
        # データをロード
        save_data_object = joblib.load(f"{simulation_data_folder_path}/{str(t_step).zfill(3)}.jb")

        # 展開
        condition = save_data_object["実験条件データ（condition）"]
        T = condition.T
        len_x = 2 * T + 1
        len_y = 2 * T + 1
        t = save_data_object["このシミュレーションデータが何ステップ目か（t）"]
        PSY = save_data_object["シミュレーションデータ"]
        exp_index = condition.exp_index
        phi_latex = condition.phi_latex
        if t != t_step:
            print("ERROR：シミュレーションデータのファイル名と時間ステップが一致しません。至急確認してください")
            raise EOFError

        print(f"START：プロット：plot_exp_index={exp_index}")

        # プロット
        prob_list = calculate_probability_distribution_at_time_t_memory_save(PSY, len_x, len_y)
        plot_heat_map(prob_list=prob_list, path=config_heatmap_save_path(exp_name=exp_name, plot_t_step=t_step),
                      file_name=f"{str(exp_index).zfill(3)}.png", title=f"${phi_latex}$")

        print("完了")


def plot_heat_map(prob_list, path, file_name, title):
    """heatmapをプロットする"""
    # プロット用のデータフレームの作成
    x_len = prob_list.shape[0]
    T = Config_simulation.max_time_step
    l = []
    for k in range(x_len):
        l.append(str(k - T))
    df = pd.DataFrame(prob_list, index=l, columns=l)

    # figureを作成しプロットする
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    sns.heatmap(df, square=True, cmap="gist_heat_r")
    # sns.heatmap(df, square=True, cmap="Blues")
    ax.set_title(title, size=24)
    plt.savefig(f"{path}/{file_name}", dpi=800, bbox_inches='tight')
    plt.close('all')
