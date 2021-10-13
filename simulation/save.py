import joblib


class exp_data_pack:
    def __init__(self, exp_name, condition, PSY, T, len_x, len_y):
        # 実験名
        self.exp_name = exp_name
        # 実験条件
        self.condition = condition
        # シミュレーション後の確率振幅ベクトル
        self.PSY = PSY
        self.T = T
        self.len_x = len_x
        self.len_y = len_y


class exp_data_pack_memory_save:
    """実験条件だけ保存する"""

    def __init__(self, exp_name, condition, T, len_x, len_y):
        # 実験名
        self.exp_name = exp_name
        # 実験条件
        self.condition = condition
        self.T = T
        self.len_x = len_x
        self.len_y = len_y


def save_data(data, path, file_name):
    # いい感じに圧縮して保存してくれます
    joblib.dump(data, f"{path}/{file_name}", compress=3)
