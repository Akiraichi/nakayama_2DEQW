import glob

from config.config import *
import os
from PIL import Image


def check_gif_progress(exp_name, exp_index):
    # plotがどこまで進んだかをチェックし途中から再開するために、
    # plotのexp_indexのフォルダが既に存在しており、plot数が足りていたらそのplotはは既に終了しているとする。
    finished = False
    # ファイルが存在するかをチェックする
    if os.path.isfile(f'{config_gif_save_path_file_name(exp_name=exp_name)}/{str(exp_index).zfill(2)}.gif'):
        finished = True
        print_green_text(f"exp_index={exp_index}：既に完了")

    return finished


class Make_gif:
    def __init__(self):
        self.exp_name = None
        self.plot_exp_index = None
        self.duration = None

    def set_up_conditions(self, exp_name, plot_exp_index, duration):
        self.exp_name = exp_name
        self.plot_exp_index = plot_exp_index
        self.duration = duration

    def check_gif_progress(self):
        # plotがどこまで進んだかをチェックし途中から再開するために、
        # plotのexp_indexのフォルダが既に存在しており、plot数が足りていたらそのplotはは既に終了しているとする。
        finished = False
        # ファイルが存在するかをチェックする
        if os.path.isfile(
                f'{config_gif_save_path_file_name(exp_name=self.exp_name)}/{str(self.plot_exp_index).zfill(2)}.gif'):
            finished = True
            print_green_text(f"exp_index={self.plot_exp_index}：既に完了")

        return finished

    def plot_surface(self):
        print(f"START：exp_index={self.plot_exp_index}")
        # 全ファイル名を取得
        file_name_list = glob.glob(f"{config_surface_save_path(exp_name=self.exp_name, index=self.plot_exp_index)}/*")
        file_name_list.sort()

        frames = []
        for file_name in file_name_list:
            new_frame = Image.open(file_name)
            frames.append(new_frame)
        frames[0].save(
            f'{config_gif_save_path_file_name(exp_name=self.exp_name)}/{str(self.plot_exp_index).zfill(2)}.gif',
            format='GIF',
            append_images=frames[1:],
            save_all=True,
            duration=self.duration,
            loop=0)
        print_finish("make_gif_surface")


def make_gif_surface(exp_name, plot_exp_index_list, duration=50):
    for plot_exp_index in plot_exp_index_list:
        plotter = Make_gif()
        if plotter.check_gif_progress():
            continue
        plotter.set_up_conditions(exp_name=exp_name, plot_exp_index=plot_exp_index, duration=duration)
        plotter.plot_surface()


def make_gif_surface_by_phase(exp_name, plot_t_step, duration=100):
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
    print_finish("make_gif_surface_by_phase")


def make_gif_heatmap_by_phase(exp_name, plot_t_step, duration=100):
    """
    :param exp_name:
    :param plot_t_step:
    :param duration: gif動画のスピード
    :return:
    """
    plot_path_list = glob.glob(f"{config_heatmap_save_path(exp_name=exp_name, plot_t_step=plot_t_step)}/*")
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
    print_finish("make_gif_heatmap_by_phase")
