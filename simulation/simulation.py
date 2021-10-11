import config.config
from config.config import *
from simulation.algorithm import simulation_QW2D
from simulation.save import save_data, exp_data_pack_memory_save
from multiprocessing import Pool
import glob


def execute_simulation(exact_condition_list, continue_t=0):
    # 並列処理用の前処理
    arguments = []
    for condition in exact_condition_list:
        arguments.append([condition, continue_t])

    # 最大並列数を設定
    p = Pool(config.config.Config_simulation.simulation_parallel_num)
    p.map(wrapper_simulation, arguments)
    # processをclose
    print_finish("execute_simulation")
    p.close()
    p.terminate()


# wrapper
def wrapper_simulation(args):
    return parallel_start_simulation_program(*args)


def check_simulation_progress(exp_index, T, exp_name):
    # シミュレーションがどこまで進んだかをチェックし途中から再開するために、
    finished = False
    folder_path = config_simulation_data_save_path(exp_name, exp_index)
    file_list = glob.glob(f"{folder_path}/*")
    # シミュレーションデータ数が必要な数と一致しているかをチェックする。envファイルがあるので＋1する。0〜600で601
    need_file_num = T + 1 + 1
    file_num = len(file_list)
    print(f"exp_index={exp_index}のデータ数：{file_num}")
    print(f"必要なデータ数：{need_file_num}")
    if need_file_num == file_num:
        print_green_text(f"exp_index={exp_index}：既に完了")
        finished = True
    return finished


def parallel_start_simulation_program(condition, continue_t):
    # 展開
    exp_index = condition.exp_index
    exp_name = condition.exp_name
    T = condition.T

    # シミュレーションが完了していたらスキップする
    if check_simulation_progress(exp_index, T, exp_name):
        return

    # シミュレーション実行
    print(f"START：exp_index={exp_index}：simulation")
    simulation_QW2D(condition, continue_t)
    # 実験条件を保存する
    data = exp_data_pack_memory_save(exp_name=exp_name, condition=condition, T=T,
                                     len_x=2 * T + 1,
                                     len_y=2 * T + 1)
    save_data(data=data, path=config_simulation_data_save_path(exp_name, exp_index),
              file_name=config_simulation_data_name(index=exp_index))
    print_finish(f"exp_index={exp_index}")
