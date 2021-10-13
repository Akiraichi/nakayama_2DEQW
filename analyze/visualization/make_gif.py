import glob

from config.config import *
import os
from PIL import Image


def make_gif_image(exp_name, plot_type="surface", plot_exp_indexes=None, plot_t_step=None, duration=50):
    """
    plot_t_stepが指定された場合、全てのplot_exp_indexesのtステップのみプロットしgifにまとめる
    """
    if plot_exp_indexes is None:
        plot_exp_indexes = [0]
    plotter = Make_gif()
    plotter.set_up_conditions(exp_name=exp_name, plot_type=plot_type, plot_exp_indexes=plot_exp_indexes,
                              plot_t_step=plot_t_step, duration=duration)
    plotter.make_gif()


class Make_gif:
    def __init__(self):
        self.exp_name = None
        self.plot_type = None
        self.plot_exp_indexes = None
        self.plot_t_step = None
        self.plot_t_step_zfill = None
        self.duration = None
        self.path = None
        self.save_path = None
        self.plot_image_path = None
        self.plot_exp_path = None

    def set_up_conditions(self, exp_name, plot_type, plot_exp_indexes, plot_t_step, duration):
        self.exp_name = exp_name
        self.plot_type = plot_type
        self.plot_exp_indexes = plot_exp_indexes
        self.plot_t_step = plot_t_step
        self.plot_t_step_zfill = str(plot_t_step).zfill(4)
        self.duration = duration

        # 保存先に関する共通事項の設定
        self.path = f'{gif_save_path(exp_name=self.exp_name, plot_type=plot_type)}'
        self.plot_exp_path = f"{plot_save_path(exp_name=self.exp_name, plot_type=plot_type)}/*"

    def check_gif_finished(self, plot_exp_index):
        finished = False
        # ファイルが存在するかをチェックする
        if os.path.isfile(self.save_path):
            finished = True
            print_green_text(f"exp_index={plot_exp_index}：既に完了")
        return finished

    def make_gif(self):
        if self.plot_t_step is None:
            for plot_exp_index in self.plot_exp_indexes:
                self.save_path = self.path + f"{str(plot_exp_index).zfill(2)}.gif"
                if self.check_gif_finished(plot_exp_index):
                    continue
                print(f"START：exp_index={plot_exp_index}")
                # 全ファイル名を取得
                plot_image_path = f"{plot_save_path(exp_name=self.exp_name, plot_type=self.plot_type, index=plot_exp_index)}/*"
                plot_image_names = glob.glob(plot_image_path)

                self.__core_make_gif(plot_image_names)
        else:
            # resultのplotの中にあるexpフォルダ名を取得
            folder_names = glob.glob(self.plot_exp_path)
            plot_image_names = [folder_name + f"/{self.plot_t_step_zfill}.png" for folder_name in folder_names]
            self.save_path = self.path + f"{str(self.plot_t_step).zfill(4)}.gif"
            self.__core_make_gif(plot_image_names)

    def __core_make_gif(self, plot_image_names):
        plot_image_names.sort()
        frames = []
        for plot_image in plot_image_names:
            new_frame = Image.open(plot_image)
            frames.append(new_frame)
        frames[0].save(
            self.save_path,
            format='GIF',
            append_images=frames[1:],
            save_all=True,
            duration=self.duration,
            loop=0)
        print_finish(self.plot_type)

#
# def make_gif_surface_by_phase(exp_name, plot_t_step, duration=100):
#     """
#     :param exp_name:
#     :param plot_t_step:
#     :param duration: gif動画のスピード
#     :return:
#     """
#     plot_path_list = glob.glob(f"{config_plot_phase_save_path(exp_name=exp_name, plot_t_step=plot_t_step)}/*")
#     plot_path_list.sort()
#     frames = []
#     for plot_path in plot_path_list:
#         new_frame = Image.open(plot_path)
#         frames.append(new_frame)
#     file_name = f"t={plot_t_step}"
#     frames[0].save(f'{config_marge_gif_phase_save_path_file_name(exp_name=exp_name)}/{file_name}.gif',
#                    format='GIF',
#                    append_images=frames[1:],
#                    save_all=True,
#                    duration=duration,
#                    loop=0)
#     print_finish("make_gif_surface_by_phase")

#
# def make_gif_heatmap_by_phase(exp_name, plot_t_step, duration=100):
#     """
#     :param exp_name:
#     :param plot_t_step:
#     :param duration: gif動画のスピード
#     :return:
#     """
#     plot_path_list = glob.glob(f"{config_heatmap_save_path(exp_name=exp_name, plot_t_step=plot_t_step)}/*")
#     plot_path_list.sort()
#     frames = []
#     for plot_path in plot_path_list:
#         new_frame = Image.open(plot_path)
#         frames.append(new_frame)
#     file_name = f"t={plot_t_step}"
#     frames[0].save(f'{config_gif_heatmap_save_path(exp_name=exp_name)}/{file_name}.gif',
#                    format='GIF',
#                    append_images=frames[1:],
#                    save_all=True,
#                    duration=duration,
#                    loop=0)
#     print_finish("make_gif_heatmap_by_phase")

#
# def check_gif_progress(exp_name, exp_index):
#     # plotがどこまで進んだかをチェックし途中から再開するために、
#     # plotのexp_indexのフォルダが既に存在しており、plot数が足りていたらそのplotはは既に終了しているとする。
#     finished = False
#     # ファイルが存在するかをチェックする
#     if os.path.isfile(f'{gif_save_path(exp_name=exp_name)}/{str(exp_index).zfill(2)}.gif'):
#         finished = True
#         print_green_text(f"exp_index={exp_index}：既に完了")
#
#     return finished
