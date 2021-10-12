# from config.config import *
# import joblib
# from simulation.algorithm import calc_probability
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd
#
#
# def execute_plot_heatmap_by_phase(exp_name, exp_index_list, plot_t_step):
#     """
#     exp_nameフォルダの中にあるexp_index_listで指定したexp_indexのt_step目のみをプロットする。
#     """
#     # 各exp_indexのt_step目をプロット
#     for exp_index in exp_index_list:
#         # データをロード
#         exp_index = str(exp_index).zfill(2)
#         save_data_object = joblib.load(
#             f"{config_simulation_data_save_path(exp_name)}{exp_index}/{str(plot_t_step).zfill(3)}.jb")
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
#         prob_list = calc_probability(PSY, len_x, len_y)
#         plot_heat_map(prob_list=prob_list, path=config_heatmap_save_path(exp_name=exp_name, plot_t_step=plot_t_step),
#                       file_name=f"{str(exp_index).zfill(3)}.png", title=f"${phi_latex}$,erase_t={erase_t}")
#     print_finish("execute_plot_heatmap_by_phase")
#
#
# def plot_heat_map(prob_list, path, file_name, title):
#     """heatmapをプロットする"""
#     # プロット用のデータフレームの作成
#     x_len = prob_list.shape[0]
#     T = Config_simulation.max_time_step
#     l = []
#     for k in range(x_len):
#         l.append(str(k - T))
#     df = pd.DataFrame(prob_list, index=l, columns=l)
#
#     # figureを作成しプロットする
#     fig = plt.figure()
#     ax = fig.add_subplot(1, 1, 1)
#     sns.heatmap(df, square=True, cmap="gist_heat_r")
#     # sns.heatmap(df, square=True, cmap="Blues")
#     ax.set_title(title, size=24)
#     plt.savefig(f"{path}/{file_name}", dpi=800, bbox_inches='tight')
#     plt.close('all')
