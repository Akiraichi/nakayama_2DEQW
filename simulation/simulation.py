from config.config import *
from simulation.algorithm import simulation_QW2D
from simulation.save import save_data, exp_data_pack_memory_save
from multiprocessing import Pool
import glob


class Simulation_qw:
    def __init__(self):
        self.exp_conditions = None
        self.start_step_t = None
        self.p = None

    def set_up_conditions(self, exp_conditions, start_step_t):
        self.exp_conditions = exp_conditions
        self.start_step_t = start_step_t

    def start_parallel_processing(self):
        # 並列処理させるために、かくプロセスに渡す引数を生成する
        arguments = []
        for condition in self.exp_conditions:
            arguments.append([condition, self.start_step_t])

        # 最大並列数を設定
        self.p = Pool(Config_simulation.simulation_parallel_num)
        # 並列処理を開始する
        self.p.map(wrapper_simulation, arguments)

        # 処理完了後にprocessをclose
        print_finish("execute_simulation")
        self.p.close()
        self.p.terminate()


def wrapper_simulation(args):
    return exact_simulation(*args)


class qw_2d_simulation:
    def __init__(self):
        self.start_step_t = None
        self.condition = None
        self.exp_index = None
        self.exp_name = None
        self.T = None

    def set_up_condition(self, condition, start_step_t):
        self.start_step_t = start_step_t
        self.condition = condition
        self.exp_index = condition.exp_index
        self.exp_name = condition.exp_name
        self.T = condition.T

    def check_finished(self):
        folder_path = config_simulation_data_save_path(self.exp_name, self.exp_index)
        file_list = glob.glob(f"{folder_path}/*")
        # シミュレーションデータ数が必要な数と一致しているかをチェックする。envファイルがあるので＋1する。0〜600で601
        need_file_num = self.T + 1 + 1
        file_num = len(file_list)
        print(f"exp_index={self.exp_index}のデータ数：{file_num}")
        print(f"必要なデータ数：{need_file_num}")

        finished = False
        if need_file_num == file_num:
            print_green_text(f"exp_index={self.exp_index}：既に完了")
            finished = True
        return finished

    def run(self):
        # シミュレーション実行
        print(f"START：exp_index={self.exp_index}：simulation")
        simulation_QW2D(self.condition, self.start_step_t)

    def save(self):
        # 実験条件を保存する
        data = exp_data_pack_memory_save(exp_name=self.exp_name, condition=self.condition, T=self.T,
                                         len_x=2 * self.T + 1,
                                         len_y=2 * self.T + 1)
        save_data(data=data, path=config_simulation_data_save_path(self.exp_name, self.exp_index),
                  file_name=config_simulation_data_name(index=self.exp_index))
        print_finish(f"exp_index={self.exp_index}")


def start_simulation_2dqw(exp_conditions, start_step_t=0):
    simulation = Simulation_qw()
    simulation.set_up_conditions(exp_conditions, start_step_t)
    simulation.start_parallel_processing()


def exact_simulation(condition, start_step_t):
    simulation = qw_2d_simulation()
    simulation.set_up_condition(condition, start_step_t)
    if not simulation.check_finished():
        simulation.run()
        simulation.save()
    else:
        return

# def exact_simulation(condition, continue_t):
#     # 展開
#     exp_index = condition.exp_index
#     exp_name = condition.exp_name
#     T = condition.T
#
#     # シミュレーションが完了していたらスキップする
#     if check_simulation_progress(exp_index, T, exp_name):
#         return
#
#     # シミュレーション実行
#     print(f"START：exp_index={exp_index}：simulation")
#     simulation_QW2D(condition, continue_t)
#     # 実験条件を保存する
#     data = exp_data_pack_memory_save(exp_name=exp_name, condition=condition, T=T,
#                                      len_x=2 * T + 1,
#                                      len_y=2 * T + 1)
#     save_data(data=data, path=config_simulation_data_save_path(exp_name, exp_index),
#               file_name=config_simulation_data_name(index=exp_index))
#     print_finish(f"exp_index={exp_index}")


# def simulation_2dqw(exp_conditions, start_step_t):
#     # 並列処理させるために、かくプロセスに渡す引数を生成する
#     arguments = []
#     for condition in exp_conditions:
#         arguments.append([condition, start_step_t])
#
#     # 並列処理を開始する
#     # 最大並列数を設定
#     p = Pool(config.config.Config_simulation.simulation_parallel_num)
#     p.map(wrapper_simulation, arguments)
#     # processをclose
#     print_finish("execute_simulation")
#     p.close()
#     p.terminate()


# def execute_simulation(exact_condition_list, continue_t=0):
#     # 並列処理用の前処理
#     arguments = []
#     for condition in exact_condition_list:
#         arguments.append([condition, continue_t])
#
#     # 最大並列数を設定
#     p = Pool(config.config.Config_simulation.simulation_parallel_num)
#     p.map(wrapper_simulation, arguments)
#     # processをclose
#     print_finish("execute_simulation")
#     p.close()
#     p.terminate()


# def check_simulation_progress(exp_index, T, exp_name):
#     # シミュレーションがどこまで進んだかをチェックし途中から再開するために、
#     finished = False
#     folder_path = config_simulation_data_save_path(exp_name, exp_index)
#     file_list = glob.glob(f"{folder_path}/*")
#     # シミュレーションデータ数が必要な数と一致しているかをチェックする。envファイルがあるので＋1する。0〜600で601
#     need_file_num = T + 1 + 1
#     file_num = len(file_list)
#     print(f"exp_index={exp_index}のデータ数：{file_num}")
#     print(f"必要なデータ数：{need_file_num}")
#     if need_file_num == file_num:
#         print_green_text(f"exp_index={exp_index}：既に完了")
#         finished = True
#     return finished
