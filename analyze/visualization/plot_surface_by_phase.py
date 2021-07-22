import numpy as np
from analyze.visualization.plot_surface import do_plot_3d_gif
from config.config import *
import joblib
import glob
from simulation.algorithm import calculate_probability_distribution_at_time_t_memory_save


def execute_plot_surface_by_phase(exp_name, plot_t_step):
    """
    exp_nameの中にある全実験（全exp_index）のt_step目のみをプロットする
    :param exp_name:
    :param plot_t_step:
    :return:
    """
    # exp_nameにある全実験フォルダーへのpath。sortもする。
    simulation_data_folder_path_list = glob.glob(f"{config_simulation_data_save_path(exp_name)}/*")
    simulation_data_folder_path_list.sort()

    # 各exp_indexのt_step目をプロット
    for simulation_data_folder_path in simulation_data_folder_path_list:
        # データをロード
        save_data_object = joblib.load(f"{simulation_data_folder_path}/{str(plot_t_step).zfill(3)}.jb")

        # 展開
        condition = save_data_object["実験条件データ（condition）"]
        T = condition.T
        if T != Config_simulation.max_time_step:
            print_warning("シミュレーションデータの最大時間ステップと現在の設定の最大時間ステップが一致しません。大丈夫ですか？")
        len_x = 2 * T + 1
        len_y = 2 * T + 1
        t = save_data_object["このシミュレーションデータが何ステップ目か（t）"]
        PSY = save_data_object["シミュレーションデータ"]
        exp_index = condition.exp_index
        phi_latex = condition.phi_latex
        if int(t) != plot_t_step:
            print_warning("シミュレーションデータのファイル名と時間ステップが一致しません。至急確認してください")
            raise EOFError

        print(f"START：プロット：plot_exp_index={exp_index}")

        # プロット
        mesh_x, mesh_y = np.meshgrid(np.linspace(-T, T, 2 * T + 1), np.linspace(-T, T, 2 * T + 1), indexing="ij")
        mesh_z = calculate_probability_distribution_at_time_t_memory_save(PSY, len_x, len_y)
        do_plot_3d_gif(mesh_x, mesh_y, mesh_z,
                       path=config_plot_phase_save_path(exp_name=exp_name, plot_t_step=plot_t_step),
                       file_name=f"{str(exp_index).zfill(3)}.png", title=f"${phi_latex}$")
    print_finish("execute_plot_surface_by_phase")
