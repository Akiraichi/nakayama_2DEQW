# class ConfigSimulation:
#     moduleList = sys.modules
#     ENV_COLAB = False
#
#     if 'google.colab' in moduleList:
#         ENV_COLAB = True
#
#     if ENV_COLAB:
#         print("Execute in google_colab")
#         # 実験条件の設定
#         MaxTimeStep = 600  # 最大時間ステップ数
#         # シミュレーションの並列数
#         SimulationParallelNum = 4
#         # plotの並列数
#         PlotParallelNum = 4
#     else:
#         print("Execute in local")
#         # 実験条件の設定
#         MaxTimeStep = 200  # 最大時間ステップ数
#         # シミュレーションの並列数
#         SimulationParallelNum = 4
#         # plotの並列数
#         PlotParallelNum = 4


# 実験データの保存場所。タイムステップごとに分割


# # 保存する実験環境データの名前
# def config_simulation_data_name(index):
#     # index=実験した時の順番でつけた番号。0埋めする
#     index = str(index).zfill(2)
#     return f"{index}_env.env"


# プロットの保存場所


# # 確率の保存場所
# def config_prob_save_path(folder_name):
#     # 実験データの保存先のフォルダーがなければ作成する
#     path = f"result/prob/{folder_name}"
#     os.makedirs(path, exist_ok=True)
#     return path
#
#
# # 分散の保存場所
# def config_var_save_path(folder_name):
#     # 実験データの保存先のフォルダーがなければ作成する
#     path = f"result/var/{folder_name}"
#     os.makedirs(path, exist_ok=True)
#     return path
#
#
# # 確率分布幅の保存場所
# def config_width_save_path(folder_name):
#     # 実験データの保存先のフォルダーがなければ作成する
#     path = f"result/width/{folder_name}"
#     os.makedirs(path, exist_ok=True)
#     return path
#
#
# # 結合後のgifの保存場所
# def gif_save_path(exp_name, plot_type):
#     # 実験データの保存先のフォルダーがなければ作成する
#     path = f"result/{exp_name}/gif_{plot_type}_{exp_name}/"
#     os.makedirs(path, exist_ok=True)
#     return path
