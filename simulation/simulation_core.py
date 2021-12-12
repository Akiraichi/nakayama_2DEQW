import numpy as np
from numba import njit, jit
from config.config import print_warning, print_green_text, ConfigSimulation


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


@njit('c16[:,:,:](i8,c16[:],f8,c16[:,:,:],c16[:,:,:],i8,c16[:,:],c16[:,:],c16[:,:],c16[:,:],i8,i8,i8)', cache=True)
def calculate_QW2D(T, init_vector, phi, PSY_now, PSY_next, Algorithm, P, Q, R, S, t, erase_t, erase_time_step):
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
                PSY_next[x, y] = np.exp(1j * (x - T) * phi) * np.exp(1j * (y - T) * phi) * \
                                 ((P @ PSY_of_P) +
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
            elif Algorithm == 200:
                """
                電場をゆっくり消す場合。
                離散量ウォークだから、どのみち離散的に電場は変化していく必要がある。今までは突然、電場を消していたが、
                ゆっくり電場を減少させていくことで、多少、なんら中の違いが生まれる可能性はあると思う。
                線形的に小さくしていくことで消していく
                では、何ステップ使って、電場を消していくかだが、configで設定できるようにしておくことにする。
                """
                # x軸で電場をかけた
                if t >= erase_t:
                    per = t - erase_t
                    if per < erase_time_step:
                        per = 1 - per / erase_time_step

                        PSY_next[x, y] = np.exp(1j * (x - T) * phi * per) * ((P @ PSY_of_P) +
                                                                             (Q @ PSY_of_Q) +
                                                                             (R @ PSY_of_R) +
                                                                             (S @ PSY_of_S))
                    else:
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


def calc_probability(PSY, len_x, len_y):
    probability = np.zeros([len_x, len_y])
    probability, p_sum, err = calculate_dict(len_x, len_y, probability, PSY)
    if err:
        print_warning(f"確率に問題がある可能性があります：{p_sum}")
    return probability


@njit('Tuple((f8[:,:],f8,b1))(i8,i8,f8[:,:],c16[:,:,:])', cache=True)
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
    return probability, probability_sum, err
