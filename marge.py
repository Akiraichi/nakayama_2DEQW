import pandas as pd
import glob
import matplotlib.pyplot as plt


def connect_csv(folder_name):
    import pandas as pd
    import glob

    csv_files = glob.glob(f'{folder_name}/*.csv')
    csv_files.sort()

    data_list = []
    for i, file in enumerate(csv_files):
        if i == 0:
            data_list.append(pd.read_csv(file))
        else:
            data = pd.read_csv(file)
            data_list.append(data.iloc[:, 1])

    df = pd.concat(data_list, axis=1)

    return df


def change_columns(df, str_flag):
    # 列名を変更する
    column_list = df.columns.values  # 今の列名を全て取得する
    column_list = [column[-4:] for column in column_list]  # 最後の4文字がtなので抽出する
    # 最初の1文字目以外は数字なので、intで初めの00を消しておく
    for i in range(1, len(column_list)):
        if str_flag:
            column_list[i] = "$t_{erase}=$" + str(int(column_list[i]))
        else:
            column_list[i] = int(column_list[i])
    df = df.set_axis(column_list, axis='columns')  # 列名を一括して書き換える
    return df


def plot_t(df, path, step_t_list):
    """
    tステップで比較したい時のプロット
    横軸：exp番号。つまり電場を消した時の時間ステップ
    縦軸：KLダイバージェンス
    """
    # 列名を変更する
    df = change_columns(df, str_flag=False)

    # 行名を変更する
    df = df.set_index("t")  # 列名がtである列をindexとして使用する
    index_list = df.index.values  # 今の行名を全て取得する
    index_list = ["t=" + str(index) for index in index_list]
    df = df.set_axis(index_list, axis='index')  # 行名を一括して書き換える

    # プロットする
    ax = df.loc["t=" + str(step_t_list[0])].plot(grid=True, x="t=0", figsize=(8, 6))  # step_tステップ目のデータを抽出してプロットする
    ax.set_xlabel("$t_{erase}$", size=24, labelpad=5)
    ax.set_ylabel("$KL divergence$", size=24)

    for i in range(1, len(step_t_list)):
        df.loc["t=" + str(step_t_list[i])].plot(grid=True, x="t", figsize=(8, 6), ax=ax)  # 同じ表に次々とプロットしていく
    plt.legend()
    # plt.show()
    plt.savefig(f"{path}/compare_erase_t.png", dpi=400)


def plot_index(df, path, t_erase_list, start_t):
    """
    indexで比較したい時に使う
    横軸：時間発展ステップ数
    縦軸：KLダイバージェンス
    """
    df = change_columns(df, str_flag=True)

    """dfの中から指定したものを抽出する"""
    select = ["t"]
    for t_erase in t_erase_list:
        s = "$t_{erase}=$"
        s += str(t_erase)
        select.append(s)
    df = df[select]

    """start_tから先のものを抽出する"""
    # start_tのindex番号を取得する
    index = df.query(f't == {start_t}').index[0]
    # index番号以降のデータを抽出する
    df = df[index:]
    ax = df.plot(grid=True, x="t", figsize=(8, 6))
    ax.set_xlabel("$t$", size=24, labelpad=5)
    ax.set_ylabel("$KL divergence$", size=24)

    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()
    # plt.show()
    plt.savefig(f"{path}/marge.png", dpi=400)


if __name__ == '__main__':
    """フォルダ選択"""
    # フォルダ名を指定すると、そのフォルダ内のcsvファイルをマージしたものとプロットした結果を返す
    folder_list = glob.glob(f'result/KL_div_marge/*')
    for i, folder in enumerate(folder_list):
        print(f"（{i}）", folder)
    select = int(input("どのフォルダにしますか？"))
    path = f'{folder_list[select]}/csv'
    # path = f'{folder_list[select]}/csv_in_circle'
    print(path)

    """選択したフォルダのcsvを結合"""
    df = connect_csv(path)
    # plot_t(df, path, [100, 200, 300, 400, 500, 600])
    plot_t(df, path, [100, 200, 300, 400, 500, 1000, 2000])
    # plot_t(df, path, [100,120, 140, 160, 180, 200])
    # plot_t(df, path, [220, 240, 260, 280, 300, 400, 500, 600])
    # plot_t(df, path, [300, 320, 340, 360, 380, 400, 500, 600])
    # plot_t(df, path, list(range(400, 620, 20)))
    # plot_t(df, path, list(range(280, 620, 20)))
    # plot_t(df, path, list(range(220, 400, 20)))

    # plot_t(df, path, list(range(600, 2000, 100)))

    # plot_index(df, path, [10, 20, 30, 100, 200, 300], start_t=200)
    # plot_index(df, path, t_erase_list=[100, 200, 300, 400, 500], start_t=800)
