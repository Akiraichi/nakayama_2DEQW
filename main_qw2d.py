# exp_setting
from exp_setting.exp import *
# simulation
from simulation.simulation_mamoery_save import execute_simulation_memory_save
# plot
from analyze.visualization.plot_memory_save import execute_plot_memory_save_2
from analyze.visualization.plot_phase_save import execute_plot_phase
from analyze.visualization.plot_heatmap import execute_plot_heatmap
# gif
from analyze.visualization.make_gif import make_gif, make_gif_phase, make_gif_heatmap

if __name__ == '__main__':
    # デバッグ1
    conditions, exp_name = exp_016_01_00_x_set_debug(60,61)
    execute_simulation_memory_save(conditions, exp_name)

    # execute_plot_memory_save_2(exp_name)
    # make_gif(exp_name)

    execute_plot_phase(exp_name, 100)
    # make_gif_phase(exp_name, 100)

    # execute_plot_heatmap(exp_name, t_step=100)
    # make_gif_heatmap(exp_name, 100)
