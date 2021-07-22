import os


class Config_simulation:
    import sys
    print(type(sys.modules))
    moduleList = sys.modules
    ENV_COLAB = False

    if 'google.colab' in moduleList:
        ENV_COLAB = True

    if ENV_COLAB:
        print("Execute in google_colab")
        # 実験条件の設定
        max_time_step = 600  # 最大時間ステップ数
        # シミュレーションの並列数
        simulation_parallel_num = 4
        # plotの並列数
        plot_parallel_num = 4
    else:
        print("Execute in local")
        # 実験条件の設定
        max_time_step = 100  # 最大時間ステップ数
        # シミュレーションの並列数
        simulation_parallel_num = 4
        # plotの並列数
        plot_parallel_num = 4


class Config_save_log:
    path = "log/log_data"


# 実験データの保存場所。タイムステップごとに分割
def config_simulation_data_save_path(exp_name, index=None):
    # 実験データの保存先のフォルダーがなければ作成する
    if index is None:
        path = f"result/{exp_name}/simulation_data_{exp_name}/"
    else:
        # index=実験した時の順番でつけた番号。0埋めする
        index = str(index).zfill(2)
        path = f"result/{exp_name}/simulation_data_{exp_name}/{index}"
    os.makedirs(path, exist_ok=True)
    return path


# 保存する実験環境データの名前
def config_simulation_data_name(index):
    # index=実験した時の順番でつけた番号。0埋めする
    index = str(index).zfill(2)
    return f"{index}_env.env"


# 3次元プロットデータの保存場所
def config_plot_save_path(exp_name, index=None):
    # 実験データの保存先のフォルダーがなければ作成する
    if index is None:
        path = f"result/{exp_name}/plot_img_{exp_name}"
    else:
        # index=実験した時の順番でつけた番号。0埋めする
        index = str(index).zfill(2)
        path = f"result/{exp_name}/plot_img_{exp_name}/{index}"
    os.makedirs(path, exist_ok=True)
    return path


# 位相ごとの3次元プロットデータの保存場所
def config_plot_phase_save_path(exp_name, plot_t_step):
    # 実験データの保存先のフォルダーがなければ作成する
    path = f"result/{exp_name}/plot_img_phase_{exp_name}/t={plot_t_step}"
    os.makedirs(path, exist_ok=True)
    return path


# 位相ごとの3次元プロットデータの保存場所
def config_heatmap_save_path(exp_name, plot_t_step):
    # 実験データの保存先のフォルダーがなければ作成する
    path = f"result/{exp_name}/heatmap_phase_{exp_name}/t={plot_t_step}"
    os.makedirs(path, exist_ok=True)
    return path


# # 結合後のpdfの保存場所
# def config_marge_pdf_save_path_file_name(exp_name, day=datetime.date.today()):
#     # 実験データの保存先のフォルダーがなければ作成する
#     path = f"result/{exp_name}/save_data/plot_marge_pdf/{day}"
#     os.makedirs(path, exist_ok=True)
#     return path


# 結合後のgifの保存場所
def config_marge_gif_save_path_file_name(exp_name):
    # 実験データの保存先のフォルダーがなければ作成する
    path = f"result/{exp_name}/plot_gif_{exp_name}/"
    os.makedirs(path, exist_ok=True)
    return path


# 結合後のgif_phaseの保存場所
def config_marge_gif_phase_save_path_file_name(exp_name):
    # 実験データの保存先のフォルダーがなければ作成する
    path = f"result/{exp_name}/plot_gif_phase_{exp_name}/"
    os.makedirs(path, exist_ok=True)
    return path


# gif_heatmapの保存場所
def config_gif_heatmap_save_path(exp_name):
    # 実験データの保存先のフォルダーがなければ作成する
    path = f"result/{exp_name}/heatmap_gif_phase_{exp_name}/"
    os.makedirs(path, exist_ok=True)
    return path
