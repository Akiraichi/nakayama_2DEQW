import pandas as pd
import glob
import matplotlib.pyplot as plt


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


def plot_t(df, path, step_t_list, file_name):
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
    plt.savefig(f"{path}/{file_name}.png", dpi=400)


def plot_index(df, path, t_erase_list, start_t, file_name):
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
    plt.savefig(f"{path}/{file_name}.png", dpi=400)


def plot_index_prob(df, path, t_erase_list, start_t, file_name):
    """
       indexで比較したい時に使う
       横軸：時間発展ステップ数
       縦軸：確率
    """
    df = change_columns(df, str_flag=False)

    """dfの中から指定したものを抽出する"""
    select = ["t"] + t_erase_list
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
    plt.savefig(f"{path}/{file_name}.png", dpi=400)


class Marge:
    def __init__(self, type):
        self.type = type
        self.file_name = None
        if type == "KL":
            folder_list = glob.glob(f'result/KL_div_marge/*')

        elif type == "prob":
            folder_list = glob.glob(f'result/prob/*')
        else:
            raise Exception
        self.__select(folder_list)

    def __select(self, folder_list):
        for i, folder in enumerate(folder_list):
            print(f"（{i}）", folder)
        select = int(input("どのフォルダにしますか？"))
        if self.type == "KL":
            # self.path = f'{folder_list[select]}/csv'
            self.path = f'{folder_list[select]}/csv_in_circle'
        elif self.type == "prob":
            self.path = f'{folder_list[select]}'
        print(self.path)

    def __connect_csv(self):
        csv_files = glob.glob(f'{self.path}/*.csv')
        csv_files.sort()
        if self.type == "KL":
            data_list = []
            for i, file in enumerate(csv_files):
                if i == 0:
                    data_list.append(pd.read_csv(file))
                else:
                    data = pd.read_csv(file)
                    data_list.append(data.iloc[:, 1])
            df = pd.concat(data_list, axis=1)
            return df

        elif self.type == "prob":
            in_circle_list = []
            out_circle_list = []
            circle_list = []
            for i, file in enumerate(csv_files):
                df = pd.read_csv(file)
                index = file[-8:-4]
                print(index)  # デバッグ
                if i == 0:
                    in_circle_list.append(df.loc[:, ['t', f'in_circle_{index}']])
                    out_circle_list.append(df.loc[:, ['t', f'out_circle_{index}']])
                    circle_list.append(df.loc[:, ['t', f'circle_{index}']])
                else:
                    in_circle_list.append(df.loc[:, [f'in_circle_{index}']])
                    out_circle_list.append(df.loc[:, [f'out_circle_{index}']])
                    circle_list.append(df.loc[:, [f'circle_{index}']])

            df_in = pd.concat(in_circle_list, axis=1)
            df_out = pd.concat(out_circle_list, axis=1)
            df_circle = pd.concat(circle_list, axis=1)
            return df_in, df_out, df_circle

    def plot_t(self, t_list):
        if self.type == "KL":
            """選択したフォルダのcsvを結合"""
            df = self.__connect_csv()
            plot_t(df, self.path, step_t_list=t_list, file_name=f"KL_{t_list}")
        elif self.type == "prob":
            df_in, df_out, df_circle = self.__connect_csv()
            plot_t(df_in, self.path, step_t_list=t_list, file_name=f"prob_in_{t_list}")
            plot_t(df_out, self.path, step_t_list=t_list, file_name=f"prob_out_{t_list}")
            plot_t(df_circle, self.path, step_t_list=t_list, file_name=f"prob_circle_{t_list}")

    def plot_index(self, indexes, start_t):
        if self.type == "KL":
            """選択したフォルダのcsvを結合"""
            df = self.__connect_csv()
            plot_index(df, self.path, t_erase_list=indexes, start_t=start_t,
                       file_name=f"KL_start_t={start_t}_indexes={indexes}")
        elif self.type == "prob":
            df_in, df_out, df_circle = self.__connect_csv()
            plot_index_prob(df_in, self.path, indexes, start_t=start_t,
                            file_name=f"prob_in_start_t={start_t}_indexes={indexes}")
            plot_index_prob(df_out, self.path, indexes, start_t=start_t,
                            file_name=f"prob_out_start_t={start_t}_indexes={indexes}")
            plot_index_prob(df_circle, self.path, indexes, start_t=start_t,
                            file_name=f"prob_circle_start_t={start_t}_indexes={indexes}")


if __name__ == '__main__':
    marge = Marge(type="KL")
    # t_list = [100, 200, 300, 400, 500, 1000, 2000]
    t_list = list(range(400, 2100, 200))
    # t_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    # t_list = [100, 200, 300, 400, 500, 1000, 2000]
    # indexes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500]
    # indexes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    # indexes = [100, 150, 200, 250, 300, 350, 400, 450, 500]
    marge.plot_t(t_list=t_list)
    # marge.plot_index(indexes=indexes, start_t=900)
