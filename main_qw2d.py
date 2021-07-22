# exp_setting
from exp_setting.exp import *
# simulation
from simulation.simulation import execute_simulation
# plot
from analyze.visualization.plot_surface import execute_plot_surface
from analyze.visualization.plot_surface_by_phase import execute_plot_surface_by_phase
from analyze.visualization.plot_heatmap_by_phase import execute_plot_heatmap_by_phase
# gif
from analyze.visualization.make_gif import make_gif_surface, make_gif_surface_by_phase, make_gif_heatmap_by_phase

if __name__ == '__main__':

    select_exp_index_list = list(range(10, 21))
    print(select_exp_index_list)
    selected_conditions, exp_name = exp_016_01_00_x_set_debug(select_exp_index_list)
    execute_simulation(exact_condition_list=selected_conditions)

    # plotしたいexp_nameのexp_indexを指定する
    select_plot_exp_index = select_exp_index_list
    execute_plot_surface(exp_name=exp_name, plot_exp_index_list=select_plot_exp_index)
    make_gif_surface(exp_name=exp_name,plot_exp_index_list=select_plot_exp_index)

    execute_plot_surface_by_phase(exp_name=exp_name, plot_t_step=100)
    make_gif_surface_by_phase(exp_name=exp_name, plot_t_step=100)

    execute_plot_heatmap_by_phase(exp_name=exp_name, plot_t_step=100)
    make_gif_heatmap_by_phase(exp_name=exp_name, plot_t_step=100)
