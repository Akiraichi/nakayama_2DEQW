# exp_setting
from exp_setting.exp import *
# simulation
from simulation.simulation import execute_simulation_memory_save
# plot
from analyze.visualization.plot_surface import execute_plot_surface
from analyze.visualization.plot_surface_by_phase import execute_plot_surface_by_phase
from analyze.visualization.plot_heatmap_by_phase import execute_plot_heatmap_by_phase
# gif
from analyze.visualization.make_gif import make_gif_surface, make_gif_surface_by_phase, make_gif_heatmap_by_phase

if __name__ == '__main__':
    # デバッグ1
    select_exp_index = list(range(20))
    selected_conditions, exp_name = exp_016_01_00_x_set_debug(select_exp_index)
    execute_simulation_memory_save(selected_conditions)

    # plotしたいexp_nameのexp_indexを指定する
    select_plot_exp_index = [0, 1, 2]
    execute_plot_surface(exp_name, select_plot_exp_index)
    make_gif_surface(exp_name)

    execute_plot_surface_by_phase(exp_name, 100)
    make_gif_surface_by_phase(exp_name, 100)

    execute_plot_heatmap_by_phase(exp_name, t_step=100)
    make_gif_heatmap_by_phase(exp_name, 100)
