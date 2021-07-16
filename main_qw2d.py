# exp_setting
import config.config
from exp_setting.exp import *
# simulation
from simulation.simulation_mamoery_save import execute_simulation_memory_save
# plot
from analyze.visualization.plot_memory_save import execute_plot_memory_save_2
from analyze.visualization.plot_phase_save import execute_plot_phase
# gif
from analyze.visualization.make_gif import make_gif, make_gif_phase


def main_loop(conditions, exp_name):
    while True:
        try:
            print("simuのスタート")
            execute_simulation_memory_save(conditions, exp_name)

            print("plotのスタート")
            execute_plot_memory_save_2(exp_name)

            print("gifのスタート")
            make_gif(exp_name)
        except Exception as e:
            print("Error発生")
            print(e)
            # システムをリスタートする
            import os
            import sys

            os.execl(sys.executable, 'python3', __file__)
        else:
            print('finish (no error)')
            print("システム完了")
            break


def main_loop_phase(conditions, exp_name):
    while True:
        try:
            print("simuのスタート")
            execute_simulation_memory_save(conditions, exp_name)

            for plot_t_step in [100, 200, 300, 400, 500, 599]:
                print("plotのスタート")
                execute_plot_phase(exp_name, plot_t_step)
                print("gifのスタート")
                make_gif_phase(exp_name, plot_t_step)

        except Exception as e:
            print("Error発生")
            print(e)
            # システムをリスタートする
            import os
            import sys

            os.execl(sys.executable, 'python3', __file__)
        else:
            print('finish (no error)')
            print("システム完了")
            break


if __name__ == '__main__':
    # デバッグ1
    conditions, exp_name = exp_5010_x_set(start_index=61, end_index=81)
    main_loop_phase(conditions, exp_name)

    # execute_plot_memory_save_2(exp_name=exp_name)
    # main_loop_phase(conditions, exp_name)
    # execute_plot_phase(exp_name, 9)
    # デバッグ2
    # conditions, exp_name = exp_0000__debug_folder_changed_check_set()
    # main_loop(conditions, exp_name)

    # デバッグ3
    # plot_t_step = 99
    # make_gif_phase(exp_name=exp_name, plot_t_step=plot_t_step)
