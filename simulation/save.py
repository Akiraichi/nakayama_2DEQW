import joblib
from config.config import config_simulation_save_mamory_data_save_path


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


def save_t_step_psy(psy, t, exp_name, i):
    """

    :param psy: tステップのpsy
    :param t: tステップのt
    :param path: 保存場所のpath
    :param exp_name:
    :return:
    """
    path = config_simulation_save_mamory_data_save_path(exp_name, i)
    t = str(t).zfill(3)
    joblib.dump(psy, f"{path}/{t}.jb", compress=3)
