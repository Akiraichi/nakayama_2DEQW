import glob

from config.config import config_marge_gif_save_path_file_name, config_plot_save_path, config_plot_phase_save_path, \
    config_marge_gif_phase_save_path_file_name, config_heat_map_save_path, config_gif_heatmap_save_path
import os
from PIL import Image


def check_gif_progress(exp_name, index):
    # plotがどこまで進んだかをチェックし途中から再開するために、
    # plotのindexのフォルダが既に存在しており、plot数が足りていたらそのplotはは既に終了しているとする。
    finished = False
    # ファイルが存在するかをチェックする
    if os.path.isfile(f'{config_marge_gif_save_path_file_name(exp_name=exp_name)}/{str(index).zfill(2)}.gif'):
        finished = True
    return finished


def make_gif(exp_name, duration=50):
    dir_name_list = glob.glob(f"{config_plot_save_path(exp_name=exp_name)}/*")
    for index, _ in enumerate(dir_name_list):
        # gifをどこまで作成したかチェックし続きから実行する
        if check_gif_progress(exp_name, index):
            print(f"{index}回目：既に完了しています")
            continue

        print(f"{index}回目：実行")
        # 全ファイル名を取得
        file_name_list = glob.glob(f"{config_plot_save_path(exp_name=exp_name, index=index)}/*")
        file_name_list.sort()

        frames = []
        for file_name in file_name_list:
            new_frame = Image.open(file_name)
            frames.append(new_frame)
        frames[0].save(f'{config_marge_gif_save_path_file_name(exp_name=exp_name)}/{str(index).zfill(2)}.gif',
                       format='GIF',
                       append_images=frames[1:],
                       save_all=True,
                       duration=duration,
                       loop=0)
        print(f"{index}回目：完了")


def make_gif_phase(exp_name, plot_t_step, duration=100):
    """
    :param exp_name:
    :param plot_t_step:
    :param duration: gif動画のスピード
    :return:
    """
    plot_path_list = glob.glob(f"{config_plot_phase_save_path(exp_name=exp_name, plot_t_step=plot_t_step)}/*")
    plot_path_list.sort()
    frames = []
    for plot_path in plot_path_list:
        new_frame = Image.open(plot_path)
        frames.append(new_frame)
    file_name = f"t={plot_t_step}"
    frames[0].save(f'{config_marge_gif_phase_save_path_file_name(exp_name=exp_name)}/{file_name}.gif',
                   format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=duration,
                   loop=0)


def make_gif_heatmap(exp_name, plot_t_step, duration=100):
    """
    :param exp_name:
    :param plot_t_step:
    :param duration: gif動画のスピード
    :return:
    """
    plot_path_list = glob.glob(f"{config_heat_map_save_path(exp_name=exp_name, plot_t_step=plot_t_step)}/*")
    plot_path_list.sort()
    frames = []
    for plot_path in plot_path_list:
        new_frame = Image.open(plot_path)
        frames.append(new_frame)
    file_name = f"t={plot_t_step}"
    frames[0].save(f'{config_gif_heatmap_save_path(exp_name=exp_name)}/{file_name}.gif',
                   format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=duration,
                   loop=0)
