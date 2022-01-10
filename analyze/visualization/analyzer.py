from helper import save_jb_file, load_file_by_error_handling


# 旧形式のデータ構造に対応するためのファイル

class AnalyzeData:
    def __init__(self, **data):
        self.__KL_div = data["KL_div"]
        self.__L1_norm = data["L1_norm"]
        self.__L2_norm = data["L2_norm"]
        self.__correlation_coefficient = data["correlation_coefficient"]
        self.__t = data["t"]

    def save(self, folder_path, file_name):
        """現在のインスタンスを保存する"""
        save_jb_file(self, folder_path, file_name)

    @staticmethod
    def load(folder_path, file_name):
        """保存したAnalyzeDataインスタンスを返却する"""
        return load_file_by_error_handling(f"{folder_path}/{file_name}")

    @property
    def KL_div(self):
        return self.__KL_div

    @property
    def L1_norm(self):
        return self.__L1_norm

    @property
    def L2_norm(self):
        return self.__L2_norm

    @property
    def correlation_coefficient(self):
        return self.__correlation_coefficient

    @property
    def t(self):
        return self.__t
