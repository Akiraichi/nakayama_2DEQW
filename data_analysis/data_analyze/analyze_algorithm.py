import itertools

import numpy as np
from numba import njit


@njit('Tuple((f8,f8,f8))(f8[:,:],f8[:,:],b1,b1,b1)', cache=True)
def calc_KL_and_L1_and_L2(p1, p2, enable_KL_div, enable_L1_norm, enable_L2_norm):
    """
        概要
            量子ウォークの確率分布のKLダイバージェンスを求める。ただし中心が原点で直径が指定した値である円形領域では、KLダイバージェンスの値を0とする（領域内を無視する）
            また、その領域内のKLダイバージェンスを求める。
        引数
            p1,p2：大きさの等しい2次元リストp1[x,y]のように指定できること。
        返却値
            円形領域を無視した場合のKLダイバージェンスと、その円形領域のKLダイバージェンスを返却する
        """
    # 変数を初期化
    KL_div = 0
    L1_norm = 0
    L2_norm = 0
    # 便利な変数を定義
    len_x = p1.shape[1]
    len_y = p1.shape[0]

    for x in range(len_x):
        for y in range(len_y):

            # KLダイバージェンスを求める場合は以下を実行
            if enable_KL_div:
                if p1[x, y] == 0:
                    continue
                if p2[x, y] == 0:
                    p2[x, y] = 10E-20
                KL_div += p1[x, y] * np.log(p1[x, y] / p2[x, y])

            # L1ノルムを求める場合は以下を実行
            if enable_L1_norm:
                """誤差の絶対値の和"""
                # 以下の処理について：実行しなくても誤差は生じないようなのでコメントアウトしても良い
                # 小さすぎる値でも処理できるようにしておく。
                # 確率が1以上になるまで10を何度かければいいのか、その回数をcountに代入する。
                count = 1
                while (p1[x, y] * count) > 1.0:
                    count += 1
                L1_norm += np.abs(p1[x, y] * (10 ** count) - p2[x, y] * (10 ** count)) / (10 ** count)
            # L2ノルムを求める場合は以下を実行
            if enable_L2_norm:
                """二乗誤差の和"""
                # 以下の処理について：実行しなくても誤差は生じないようなのでコメントアウトしても良い
                # 小さすぎる値でも処理できるようにしておく
                # 確率が1以上になるまで10を何度かければいいのか、その回数をcountに代入する。
                count = 1
                while (p1[x, y] * count) > 1.0:
                    count += 1
                L2_norm += ((p1[x, y] * (10 ** count) - p2[x, y] * (10 ** count)) ** 2) / (10 ** (count * 2))
    return KL_div, L1_norm, L2_norm


def calc_correlation_coefficient(p1, p2, enable_correlation_coefficient):
    # 相関係数を求める場合は以下を実行
    correlation_coefficient = 0
    if enable_correlation_coefficient:
        data_1 = list(itertools.chain.from_iterable(p1))
        data_2 = list(itertools.chain.from_iterable(p2))

        # 相関行列を計算
        correlation_coefficient = np.corrcoef(data_1, data_2)

    return correlation_coefficient[0, 1]
