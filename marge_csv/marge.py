def connect_csv():
    import pandas as pd
    import glob

    csv_files = glob.glob('./*.csv')
    data_list = []
    for i, file in enumerate(csv_files):
        if i == 0:
            data_list.append(pd.read_csv(file))
        else:
            data = pd.read_csv(file)
            data_list.append(data.iloc[:, 1])

    df = pd.concat(data_list, axis=1)
    df.to_csv('marge_result.csv', index=False)