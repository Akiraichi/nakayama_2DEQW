# exp_setting
from analyze.visualization.plot_kl import execute_plot_kl_div
from analyze.visualization.plot_var import execute_plot_var
from exp_setting.exp import *
# simulation
from simulation.simulation import execute_simulation
# plot
from analyze.visualization.plot_surface import execute_plot_surface
from analyze.visualization.plot_surface_by_phase import execute_plot_surface_by_phase
from analyze.visualization.plot_heatmap_by_phase import execute_plot_heatmap_by_phase
# gif
from analyze.visualization.make_gif import make_gif_surface, make_gif_surface_by_phase, make_gif_heatmap_by_phase


def erase_eqw_simulation():
    # 電場を消し去る場合のシミュレーション
    # select_exp_index_list = list(range(10, 21))
    select_exp_index_list = [3]
    # erase_tステップ目から電場を消し去る
    erase_t = 100
    print(select_exp_index_list)
    selected_conditions, exp_name = exp_017(exp_index_list=select_exp_index_list, erase_t=erase_t)
    execute_simulation(exact_condition_list=selected_conditions)

    plot_all(select_exp_index_list=select_exp_index_list, exp_name=exp_name)


def eqw_simulation():
    # 電場を消し去らない場合のシミュレーション
    select_exp_index_list = [3]
    print(select_exp_index_list)
    selected_conditions, exp_name = exp_016_01_00_x_set(exp_index_list=select_exp_index_list)
    execute_simulation(exact_condition_list=selected_conditions)
    plot_all(select_exp_index_list=select_exp_index_list, exp_name=exp_name)


def plot_all(select_exp_index_list, exp_name):
    # plotしたいexp_nameのexp_indexを指定する
    select_plot_exp_index = select_exp_index_list
    execute_plot_surface(exp_name=exp_name, plot_exp_index_list=select_plot_exp_index)
    make_gif_surface(exp_name=exp_name, plot_exp_index_list=select_plot_exp_index)

    execute_plot_surface_by_phase(exp_name=exp_name, plot_t_step=100)
    make_gif_surface_by_phase(exp_name=exp_name, plot_t_step=100)

    execute_plot_heatmap_by_phase(exp_name=exp_name, plot_t_step=100)
    make_gif_heatmap_by_phase(exp_name=exp_name, plot_t_step=100)


def e1(select_exp_index_list):
    """
    このerase_t_listでのexp_019のまとめ実行
    つまりpi/60の電場をかけた電場量子ウォークの電場を途中で消し去った場合
    """
    selected_conditions, exp_name = exp_019(exp_index_list=select_exp_index_list)
    execute_simulation(exact_condition_list=selected_conditions)

    execute_plot_surface(exp_name=exp_name, plot_exp_index_list=select_exp_index_list)
    make_gif_surface(exp_name=exp_name, plot_exp_index_list=select_exp_index_list)

    execute_plot_heatmap_by_phase(exp_name=exp_name, plot_t_step=100)
    make_gif_heatmap_by_phase(exp_name=exp_name, plot_t_step=100)
    # execute_plot_var(exp_name=exp_name, plot_exp_index_list=select_plot_exp_index)


def e2():
    """
    このerase_t_listでのexp_016_01_00_x_setのまとめ実行。
    つまりpi/60の電場をかけて電場量子ウォーク
    """
    # 電場ありのシミュレーション
    select_exp_index_list = [3]
    selected_conditions, exp_name = exp_016_01_00_x_set(exp_index_list=select_exp_index_list)
    execute_simulation(exact_condition_list=selected_conditions)

    # plotしたいexp_nameのexp_indexを指定する
    select_plot_exp_index = select_exp_index_list
    execute_plot_surface(exp_name=exp_name, plot_exp_index_list=select_plot_exp_index)
    make_gif_surface(exp_name=exp_name, plot_exp_index_list=select_plot_exp_index)

    # execute_plot_surface_by_phase(exp_name=exp_name, plot_t_step=200)
    # make_gif_surface_by_phase(exp_name=exp_name, plot_t_step=100)

    execute_plot_heatmap_by_phase(exp_name=exp_name, plot_t_step=100)
    make_gif_heatmap_by_phase(exp_name=exp_name, plot_t_step=100)


def e3(select_exp_index_list):
    """
    KLダイバージェンスを求める。
    電場のない量子ウォークと電場を途中で消した場合とのKLダイバージェンス
    :return:
    """
    exp_index_1 = 0
    selected_conditions_1, exp_name_1 = exp_018()

    selected_conditions_2, exp_name_2 = exp_019(exp_index_list=select_exp_index_list)

    for i, _ in enumerate(select_exp_index_list):
        execute_plot_kl_div(exp_name_1=exp_name_1, exp_index_1=exp_index_1, exp_name_2=exp_name_2, exp_index_2=i)


def e4():
    """
    KLダイバージェンスを求める。
    電場のない量子ウォークと電場のある量子ウォークとのKLダイバージェンス
    :return:
    """
    exp_index_1 = 0
    selected_conditions_1, exp_name_1 = exp_018()

    select_exp_index_list = [3]
    exp_index_2 = 3
    selected_conditions, exp_name_2 = exp_016_01_00_x_set(exp_index_list=select_exp_index_list)

    execute_plot_kl_div(exp_name_1=exp_name_1, exp_index_1=exp_index_1, exp_name_2=exp_name_2,
                        exp_index_2=exp_index_2)


if __name__ == '__main__':
    e2()
