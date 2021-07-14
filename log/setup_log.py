from logging import getLogger, StreamHandler, Formatter, FileHandler, DEBUG
import os
from config.config import Config_save_log
import datetime


class Log_setting:
    def __init__(self):
        self.path = None
        self.full_path = None
        self.save_setting()
        self.logger = self.setup_logger(self.full_path)

    def save_setting(self):
        # フォルダーがなければ作成する
        self.path = Config_save_log.path
        os.makedirs(self.path, exist_ok=True)
        log_file_name = '{0}.log'.format(datetime.date.today())
        self.full_path = Config_save_log.path + "/" + log_file_name



    def setup_logger(self, log_folder, modname=__name__):
        logger = getLogger(modname)
        logger.setLevel(DEBUG)

        sh = StreamHandler()
        sh.setLevel(DEBUG)
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh.setFormatter(formatter)
        logger.addHandler(sh)

        fh = FileHandler(log_folder)  # fh = file handler
        fh.setLevel(DEBUG)
        fh_formatter = Formatter('%(asctime)s - %(filename)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s')
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)
        return logger
