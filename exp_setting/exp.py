from simulation.codition import Condition
from simulation.codition import set_basic_condition_1
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
        set_basic_condition_1(c)
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
        set_basic_condition_1(c)
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
        set_basic_condition_1(c)
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
        set_basic_condition_1(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        # x軸のみに電場を加えるため、アルゴリズム番号は3番
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
        set_basic_condition_1(c)
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
        set_basic_condition_1(c)
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
    for i in range(1, 61):
        c = Condition()
        set_basic_condition_1(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 3

        x = sympy.Symbol('x')
        phi = x * sympy.pi / 4
        phi = phi.subs(x, i)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.index = i-1
        conditions.append(c)
    return conditions, exp_name


def exp_3010_x_set():
    """x軸に電場をかけた_pi/60刻み。1から60"""
    exp_name = "exp_3010"
    conditions = []
    for i in range(1, 61):
        c = Condition()
        set_basic_condition_1(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 3

        x = sympy.Symbol('x')
        phi = x * 2 * sympy.pi / 120
        phi = phi.subs(x, i)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        conditions.append(c)
    return conditions, exp_name


def exp_3011_x_set():
    """x軸に電場をかけた_2pi/120刻み。i=61から120まで"""
    exp_name = "exp_3011"
    conditions = []
    for i in range(61, 121):
        c = Condition()
        set_basic_condition_1(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 3

        x = sympy.Symbol('x')
        phi = x * 2 * sympy.pi / 120
        phi = phi.subs(x, i)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        conditions.append(c)
    return conditions, exp_name


def exp_3030_xy_set():
    """xとy軸に電場をかけた_2pi_120刻み。i=1から60まで"""
    exp_name = "exp_3030"
    conditions = []
    for i in range(1, 61):
        c = Condition()
        set_basic_condition_1(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 5
        x = sympy.Symbol('x')
        phi = x * 2 * sympy.pi / 120
        phi = phi.subs(x, i)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        conditions.append(c)
    return conditions, exp_name


def exp_3031_xy_set():
    """xとy軸に電場をかけた_2pi_120刻み。i=61から120まで"""
    exp_name = "exp_3031"
    conditions = []
    for i in range(61, 121):
        c = Condition()
        set_basic_condition_1(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = 5
        x = sympy.Symbol('x')
        phi = x * 2 * sympy.pi / 120
        phi = phi.subs(x, i)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        conditions.append(c)
    return conditions, exp_name


def exp_5010_x_set():
    """x軸に電場をかけた。pi/整数の位相でシミュレーションする。"""
    exp_name = "exp_3031"
    conditions = []
    for i in range(1, 21):
        c = Condition()
        set_basic_condition_1(c)
        c.PSY_init = 1 / 2 * np.array([1, 1, -1, -1])
        c.algorithm = None
        x = sympy.Symbol('x')
        phi = sympy.pi / x
        phi = phi.subs(x, i)
        print(phi)
        c.phi = float(phi.evalf())
        c.phi_latex = sympy.latex(phi)
        c.exp_name = exp_name
        c.index = i-1
        conditions.append(c)
    return conditions, exp_name


if __name__ == '__main__':
    # x = sympy.Symbol('x')
    # phi = x * 2 * sympy.pi / 120
    # latex_txt = sympy.latex(phi)
    # print(latex_txt)
    c, exp_name = exp_5010_x_set()
    # print(c[0].phi)
    # print(c[0].phi_latex)
