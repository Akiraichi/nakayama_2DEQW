from simulation.codition import Condition
from simulation.codition import set_basic_condition
import numpy as np
import sympy


#
# def exp0_set():
#     exp_name = "デバッグ用の実験"
#     conditions = []
#     for i in range(1):
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = np.array([1 / 2, 1 / 2, -1 / 2, -1 / 2])
#         conditions.append(c)
#     return conditions, exp_name
#
#
# def exp1_set():
#     exp_name = "初期確立振幅ベクトル４成分のうち一つだけ１で他は０"
#     conditions = []
#     for i in range(4):
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = np.array([0, 0, 0, 0])
#         c.PSY_init[i] = 1
#         conditions.append(c)
#     return conditions, exp_name
#
#
# def exp2_set():
#     exp_name = "全ての初期確率振幅ベクトルの絶対値が1／2。-を適用する全パターンを実験"
#     param_list = [
#         # 0つ
#         [1 / 2, 1 / 2, 1 / 2, 1 / 2],
#
#         # 1つ
#         [-1 / 2, 1 / 2, 1 / 2, 1 / 2],
#         [1 / 2, -1 / 2, 1 / 2, 1 / 2],
#         [1 / 2, 1 / 2, -1 / 2, 1 / 2],
#         [1 / 2, 1 / 2, 1 / 2, -1 / 2],
#
#         # 2つ
#         [-1 / 2, -1 / 2, 1 / 2, 1 / 2],
#         [-1 / 2, 1 / 2, -1 / 2, 1 / 2],
#         [-1 / 2, 1 / 2, 1 / 2, -1 / 2],
#
#         [1 / 2, -1 / 2, -1 / 2, 1 / 2],
#         [1 / 2, -1 / 2, 1 / 2, -1 / 2],
#
#         [1 / 2, 1 / 2, -1 / 2, -1 / 2],
#         # 3つ
#         [-1 / 2, -1 / 2, -1 / 2, 1 / 2],
#         [-1 / 2, -1 / 2, 1 / 2, -1 / 2],
#         [-1 / 2, 1 / 2, -1 / 2, -1 / 2],
#         [1 / 2, -1 / 2, -1 / 2, -1 / 2],
#         # 4つ
#         [-1 / 2, -1 / 2, -1 / 2, -1 / 2]]
#     conditions = []
#     for i, param in enumerate(param_list):
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = np.array(param)
#         conditions.append(c)
#     return conditions, exp_name
#
#
# def exp3_set():
#     exp_name = "sin_cos_exp"
#
#     theta_list = []
#     param_list = []
#     for i in range(12):
#         theta = np.pi * i / 12
#         theta_list.append(theta)
#
#     for theta in theta_list:
#         param = [np.sin(theta) / np.sqrt(2), np.sin(theta) / np.sqrt(2), np.cos(theta) / np.sqrt(2),
#                  np.cos(theta) / np.sqrt(2)]
#         param_list.append(param)
#
#     conditions = []
#     for i, param in enumerate(param_list):
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = np.array(param)
#         conditions.append(c)
#     return conditions, exp_name
#
#
# def exp4_set():
#     exp_name = "6-14-傾けて実験するやつ"
#     conditions = []
#     c = Condition()
#     set_basic_condition_1(c)
#     c.PSY_init = 1 / 2 * np.array([1, -1, -1, 1])
#     conditions.append(c)
#     return conditions, exp_name
#
#
# def exp5_set(exp_name):
#     algorithm_list = [2]
#     conditions = []
#     for param in algorithm_list:
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         c.algorithm = param
#         c.phi = 120
#         conditions.append(c)
#     return conditions, exp_name
#
#
# def exp6_set():
#     exp_name = "6-15論文再現テスト-本テスト"
#     algorithm_list = [2, 3, 4, 5]
#     conditions = []
#     for param in algorithm_list:
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         c.algorithm = param
#         c.phi = 2 * np.pi / 120
#         conditions.append(c)
#     return conditions, exp_name
#
#
# def exp_debug_x():
#     exp_name = "「x軸に電場を加える」デバッグ"
#     algorithm_list = [3]
#     conditions = []
#     for param in algorithm_list:
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         c.algorithm = param
#         c.phi = 2 * np.pi / 120
#         conditions.append(c)
#     return conditions, exp_name
#
#
# def exp7_set(exp_name):
#     """x軸に電場をかけた"""
#     phi_list = [i * 30 * np.pi / 120 for i in range(1, 21)]
#     conditions = []
#     for phi in phi_list:
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         # x軸のみに電場を加えるため、アルゴリズム番号は3番
#         c.algorithm = 3
#         c.phi = phi
#         conditions.append(c)
#     return conditions, exp_name
#
#
# def exp_1_1_y_set(exp_name):
#     """y軸に電場をかけた場合"""
#     phi_list = [i * 30 * np.pi / 120 for i in range(1, 21)]
#     conditions = []
#     for phi in phi_list:
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         # x軸のみに電場を加えるため、アルゴリズム番号は3番
#         c.algorithm = 4
#         c.phi = phi
#         conditions.append(c)
#     return conditions, exp_name
#
#
# def exp_1_2_xy_set(exp_name):
#     """x軸とy軸に電場をかけた場合"""
#     phi_list = [i * 30 * np.pi / 120 for i in range(1, 21)]
#     conditions = []
#     for phi in phi_list:
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         # x軸のみに電場を加えるため、アルゴリズム番号は3番
#         c.algorithm = 5
#         c.phi = phi
#         conditions.append(c)
#     return conditions, exp_name
#
#
# def exp_2_1_x_set(exp_name):
#     """x軸に電場をかけた場合。位置の逆数"""
#     phi_list = [i * 30 * np.pi / 120 for i in range(1, 21)]
#     conditions = []
#     for phi in phi_list:
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         # x軸のみに電場を加えるため、アルゴリズム番号は3番
#         c.algorithm = 8
#         c.phi = phi
#         conditions.append(c)
#     return conditions, exp_name
#
#
# def exp_2_2_y_set(exp_name):
#     """y軸に電場をかけた場合。位置の逆数"""
#     phi_list = [i * 30 * np.pi / 120 for i in range(1, 21)]
#     conditions = []
#     for phi in phi_list:
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         # x軸のみに電場を加えるため、アルゴリズム番号は3番
#         c.algorithm = 9
#         c.phi = phi
#         conditions.append(c)
#     return conditions, exp_name
#
#
# def exp_2_3_xy_set(exp_name):
#     phi_list = [i * 30 * np.pi / 120 for i in range(1, 21)]
#     conditions = []
#     for phi in phi_list:
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         # x軸のみに電場を加えるため、アルゴリズム番号は3番
#         c.algorithm = 10
#         c.phi = phi
#         conditions.append(c)
#     return conditions, exp_name


def exp_1010_x_set():
    exp_name = "x軸に移動前の電場（遅延）をかけた場合"
    phi_list = [i * 2 * np.pi / 120 for i in range(1, 21)]
    conditions = []
    for phi in phi_list:
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        # x軸のみに電場を加えるため、アルゴリズム番号は3番
        c.algorithm = 1010
        c.phi = phi
        conditions.append(c)
    return conditions, exp_name


def exp_1020_y_set():
    exp_name = "y軸に移動前の電場（遅延）をかけた場合"
    phi_list = [i * 2 * np.pi / 120 for i in range(1, 21)]
    conditions = []
    for phi in phi_list:
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        # x軸のみに電場を加えるため、アルゴリズム番号は3番
        c.algorithm = 1020
        c.phi = phi
        conditions.append(c)
    return conditions, exp_name


def exp_1030_xy_set():
    exp_name = "xとy軸に移動前の電場（遅延）をかけた場合"
    phi_list = [i * 2 * np.pi / 120 for i in range(1, 21)]
    conditions = []
    for phi in phi_list:
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        # x軸のみに電場を加えるため、アルゴリズム番号は3番
        c.algorithm = 1030
        c.phi = phi
        conditions.append(c)
    return conditions, exp_name


#
# def exp_2010_x_set():
#     exp_name = "exp_2010_x軸に電場をかけた_pi/4刻み"
#     phi_list = [i * 30 * np.pi / 120 for i in range(1, 21)]
#     conditions = []
#     for phi in phi_list:
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         # x軸のみに電場を加えるため、アルゴリズム番号は3番
#         c.algorithm = 3
#         c.phi = phi
#         conditions.append(c)
#     return conditions, exp_name
#
#
# def exp_3010_x_set():
#     exp_name = "exp_3010_x軸に電場をかけた_2pi/120刻み"
#     phi_list = [i * 2 * np.pi / 120 for i in range(1, 61)]
#     conditions = []
#     for phi in phi_list:
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         # x軸のみに電場を加えるため、アルゴリズム番号は3番
#         c.algorithm = 3
#         c.phi = phi
#         conditions.append(c)
#     return conditions, exp_name
#
#
# def exp_3011_x_set():
#     exp_name = "exp_3010_x軸に電場をかけた_2pi/120刻みの続き。i=61から120まで"
#     phi_list = [i * 2 * np.pi / 120 for i in range(61, 121)]
#     conditions = []
#     for phi in phi_list:
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         # x軸のみに電場を加えるため、アルゴリズム番号は3番
#         c.algorithm = 3
#         c.phi = phi
#         conditions.append(c)
#     return conditions, exp_name
#
#
# def exp_3030_xy_set():
#     exp_name = "exp_3030/xとy軸に電場をかけた_2pi_120刻み。i=1から30まで"
#     phi_list = [i * 2 * np.pi / 120 for i in range(1, 31)]
#     conditions = []
#     for phi in phi_list:
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         # x軸のみに電場を加えるため、アルゴリズム番号は3番
#         c.algorithm = 5
#         c.phi = phi
#         conditions.append(c)
#     return conditions, exp_name
#
#
# def exp_3031_xy_set():
#     exp_name = "exp_3030/exp_3031_xとy軸に電場をかけた_2pi_120刻みの続き。i=31から60まで"
#     phi_list = [i * 2 * np.pi / 120 for i in range(31, 61)]
#     conditions = []
#     for phi in phi_list:
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         # x軸のみに電場を加えるため、アルゴリズム番号は3番
#         c.algorithm = 5
#         c.phi = phi
#         conditions.append(c)
#     return conditions, exp_name


def exp_4010_t_xy_set():
    exp_name = "exp_4010/時間変化する電場_pi_4刻み。tが偶数の時x軸の電場、奇数の時y軸に電場をかけた"
    phi_list = [i * np.pi / 4 for i in range(1, 21)]
    conditions = []
    for phi in phi_list:
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 4010
        c.phi = phi
        conditions.append(c)
    return conditions, exp_name


def exp_4011_t_xy_set():
    exp_name = "exp_4010/exp_4011_時間変化する電場_2pi_120刻み。tが偶数の時x軸の電場、奇数の時y軸に電場をかけた"
    phi_list = [i * 2 * np.pi / 120 for i in range(1, 21)]
    conditions = []
    for phi in phi_list:
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        # x軸のみに電場を加えるため、アルゴリズム番号は3番
        c.algorithm = 4010
        c.phi = phi
        conditions.append(c)
    return conditions, exp_name


# 以下新システム
def exp_0000__debug_folder_changed_check_set():
    """
    ・関数名：exp_番号__補足情報_set
    ・exp_nameはexp番号のみにする。
    ・実験詳細はコメントに記入（数式をふんだんに使いたい場合はjupyterでも可能だが、ここのコメントにも記入すること）
    ・
    """
    exp_name = "exp_0000"
    conditions = []
    for i in range(1, 5):
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 3

        x = sympy.Symbol('x')
        phi = x * sympy.pi / 4
        phi = phi.subs(x, i)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        conditions.append(c)
    return conditions, exp_name


def exp_2010_x_set():
    """
    x軸に電場をかけた_pi/4刻み
    """
    exp_name = "exp_2010"
    conditions = []
    for i in range(1, 21):
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 3

        x = sympy.Symbol('x')
        phi = x * sympy.pi / 4
        phi = phi.subs(x, i)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.index = i - 1
        conditions.append(c)
    return conditions, exp_name


def exp_3010_x_set():
    """x軸に電場をかけた_pi/60刻み。1から60"""
    exp_name = "exp_3010"
    conditions = []
    for i in range(1, 61):
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 3

        x = sympy.Symbol('x')
        phi = x * 2 * sympy.pi / 120
        phi = phi.subs(x, i)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.index = i - 1
        conditions.append(c)
    return conditions, exp_name


def exp_3011_x_set():
    """x軸に電場をかけた_2pi/120刻み。i=61から120まで"""
    exp_name = "exp_3011"
    conditions = []
    for i in range(61, 121):
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 3

        x = sympy.Symbol('x')
        phi = x * 2 * sympy.pi / 120
        phi = phi.subs(x, i)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.index = i - 1
        conditions.append(c)
    return conditions, exp_name


def exp_3030_xy_set():
    """xとy軸に電場をかけた_2pi_120刻み。i=1から60まで"""
    exp_name = "exp_3030"
    conditions = []
    for i in range(1, 61):
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 5
        x = sympy.Symbol('x')
        phi = x * 2 * sympy.pi / 120
        phi = phi.subs(x, i)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.index = i - 1
        conditions.append(c)
    return conditions, exp_name


def exp_3031_xy_set():
    """xとy軸に電場をかけた_2pi_120刻み。i=61から120まで"""
    exp_name = "exp_3031"
    conditions = []
    for i in range(61, 121):
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 5
        x = sympy.Symbol('x')
        phi = x * 2 * sympy.pi / 120
        phi = phi.subs(x, i)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.index = i - 1
        conditions.append(c)
    return conditions, exp_name


def exp_5010_x_set(start_index, end_index):
    """
    x軸に電場をかけた。pi/整数の位相でシミュレーションする。
    Example: i=1〜20
    start_index=1
    end_index=21
    """
    exp_name = "exp_5010"
    conditions = []
    for i in range(start_index, end_index):
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 3
        x = sympy.Symbol('x')
        phi = sympy.pi / x
        phi = phi.subs(x, i)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.index = i - 1
        conditions.append(c)
    return conditions, exp_name


def exp_6010_prime_number_x_set():
    """pi/素数でシミュレーションしてみる"""  # 変更点
    exp_name = "exp_6010"  # 変更点
    conditions = []
    prime_number_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89,
                         97, ]
    for i, num in enumerate(prime_number_list):  # 変更点
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 3  # 変更点
        x = sympy.Symbol('x')
        phi = sympy.pi / x  # 変更点
        phi = phi.subs(x, num)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.index = i  # 変更点
        conditions.append(c)
    return conditions, exp_name


def exp_7010_ryoka_x_set():
    """ryoka数でシミュレーションしてみる"""  # 変更点
    exp_name = "exp_7010"  # 変更点
    conditions = []
    prime_number_list = [2, 1, 3, 4, 7, 11, 18, 29, 47, 76]
    for i, num in enumerate(prime_number_list):  # 変更点
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 3  # 変更点
        x = sympy.Symbol('x')
        phi = sympy.pi / x  # 変更点
        phi = phi.subs(x, num)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.index = i  # 変更点
        conditions.append(c)
    return conditions, exp_name


def exp_8010_Landau_x_set():
    """Landau数でシミュレーションしてみる"""  # 変更点
    exp_name = "exp_8010"  # 変更点
    conditions = []
    prime_number_list = [1, 2, 3, 4, 6, 12, 15, 20, 30, 60, 84, 105, 140, 210, 420]
    for i, num in enumerate(prime_number_list):  # 変更点
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 3  # 変更点
        x = sympy.Symbol('x')
        phi = sympy.pi / x  # 変更点
        phi = phi.subs(x, num)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.index = i  # 変更点
        conditions.append(c)
    return conditions, exp_name


# 新しい実験番号の付け方を以下から適用
def exp_009_01_00_x_set():
    """	Number of partitions of n into pairwise relatively prime parts."""  # 変更点
    exp_name = "exp_009_01_00"  # 変更点
    conditions = []
    prime_number_list = [1, 2, 3, 4, 6, 7, 10, 12, 15, 18, 23, 27, 33, 38, 43, 51, 60, 70, 81, 92, 102, 116, 134, 153,
                         171, 191, 211]
    for i, num in enumerate(prime_number_list):  # 変更点
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 3  # 変更点
        x = sympy.Symbol('x')
        phi = sympy.pi / x  # 変更点
        phi = phi.subs(x, num)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.index = i  # 変更点
        conditions.append(c)
    return conditions, exp_name


def exp_010_01_00_x_set():
    """		Number of integer partitions of n with all pairs of consecutive parts relatively prime. """  # 変更点
    exp_name = "exp_010_01_00"  # 変更点
    conditions = []
    prime_number_list = [1, 2, 3, 4, 6, 7, 10, 12, 16, 19, 24, 28, 36, 43, 51, 62, 74, 87, 104, 122, 143, 169, 195, 227]
    for i, num in enumerate(prime_number_list):  # 変更点
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 3  # 変更点
        x = sympy.Symbol('x')
        phi = sympy.pi / x  # 変更点
        phi = phi.subs(x, num)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.index = i  # 変更点
        conditions.append(c)
    return conditions, exp_name


def exp_011_01_00_x_set():
    """600の約数。exp_5010系統"""  # 変更点
    exp_name = "exp_011_01_00"  # 変更点
    conditions = []
    prime_number_list = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 25, 30, 40, 50, 60, 75, 100, 120, 150, 200, 300, 600]
    for i, num in enumerate(prime_number_list):  # 変更点
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 3  # 変更点
        x = sympy.Symbol('x')
        phi = sympy.pi / x  # 変更点
        phi = phi.subs(x, num)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.index = i  # 変更点
        conditions.append(c)
    return conditions, exp_name


# ここの実験から600ステップまでシミュレーションするように変更。今までのシミュレーションを再実行すると全て再実行になることに注意
# def exp_012_01_00_x_set():
#     """時間変化する電場位置の逆数"""  # 変更点
#     exp_name = "exp_012_01_00"  # 変更点
#     conditions = []
#     for i in range(1, 21):  # 変更点
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         c.algorithm = 4010  # 変更点
#         x = sympy.Symbol('x')
#         phi = x * sympy.pi / 4  # 変更点
#         phi = phi.subs(x, i)
#         print(phi)
#         c.phi = float(phi.evalf())
#         c.phi_latex = sympy.latex(phi)
#         c.exp_name = exp_name
#         c.index = i - 1
#         conditions.append(c)
#     return conditions, exp_name


# def exp_013_01_00_x_set(start_index, end_index):
#     """弱電場で時間変化する電場。位置の逆数"""  # 変更点
#     exp_name = "exp_013_01_00"  # 変更点
#     conditions = []
#     for i in range(start_index, end_index):
#         c = Condition()
#         set_basic_condition_1(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         c.algorithm = 4010
#         x = sympy.Symbol('x')
#         phi = sympy.pi / x
#         phi = phi.subs(x, i * 10)
#         print(phi)
#         c.phi = float(phi.evalf())
#         c.phi_latex = sympy.latex(phi)
#         c.exp_name = exp_name
#         c.index = i - 1
#         conditions.append(c)
#     return conditions, exp_name


def exp_014_01_00_x_set(start_index, end_index):
    """exp_5010系統"""  # 変更点
    exp_name = "exp_014_01_00"  # 変更点
    conditions = []
    for i in range(start_index, end_index):
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 3
        x = sympy.Symbol('x')
        phi = sympy.pi / x
        phi = phi.subs(x, i * 10)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.index = i - 1
        conditions.append(c)
    return conditions, exp_name


def exp_015_01_00_x_set(start_index, end_index):
    """弱電場で時間変化する電場"""  # 変更点
    exp_name = "exp_015_01_00"  # 変更点
    conditions = []
    for i in range(start_index, end_index):
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 5010
        x = sympy.Symbol('x')
        phi = sympy.pi * x / 4
        phi = phi.subs(x, i)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.index = i - 1
        conditions.append(c)
    return conditions, exp_name


#
# def exp_016_01_00_x_set(start, end):
#     """x軸に電場をかけた_pi/240刻み。1から60"""
#     exp_name = "exp_016_01_00"
#     conditions = []
#     for i in range(start, end):
#         c = Condition()
#         set_basic_condition(c)
#         c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
#         c.algorithm = 3
#
#         x = sympy.Symbol('x')
#         phi = x * sympy.pi / 240
#         phi = phi.subs(x, i)
#         print(phi)
#         c.phi = float(phi.evalf())
#         c.phi_latex = sympy.latex(phi)
#         c.exp_name = exp_name
#         c.index = i - 1
#         conditions.append(c)
#     return conditions, exp_name

# 新システムとしてのexp016
def exp_016_01_00_x_set(exp_index_list):
    """
    Example
    exp_index_list=[0,1,2,3,4,5]
    exp_index=0,1,2,3,4,5を実行する
    exp_indexは0〜239まである（range(240))

    設計理念
    ・関数はあくまで複数の実験を一つにまとめて実行する
    ・この複数の実験に番号をつけたがそれがexp_index（0からスタート）
    ・exp_index_listにリストで実行したいexp_index番号を指定されたものを実行する
    ・実験に関する情報は全てconditionに格納する
    ・今回のセッションで実験したい内容を、conditionsからexp_index_listをもとにselected_conditionsへ抽出する。
    :param exp_index_list: リストで実行したいexp_index番号を指定
    :return: 今回のセッションで実行する実験のconditionのリスト
    """
    exp_name = "exp_016_01_00"
    conditions = []
    # 0から239まで240回分の実験をconditionsにまとめる
    for i in range(240):
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 3

        x = sympy.Symbol('x')
        phi = x * sympy.pi / 240
        phi = phi.subs(x, i + 1)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.exp_index = i
        conditions.append(c)

    # 今回のセッションで実験したい内容を、conditionsからexp_index_listをもとにselected_conditionsへ抽出する。
    # オブジェクトの格納でコピーではないので元のconditionsの変更はselected_conditionsにも影響する。
    selected_conditions = []
    for k in exp_index_list:
        print(conditions[k].phi_latex)
        selected_conditions.append(conditions[k])

    return selected_conditions, exp_name


def exp_017(exp_index_list, erase_t):
    """
    Example
    exp_index_list=[0,1,2,3,4,5]
    exp_index=0,1,2,3,4,5を実行する
    exp_indexは0〜239まである（range(240))

    設計理念
    ・関数はあくまで複数の実験を一つにまとめて実行する
    ・この複数の実験に番号をつけたがそれがexp_index（0からスタート）
    ・exp_index_listにリストで実行したいexp_index番号を指定されたものを実行する
    ・実験に関する情報は全てconditionに格納する
    ・今回のセッションで実験したい内容を、conditionsからexp_index_listをもとにselected_conditionsへ抽出する。
    :param exp_index_list: リストで実行したいexp_index番号を指定
    :return: 今回のセッションで実行する実験のconditionのリスト
    """
    exp_name = f"exp_017_erase_t={erase_t}"
    conditions = []
    # 0から239まで240回分の実験をconditionsにまとめる
    for i in range(240):
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 100

        x = sympy.Symbol('x')
        phi = x * sympy.pi / 240
        phi = phi.subs(x, i + 1)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.exp_index = i
        c.erase_t = erase_t
        conditions.append(c)

    # 今回のセッションで実験したい内容を、conditionsからexp_index_listをもとにselected_conditionsへ抽出する。
    # オブジェクトの格納でコピーではないので元のconditionsの変更はselected_conditionsにも影響する。
    selected_conditions = []
    for k in exp_index_list:
        print(conditions[k].phi_latex)
        selected_conditions.append(conditions[k])

    return selected_conditions, exp_name


def exp_018():
    """
    通常の量子ウォーク
    """
    exp_name = "exp_018"
    conditions = []

    c = Condition()
    set_basic_condition(c)
    c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
    c.algorithm = 2
    phi = 0  # phiは使わないので0を入れておく。
    c.phi = phi
    c.phi_latex = sympy.latex(phi)
    c.exp_name = exp_name
    c.exp_index = 0  # forで240回分のループをしないので、0を代入しておく
    conditions.append(c)

    return conditions, exp_name


def exp_019(exp_index_list):
    """
    erase_tごとに並列処理させる。exp_017の親戚。
    Example
        erase_t_list=[10,20,30,40]
        exp_019(erase_t_list)
        //erase_t=10,20,30,40とした場合の、exp_017を実行する。
    """
    exp_name = f"exp_019"
    conditions = []
    for i in range(600):
        c = Condition()
        set_basic_condition(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 100
        x = sympy.Symbol('x')
        phi = x * sympy.pi / 240
        phi = phi.subs(x, 4)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.exp_index = i
        c.erase_t = i
        conditions.append(c)

    # 今回のセッションで実験したい内容を、conditionsからexp_index_listをもとにselected_conditionsへ抽出する。
    # オブジェクトの格納でコピーではないので元のconditionsの変更はselected_conditionsにも影響する。
    selected_conditions = []
    for k in exp_index_list:
        print(conditions[k].phi_latex)
        selected_conditions.append(conditions[k])

    # 実行する際にerase_tの中身を確認
    for s_c in selected_conditions:
        print(f"t = {s_c.erase_t}")

    return selected_conditions, exp_name


if __name__ == '__main__':
    # x = sympy.Symbol('x')
    # phi = x * 2 * sympy.pi / 120
    # latex_txt = sympy.latex(phi)
    # print(latex_txt)
    c, exp_name = exp_5010_x_set()
    # print(c[0].phi)
    # print(c[0].phi_latex)
