import config.config
from config.config import *
from simulation.algorithm_memory_save import qw2d_simulation_memory_save
from simulation.save import save_data, exp_data_pack_memory_save
from multiprocessing import Pool
import glob


def execute_simulation_memory_save(conditions, exp_name):
    # 並列処理用の前処理
    arguments = []
    for i, condition in enumerate(conditions):
        arguments.append([i, condition, exp_name])

    # 最大並列数を設定
    p = Pool(config.config.Config_simulation.simulation_parallel_num)
    p.map(wrapper_simulation, arguments)
    # processをclose
    p.close()
    p.terminate()


# wrapper
def wrapper_simulation(args):
    return multi_start_simulation_program_memory_save(*args)


def check_simulation_progress(i, condition, exp_name):
    # シミュレーションがどこまで進んだかをチェックし途中から再開するために、
    # シミュレーションのindexのフォルダが既に存在しているのであれば、そのindexのシミュレーションは既に終了しているとする。
    finished = False
    folder_path = config_simulation_save_mamory_data_save_path(exp_name, i)
    file_list = glob.glob(f"{folder_path}/*")
    # シミュレーションによって生じたファイル数が必要な数に達しているかをチェックする。envファイルがあるので＋1する
    if condition.T + 1 == len(file_list):
        finished = True
    return finished


def multi_start_simulation_program_memory_save(i, condition, exp_name):
    # シミュレーションがどこまで進んだかをチェック
    if check_simulation_progress(i, condition, exp_name):
        print(f"{i}回目：既に完了しています")
        # シミュレーションが完了しているので終了する
        return

    # シミュレーション実行
    print(i, "回目：シミュレーション：開始")
    qw2d_simulation_memory_save(condition, exp_name, i)
    # 実験条件を保存する
    data = exp_data_pack_memory_save(exp_name=exp_name, condition=condition, T=Config_simulation.max_time_step,
                                     len_x=2 * Config_simulation.max_time_step + 1,
                                     len_y=2 * Config_simulation.max_time_step + 1)
    save_data(data=data, path=config_simulation_save_mamory_data_save_path(exp_name, i),
              file_name=config_simulation_save_memory_data_name(index=i))
    print(i, "回目：シミュレーションデータの保存：完了")


if __name__ == "__main__":
    from exp_setting.exp import *

    # 実験条件の取得
    conditions, exp_name = exp_2010_x_set()
    # 実験開始
    execute_simulation_memory_save(conditions, exp_name)
