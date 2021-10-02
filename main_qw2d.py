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
    def eqw_simulation():
        # 電場を消し去る場合のシミュレーション
        # select_exp_index_list = list(range(10, 21))
        select_exp_index_list = [59]
        # erase_tステップ目から電場を消し去る
        erase_t = 50
        print(select_exp_index_list)
        selected_conditions, exp_name = exp_017(exp_index_list=select_exp_index_list, erase_t=erase_t)
        execute_simulation(exact_condition_list=selected_conditions)


    def qw_simulation():
        # 電場を消し去らない場合のシミュレーション
        select_exp_index_list = [59]
        print(select_exp_index_list)
        selected_conditions, exp_name = exp_017(exp_index_list=select_exp_index_list)
        execute_simulation(exact_condition_list=selected_conditions)


    def plot_all(select_exp_index_list, exp_name):
        # plotしたいexp_nameのexp_indexを指定する
        select_plot_exp_index = select_exp_index_list
        execute_plot_surface(exp_name=exp_name, plot_exp_index_list=select_plot_exp_index)
        make_gif_surface(exp_name=exp_name, plot_exp_index_list=select_plot_exp_index)
        #
        # execute_plot_surface_by_phase(exp_name=exp_name, plot_t_step=100)
        # make_gif_surface_by_phase(exp_name=exp_name, plot_t_step=100)
        #
        # execute_plot_heatmap_by_phase(exp_name=exp_name, plot_t_step=100)
        # make_gif_heatmap_by_phase(exp_name=exp_name, plot_t_step=100)
