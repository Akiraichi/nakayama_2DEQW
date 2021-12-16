from config.config import *
from simulation.simulation_core import calculate_QW2D
from simulation.save import save_data, exp_data_pack_memory_save
from multiprocessing import Pool
import glob
import numpy as np
import joblib


def start_simulation_2dqw(exp_conditions, start_step_t):
    simulation = Simulation_qw()
    simulation.set_up_conditions(exp_conditions, start_step_t)
    simulation.start_parallel_processing()


class Simulation_qw:
    def __init__(self):
        self.exp_conditions = None
        self.start_step_t = None

    def set_up_conditions(self, exp_conditions, start_step_t):
        self.exp_conditions = exp_conditions
        self.start_step_t = start_step_t

    def start_parallel_processing(self):
        # 並列処理させるために、かくプロセスに渡す引数を生成する
        arguments = []
        for condition in self.exp_conditions:
            arguments.append([condition, self.start_step_t])
        with Pool(ConfigSimulation.SimulationParallelNum) as p:
            p.starmap(func=Simulation_qw.main_simulation, iterable=arguments)
        print_finish("execute_simulation")

    @staticmethod
    def main_simulation(condition, start_step_t):
        simulation = qw_2d_simulation()
        simulation.set_up_condition(condition, start_step_t)
        if simulation.check_finished():
            return
        else:
            simulation.initialize()
            simulation.run()
            # simulation.save_env_file()


class qw_2d_simulation:
    def __init__(self):
        self.start_step_t = None
        self.erase_time_step = None

        self.condition = None
        self.exp_index = None
        self.exp_name = None
        self.T = None

        self.P = None
        self.Q = None
        self.R = None
        self.S = None
        self.PSY_init = None
        self.Algorithm = None
        self.phi = None
        self.erase_t = None
        self.init_vector = None

        self.init_PSY_now = None
        self.start_t = None

    def set_up_condition(self, condition, start_step_t):
        self.start_step_t = start_step_t

        # 展開する
        self.condition = condition
        self.exp_index = condition.exp_index
        self.exp_name = condition.exp_name
        self.T = condition.T

        # 以下、展開するもののうち、アルゴリズムで使用する変数群
        self.P = condition.P
        self.Q = condition.Q
        self.R = condition.R
        self.S = condition.S
        self.PSY_init = condition.PSY_init
        self.Algorithm = condition.algorithm
        self.phi = condition.phi
        self.erase_t = condition.erase_t
        self.erase_time_step = condition.erase_time_step  # 電場を消すのにかける時間ステップ数
        self.init_vector = np.zeros_like(self.PSY_init, dtype=np.complex128)  # その他の場所の確率振幅ベクトルの設定

    def initialize(self):
        """
        途中からシミュレーションしたい時は、どこから始めるかを指定するようにした。
        continue_tステップ目から再開する。
        continue_t=99なら、98ステップをロードし、99ステップのシミュレーションから開始する
        """

        """初期データを保存する。あるいは途中データをロードする"""
        if self.start_step_t == 0:
            # 既に完了したシミュレーションが0。つまり完全新規のシミュレーション
            # 一つ前の時刻と今の時刻と2ステップ分だけメモリを用意する[時間ステップ, x, y, 4成分]
            self.init_PSY_now = np.zeros([2 * self.T + 1, 2 * self.T + 1, 4], dtype=np.complex128)
            # t=0でx=0,y=0の位置にいる。成分はPSY_init
            self.init_PSY_now[0 + self.T, 0 + self.T] = self.PSY_init
            # ここでセーブする。保存するのは初期状態のPSY
            self.save(psy=self.init_PSY_now, t=0)
            self.start_t = 1
        else:
            # 途中からシミュレーションを再開
            path = f"{config_simulation_data_save_path(self.exp_name, str(self.start_step_t - 1).zfill(4), self.exp_index)}/{str(self.start_step_t - 1).zfill(4)}.jb"
            print(path)
            self.init_PSY_now = joblib.load(path)["シミュレーションデータ"]
            self.start_t = self.start_step_t

    def check_finished(self):
        """
        self.Tが600なら、00、01、02、03、04、05、06のサブフォルダがあり、それぞれに100こずつデータが入っているだろう（06は1個）
        """
        finished = True
        for i in range(0, (self.T // 100) + 1):  # range(0,2)なら0,1で2がないから。
            str_t = str(i).zfill(2)
            # それぞれにデータが必要個数入っているかを確認する
            folder_path = config_simulation_data_save_path(self.exp_name, str_t, self.exp_index)
            file_list = glob.glob(f"{folder_path}/*")
            # シミュレーションデータ数が必要な数と一致しているかをチェックする。envファイルがあるので＋1する。0〜600で601
            if i == self.T // 100:
                # 600で1個
                need_file_num = 1
            else:
                # 0~99で100個
                need_file_num = 100
            file_num = len(file_list)
            print(f"exp_index={self.exp_index}, {str_t}, のデータ数：{file_num}")
            print(f"必要なデータ数：{need_file_num}")
            if need_file_num != file_num:
                finished = False

        if finished:
            print_green_text(f"exp_index={self.exp_index}：既に完了")
        else:
            print_warning(f"exp_index={self.exp_index}：完了していません")
        return finished

    def run(self):
        # シミュレーション実行
        print(f"START：exp_index={self.exp_index}：simulation")
        # 繰り返し回数はT+1回。現在時刻を0次の時刻を1に代入する
        PSY_now = self.init_PSY_now
        for t in range(self.start_t, self.T + 1):
            PSY_next = np.zeros([2 * self.T + 1, 2 * self.T + 1, 4], dtype=np.complex128)
            print(f"{t}：ステップ")
            PSY_now = calculate_QW2D(self.T, self.init_vector, self.phi, PSY_now, PSY_next, self.Algorithm,
                                     P=self.P, Q=self.Q, R=self.R, S=self.S, t=t, erase_t=self.erase_t,
                                     erase_time_step=self.erase_time_step)
            # ここでセーブする。保存するのはt+1ステップめ（なぜ＋1するのかというと初期値で一回保存しているから）
            self.save(psy=PSY_now, t=t)

    def save(self, psy, t):
        t = str(t).zfill(4)

        simulation_data_save_path = f"{config_simulation_data_save_path(self.exp_name, t[:2], self.exp_index)}/{t}.jb"
        data_dict = {
            "シミュレーションデータ": psy,
            "実験条件データ（condition）": self.condition,
            "このシミュレーションデータが何ステップ目か（t）": t
        }
        joblib.dump(data_dict, simulation_data_save_path, compress=3)

    # def save_env_file(self):
    #     # 実験条件を保存する
    #     data = exp_data_pack_memory_save(exp_name=self.exp_name, condition=self.condition, T=self.T,
    #                                      len_x=2 * self.T + 1,
    #                                      len_y=2 * self.T + 1)
    #     save_data(data=data, path=config_simulation_data_save_path(self.exp_name, self.exp_index),
    #               file_name=config_simulation_data_name(index=self.exp_index))
    #     print_finish(f"exp_index={self.exp_index}")
