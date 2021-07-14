import glob
from PyPDF2 import PdfFileMerger
from config.config import *


def marge_pdf(exp_name, day):
    dir_name_list = glob.glob(f"{config_plot_save_path(exp_name=exp_name, day=day)}/*")
    count_dir = len(dir_name_list)
    for index in range(count_dir):
        pdf_file_merger = PdfFileMerger()
        # 全ファイル名を取得
        file_name_list = glob.glob(f"{config_plot_save_path(exp_name=exp_name, index=index, day=day)}/*.pdf")
        # sortする
        file_name_list.sort()

        for file_name in file_name_list:
            pdf_file_merger.append(file_name)
        pdf_file_merger.write(
            f'{config_marge_pdf_save_path_file_name(exp_name=exp_name, day=day)}/{str(index).zfill(2)}.pdf')
        pdf_file_merger.close()
