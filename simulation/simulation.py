from config.config_simulation import ConfigSimulationSetting, config_simulation_data_save_path
from helper import helper
from simulation.simulation_algorithm import calculate_QW2D
import glob
import numpy as np
from concurrent.futures import ProcessPoolExecutor


class SimulationQWAgent:
    """
    QWをシミュレーションする関数群のクラス
    """

    def __init__(self, conditions, start_step_t):
        self.__conditions = conditions
        self.__start_step_t = start_step_t

    def start_parallel_processing(self):
        with ProcessPoolExecutor(max_workers=ConfigSimulationSetting.SimulationParallelNum) as e:
            for condition in self.__conditions:
                e.submit(SimulationQWAgent.main_simulation, condition, self.__start_step_t)

    @staticmethod
    def check_finished(T, exp_name, exp_index):
        """
        self.Tが600なら、00、01、02、03、04、05、06のサブフォルダがあり、それぞれに100こずつデータが入っているだろう（06は1個）
        """
        finished = True
        for i in range(0, (T // 100) + 1):  # range(0,2)なら0,1で2がないから。
            str_t = str(i).zfill(2)
            # それぞれにデータが必要個数入っているかを確認する
            folder_path = config_simulation_data_save_path(exp_name, str_t, exp_index)
            file_list = glob.glob(f"{folder_path}/*")
            # シミュレーションデータ数が必要な数と一致しているかをチェックする。envファイルがあるので＋1する。0〜600で601
            if i == T // 100:
                # 600で1個
                need_file_num = 1
            else:
                # 0~99で100個
                need_file_num = 100
            file_num = len(file_list)
            print(f"exp_index={exp_index}, {str_t}, のデータ数：{file_num}")
            print(f"必要なデータ数：{need_file_num}")
            if need_file_num != file_num:
                finished = False

        if finished:
            helper.print_green_text(f"exp_index={exp_index}：既に完了")
        else:
            helper.print_warning(f"exp_index={exp_index}：完了していません")
        return finished

    @classmethod
    def set_start_point(cls, start_step_t, condition):
        """
        途中からシミュレーションしたい時は、どこから始めるかを指定するようにした。
        continue_tステップ目から再開する。
        continue_t=99なら、98ステップをロードし、99ステップのシミュレーションから開始する
        """

        """初期データを保存する。あるいは途中データをロードする"""
        # conditionを展開する
        # exp_name = condition.exp_name
        # exp_index = condition.exp_index
        # T = condition.T
        # PSY_init = condition.PSY_init

        if start_step_t == 0:
            # # 既に完了したシミュレーションが0。つまり完全新規のシミュレーション
            # # 一つ前の時刻と今の時刻と2ステップ分だけメモリを用意する[時間ステップ, x, y, 4成分]
            # init_PSY_now = np.zeros([2 * T + 1, 2 * T + 1, 4], dtype=np.complex128)
            # # t=0でx=0,y=0の位置にいる。成分はPSY_init
            # init_PSY_now[0 + T, 0 + T] = PSY_init
            # # ここでセーブする。保存するのは初期状態のPSY
            # cls.save(psy=init_PSY_now, t=0, condition=condition)
            PSY = cls.create_initial_PSY(condition)
            cls.save_initial_PSY(PSY, condition)
            start_t = 1
        else:
            # # 途中からシミュレーションを再開
            # path = f"{config_simulation_data_save_path(exp_name, str(start_step_t - 1).zfill(4), exp_index)}/{str(start_step_t - 1).zfill(4)}.jb"
            # print(path)
            # # init_PSY_now = helper.load_file_by_error_handling(file_path=path)["シミュレーションデータ"]
            # PSY = helper.load_file_by_error_handling(file_path=path)["シミュレーションデータ"]
            PSY = cls.restart_simulation(condition, start_step_t)
            start_t = start_step_t

        return PSY, start_t

    @staticmethod
    def restart_simulation(condition, start_step_t):
        """途中からシミュレーションを再開する"""
        # 再開する一つ前の時間ステップのデータへのパスを取得する
        path = f"{config_simulation_data_save_path(condition.exp_name, str(start_step_t - 1).zfill(4), condition.exp_index)}{str(start_step_t - 1).zfill(4)}.jb"
        print(path)
        # データをロードする
        PSY = helper.load_file_by_error_handling(file_path=path)["シミュレーションデータ"]
        return PSY

    @staticmethod
    def create_initial_PSY(condition):
        """初期確率振幅ベクトルを作成する"""
        # 初期確率振幅ベクトルは原点以外全て0であるため、0で初期化する。[x座標, y座標, 4成分]。座標は-Tをindexの0番、+Tを2T+1番とするように処理する。
        PSY = np.zeros([2 * condition.T + 1, 2 * condition.T + 1, 4], dtype=np.complex128)

        # 量子ウォーカーは、t=0では原点のみに位置しており、初期状態はPSY_initで指定される
        PSY[0 + condition.T, 0 + condition.T] = condition.PSY_init
        return PSY

    @classmethod
    def save_initial_PSY(cls, PSY, condition):
        """初期確率振幅ベクトルを保存する"""
        # ここでセーブする。保存するのは初期状態のPSY
        cls.save(psy=PSY, t=0, condition=condition)

    @staticmethod
    def save(psy, t, condition):
        exp_name = condition.exp_name
        exp_index = condition.exp_index
        t = str(t).zfill(4)
        data_dict = {
            "シミュレーションデータ": psy,
            "実験条件データ（condition）": condition,
            "このシミュレーションデータが何ステップ目か（t）": t
        }

        helper.save_jb_file(data_dict=data_dict,
                            path_to_file=f"{config_simulation_data_save_path(exp_name, t[:2], exp_index)}",
                            file_name=f"{t}.jb")

    @staticmethod
    def main_simulation(condition, start_step_t):
        # conditionを展開する
        T = condition.T  # 最大時間ステップT（Tステップを実行してT+1ステップ目は実行せずに終了）
        exp_name = condition.exp_name
        exp_index = condition.exp_index
        PSY_init = condition.PSY_init  # 初期確率分布
        phi = condition.phi  # 電場の位相
        algorithm = condition.algorithm
        erase_t = condition.erase_t  # erase_tステップ目に電場を消す。
        P = condition.P
        Q = condition.Q
        R = condition.R
        S = condition.S
        erase_time_step = condition.erase_time_step  # 電場を消すのにかける時間ステップ数

        # 初期化する
        init_vector = np.zeros_like(PSY_init, dtype=np.complex128)

        if SimulationQWAgent.check_finished(T=T, exp_name=exp_name, exp_index=exp_index):
            return
        else:
            # 時間発展を開始する初めの時間ステップを設定する。その時の確率振幅ベクトルの状態とt
            init_PSY_now, start_t = SimulationQWAgent.set_start_point(start_step_t=start_step_t, condition=condition)
            # シミュレーション実行
            print(f"START：exp_index={exp_index}：simulation")
            # 繰り返し回数はT+1回。現在時刻を0次の時刻を1に代入する
            PSY_now = init_PSY_now
            for t in range(start_t, T + 1):
                # PSY_next = np.zeros([2 * T + 1, 2 * T + 1, 4], dtype=np.complex128)
                print(f"{t}：ステップ")
                PSY_now = calculate_QW2D(T, init_vector, phi, PSY_now, algorithm,
                                         P=P, Q=Q, R=R, S=S, t=t, erase_t=erase_t,
                                         erase_time_step=erase_time_step)
                # ここでセーブする。保存するのはt+1ステップめ（なぜ＋1するのかというと初期値で一回保存しているから）
                SimulationQWAgent.save(psy=PSY_now, t=t, condition=condition)
