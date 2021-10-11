import numpy as np
from numba import njit, jit
from simulation.save import save_t_step_psy
from config.config import config_simulation_data_save_path, print_warning, print_green_text
import glob
import joblib


def simulation_QW2D(condition, continue_t):
    """
    :param condition:
    :return:
    """
    # conditionを展開し初期化する。
    exp_index = condition.exp_index
    exp_name = condition.exp_name
    T = condition.T
    P = condition.P
    Q = condition.Q
    R = condition.R
    S = condition.S
    PSY_init = condition.PSY_init
    Algorithm = condition.algorithm
    phi = condition.phi
    erase_t = condition.erase_t

    # 初期確率振幅ベクトルの設定
    # 一つ前の時刻と今の時刻と2ステップ分だけメモリを用意する[時間ステップ, x, y, 4成分]
    PSY_now = np.zeros([2 * T + 1, 2 * T + 1, 4], dtype=np.complex128)
    # t=0でx=0,y=0の位置にいる。成分はPSY_init
    PSY_now[0 + T, 0 + T] = PSY_init
    # その他の場所の確率振幅ベクトルの設定
    init_vector = np.zeros_like(PSY_init, dtype=np.complex128)

    # 時間発展パート
    """
    途中からシミュレーションしたい時は、どこから始めるかを指定するようにした。
    glob関数あるいはgoogle driveの使用により一度に取得可能なファイル数が999までだったからだ。
    continue_tステップ目から再開する。
    continue_t=99なら、98ステップをロードし、99ステップのシミュレーションから開始する
    
    """
    if continue_t == 0:
        # 既に完了したシミュレーションが0。つまり完全新規のシミュレーション
        # ここでセーブする。保存するのは初期状態のPSY
        save_t_step_psy(psy=PSY_now, t=0, exp_name=exp_name, i=exp_index, condition=condition)
        start_t = 1
    else:
        # 途中からシミュレーションを再開
        path = f"{config_simulation_data_save_path(exp_name, exp_index)}/{str(continue_t - 1).zfill(3)}.jb"
        print(path)
        PSY_now = joblib.load(path)["シミュレーションデータ"]
        start_t = continue_t
    print(f"start_t={start_t}")
    #
    # simulation_data_file_names = glob.glob(f"{config_simulation_data_save_path(exp_name, exp_index)}/*.jb")
    # simulation_data_file_names.sort()  # 実験順にsortする。
    # start_t = 1
    # if len(simulation_data_file_names) == 0:
    #     # 既に完了したシミュレーションが0。つまり完全新規のシミュレーション
    #     # ここでセーブする。保存するのは初期状態のPSY
    #     save_t_step_psy(psy=PSY_now, t=0, exp_name=exp_name, i=exp_index, condition=condition)
    # else:
    #     # 途中からシミュレーションを再開
    #
    #     PSY_now = joblib.load(simulation_data_file_names[-2])["シミュレーションデータ"]  # 最も最後から一つ前からシミュレーションを再開する
    #     print(simulation_data_file_names[-2])
    #     """
    #      simulation_data_file_names[-2] // 'result/exp_018/simulation_data_exp_018/00/098.jb'
    #      a.split("/") //  ['result', 'exp_018', 'simulation_data_exp_018', '00', '098.jb']
    #      a.split("/")[-1] // '098.jb'
    #      b[:-3] // '098'
    #     """
    #     load_t = int(simulation_data_file_names[-2].split("/")[-1][:-3])
    #     print(f"load_t={load_t}")
    #     """
    #     t=load_tのシミュレーションデータをPSY_nowとしてロードする。
    #     ゆえに、次のtはload_t+1であれば良い
    #     """
    #     start_t = load_t + 1
    #     print(f"start_t={start_t}")

    # 繰り返し回数はT+1回。現在時刻を0次の時刻を1に代入する
    for t in range(start_t, T + 1):
        PSY_next = np.zeros([2 * T + 1, 2 * T + 1, 4], dtype=np.complex128)
        print(f"{t}：ステップ")
        PSY_now = calculate_QW2D(T, init_vector, phi, PSY_now, PSY_next, Algorithm, P=P, Q=Q, R=R, S=S, t=t,
                                 erase_t=erase_t)
        # ここでセーブする。保存するのはt+1ステップめ（なぜ＋1するのかというと初期値で一回保存しているから）
        # TODO:セーブに時間がかかるようだったら、10ステップごとに保存する、などする
        save_t_step_psy(psy=PSY_now, t=t, exp_name=exp_name, i=exp_index, condition=condition)


# 1/0での挙動が想定外である。
@jit
def e_i_phi(position, T, phi, pow_n):
    # 座標はposition+1。0+Tを座標0としている
    # exp(iH), H=電位, 電位＝位置座標position * phi（何かしらの電位をphiで表現）
    res = np.exp(1j * np.power(position - T, pow_n) * phi)
    # print(np.power(position - T, pow_n))
    # print(phi)
    # print(pow_n)
    # print(position)
    return res


@njit('c16[:,:,:](i8,c16[:],f8,c16[:,:,:],c16[:,:,:],i8,c16[:,:],c16[:,:],c16[:,:],c16[:,:],i8,i8)', cache=True)
def calculate_QW2D(T, init_vector, phi, PSY_now, PSY_next, Algorithm, P, Q, R, S, t, erase_t):
    for x in range(0, 2 * T + 1):
        for y in range(0, 2 * T + 1):
            # PSY_of_P, PSY_of_Q, PSY_of_R, PSY_of_S = set_param(PSY_now, init_vector, x, y, T)
            if x == 2 * T:
                PSY_of_P = init_vector
            else:
                PSY_of_P = PSY_now[x + 1, y]

            if x == 0:
                PSY_of_Q = init_vector
            else:
                PSY_of_Q = PSY_now[x - 1, y]

            if y == 2 * T:
                PSY_of_R = init_vector
            else:
                PSY_of_R = PSY_now[x, y + 1]

            if y == 0:
                PSY_of_S = init_vector
            else:
                PSY_of_S = PSY_now[x, y - 1]
            # 指定された計算式で計算
            # PSY_next = algo_list(PSY_next, Algorithm, P, Q, R, S, PSY_of_P, PSY_of_Q, PSY_of_R, PSY_of_S, x, y, T,
            #                      phi)
            if Algorithm == 2:
                # 通常
                PSY_next[x, y] = P @ PSY_of_P + \
                                 Q @ PSY_of_Q + \
                                 R @ PSY_of_R + \
                                 S @ PSY_of_S

            elif Algorithm == 3:
                # x軸で電場をかけた
                PSY_next[x, y] = np.exp(1j * (x - T) * phi) * ((P @ PSY_of_P) +
                                                               (Q @ PSY_of_Q) +
                                                               (R @ PSY_of_R) +
                                                               (S @ PSY_of_S))
            elif Algorithm == 4:
                # y軸に電場をかけた
                PSY_next[x, y] = e_i_phi(y, T, phi, 1) * ((P @ PSY_of_P) +
                                                          (Q @ PSY_of_Q) +
                                                          (R @ PSY_of_R) +
                                                          (S @ PSY_of_S))
            elif Algorithm == 5:
                # xとy両方
                PSY_next[x, y] = e_i_phi(x, T, phi, 1) * e_i_phi(y, T, phi, 1) \
                                 * ((P @ PSY_of_P) +
                                    (Q @ PSY_of_Q) +
                                    (R @ PSY_of_R) +
                                    (S @ PSY_of_S))

            elif Algorithm == 6:
                # 固定値-x軸
                PSY_next[x, y] = np.exp(2j * np.pi / 120) * ((P @ PSY_of_P) +
                                                             (Q @ PSY_of_Q) +
                                                             (R @ PSY_of_R) +
                                                             (S @ PSY_of_S))
            #
            # elif Algorithm == 8:
            #     # x軸で電場をかけた。位置の逆数
            #     PSY_next[x, y] = e_i_phi(x, T, phi, -1) * ((P @ PSY_of_P) +
            #                                                (Q @ PSY_of_Q) +
            #                                                (R @ PSY_of_R) +
            #                                                (S @ PSY_of_S))

            # elif Algorithm == 9:
            #     # y軸に電場をかけた。位置の逆数
            #     PSY_next[x, y] = e_i_phi(y, T, phi, -1) * ((P @ PSY_of_P) +
            #                                                (Q @ PSY_of_Q) +
            #                                                (R @ PSY_of_R) +
            #                                                (S @ PSY_of_S))
            elif Algorithm == 10:
                # xとy両方。位置の逆数
                PSY_next[x, y] = e_i_phi(x, T, phi, -1) * e_i_phi(y, T, phi, -1) \
                                 * ((P @ PSY_of_P) +
                                    (Q @ PSY_of_Q) +
                                    (R @ PSY_of_R) +
                                    (S @ PSY_of_S))

            elif Algorithm == 1010:
                # x軸で電場をかけた
                PSY_next[x, y] = e_i_phi(x + 1, T, phi, 1) * (P @ PSY_of_P) + \
                                 e_i_phi(x - 1, T, phi, 1) * (Q @ PSY_of_Q) + \
                                 (R @ PSY_of_R) + \
                                 (S @ PSY_of_S)
            elif Algorithm == 1020:
                # y軸に電場をかけた
                PSY_next[x, y] = P @ PSY_of_P + \
                                 Q @ PSY_of_Q + \
                                 e_i_phi(y + 1, T, phi, 1) * (R @ PSY_of_R) + \
                                 e_i_phi(y - 1, T, phi, 1) * (S @ PSY_of_S)
            elif Algorithm == 1030:
                # xとy両方
                PSY_next[x, y] = e_i_phi(x + 1, T, phi, 1) * (P @ PSY_of_P) + \
                                 e_i_phi(x - 1, T, phi, 1) * (Q @ PSY_of_Q) + \
                                 e_i_phi(y + 1, T, phi, 1) * (R @ PSY_of_R) + \
                                 e_i_phi(y - 1, T, phi, 1) * (S @ PSY_of_S)
            # elif Algorithm == 4010:
            #     # 電場が時間変化する場合。位置の逆数
            #     if t % 2 == 0:
            #         # x軸で電場をかけた。
            #         PSY_next[x, y] = e_i_phi(x, T, phi, -1) * ((P @ PSY_of_P) +
            #                                                    (Q @ PSY_of_Q) +
            #                                                    (R @ PSY_of_R) +
            #                                                    (S @ PSY_of_S))
            #     elif t % 2 == 1:
            #         # y軸に電場をかけた。
            #         PSY_next[x, y] = e_i_phi(y, T, phi, -1) * ((P @ PSY_of_P) +
            #                                                    (Q @ PSY_of_Q) +
            #                                                    (R @ PSY_of_R) +
            #                                                    (S @ PSY_of_S))
            elif Algorithm == 5010:
                # 電場が時間変化する場合
                if t % 2 == 0:
                    # x軸で電場をかけた。
                    PSY_next[x, y] = e_i_phi(x, T, phi, 1) * ((P @ PSY_of_P) +
                                                              (Q @ PSY_of_Q) +
                                                              (R @ PSY_of_R) +
                                                              (S @ PSY_of_S))
                else:
                    # y軸に電場をかけた。
                    PSY_next[x, y] = e_i_phi(y, T, phi, 1) * ((P @ PSY_of_P) +
                                                              (Q @ PSY_of_Q) +
                                                              (R @ PSY_of_R) +
                                                              (S @ PSY_of_S))

            elif Algorithm == 100:
                # x軸で電場をかけた
                if t >= erase_t:
                    PSY_next[x, y] = P @ PSY_of_P + \
                                     Q @ PSY_of_Q + \
                                     R @ PSY_of_R + \
                                     S @ PSY_of_S
                else:
                    PSY_next[x, y] = np.exp(1j * (x - T) * phi) * ((P @ PSY_of_P) +
                                                                   (Q @ PSY_of_Q) +
                                                                   (R @ PSY_of_R) +
                                                                   (S @ PSY_of_S))

    return PSY_next


def calculate_probability_distribution_at_time_t_memory_save(PSY, len_x, len_y):
    probability = np.zeros([len_x, len_y])
    probability, err = calculate_dict(len_x, len_y, probability, PSY)
    if err:
        print_warning(f"確率に問題がある可能性があります：確率の合計＝{probability.sum()}")
    return probability


@njit('Tuple((f8[:,:],b1))(i8,i8,f8[:,:],c16[:,:,:])', cache=True)
def calculate_dict(len_x, len_y, probability, PSY):
    for x in range(0, len_x):
        for y in range(0, len_y):
            # L2ノルム（いわゆる距離と同じ）をとる。そして2乗
            probability[x, y] = np.linalg.norm(PSY[x, y], ord=2) ** 2

    # 確率の合計は1かどうかをチェックする
    probability_sum = probability.sum()
    err = False
    if round(probability_sum, 13) != 1.0:
        err = True
    return probability, err
