import numpy as np
from analyze.visualization.plot_surface import Plotter, do_plot_3d_gif, main_Plotter
from config.config import *
import joblib
import glob
from simulation.algorithm import calc_probability


# def start_plot_surface_phase(exp_name, plot_exp_indexes=None):
#     """
#     exp_nameフォルダの中にあるexp_index_listで指定したexp_indexのt_step目のみをプロットする。
#     """
#     if plot_exp_indexes is None:
#         plot_exp_indexes = [0]
#     for plot_exp_index in plot_exp_indexes:
#         plotter = Plotter()
#         plotter.set_up_conditions(exp_name=exp_name, plot_exp_index=plot_exp_index)
#         plotter.plot_surface_by_phase(plot_t_step)


#
# def plot_surface_by_phase(exp_name, plot_t_step):
#     plotter = main_Plotter()
#     plotter.load_data(simulation_data_file_name= f"{config_simulation_data_save_path(exp_name)}{self.exp_index}/{str(plot_t_step).zfill(3)}.jb")
#     plotter.plot()

#
# def execute_plot_surface_by_phase(exp_name, plot_t_step):
#     """
#     exp_nameの中にある全実験（全exp_index）のt_step目のみをプロットする
#     """
#     # exp_nameにある全実験フォルダーへのpath。sortもする。
#     simulation_data_folder_path_list = glob.glob(f"{config_simulation_data_save_path(exp_name)}/*")
#     simulation_data_folder_path_list.sort()
#
#     # 各exp_indexのt_step目をプロット
#     for simulation_data_folder_path in simulation_data_folder_path_list:
#         # データをロード
#         save_data_object = joblib.load(f"{simulation_data_folder_path}/{str(plot_t_step).zfill(3)}.jb")
#
#         # 展開
#         condition = save_data_object["実験条件データ（condition）"]
#         T = condition.T
#         if T != Config_simulation.max_time_step:
#             print_warning("シミュレーションデータの最大時間ステップと現在の設定の最大時間ステップが一致しません。大丈夫ですか？")
#         len_x = 2 * T + 1
#         len_y = 2 * T + 1
#         t = save_data_object["このシミュレーションデータが何ステップ目か（t）"]
#         PSY = save_data_object["シミュレーションデータ"]
#         exp_index = condition.exp_index
#         phi_latex = condition.phi_latex
#         erase_t = condition.erase_t
#         if int(t) != plot_t_step:
#             print_warning("シミュレーションデータのファイル名と時間ステップが一致しません。至急確認してください")
#             raise EOFError
#
#         print(f"START：プロット：plot_exp_index={exp_index}")
#
#         # プロット
#         mesh_x, mesh_y = np.meshgrid(np.linspace(-T, T, 2 * T + 1), np.linspace(-T, T, 2 * T + 1), indexing="ij")
#         mesh_z = calc_probability(PSY, len_x, len_y)
#         do_plot_3d_gif(mesh_x, mesh_y, mesh_z,
#                        path=config_plot_phase_save_path(exp_name=exp_name, plot_t_step=plot_t_step),
#                        file_name=f"{str(exp_index).zfill(3)}.png", title=f"${phi_latex}$,erase_t={erase_t}")
#     print_finish("execute_plot_surface_by_phase")
