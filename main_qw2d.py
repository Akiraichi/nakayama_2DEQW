# exp_setting
import config.config
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
    conditions, exp_name = exp_5010_x_set(1, 21)
    # execute_simulation_memory_save(conditions, exp_name)
    # execute_plot_memory_save_2(exp_name)
    # execute_plot_phase(exp_name, 100)
    execute_plot_heatmap(exp_name, t_step=100)
    # make_gif(exp_name, 100, 20)
    make_gif_heatmap(exp_name, 100)

    # import joblib
    # from simulation.algorithm_memory_save import calculate_probability_distribution_at_time_t_memory_save
    #
    # T = 100
    # len_x = 201
    # len_y = 201
    # file_name = 'result/exp_5010/simulation_data_exp_5010/00/013.jb'
    # PSY = joblib.load(file_name)
    # mesh_x, mesh_y = np.meshgrid(np.linspace(-T, T, 2 * T + 1), np.linspace(-T, T, 2 * T + 1), indexing="ij")
    # mesh_z = calculate_probability_distribution_at_time_t_memory_save(PSY, len_x, len_y)
    #
    # plot_heat_map_probability(mesh_z)
