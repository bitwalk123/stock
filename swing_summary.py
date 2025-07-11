import os

import pandas as pd

if __name__ == '__main__':
    path_base = "swing"
    dir_year = "2025"
    name_excel = "20250712.xlsx"
    path_file = os.path.join(path_base, dir_year, name_excel)
    df0 = pd.read_excel(path_file)
    col_date = "約定日\n受渡日"
    col_code = "銘柄\n銘柄コード"
    col_profit = "実現損益(円)"

    df = pd.DataFrame()
    df["Date"] = [s.split("\n")[0] for s in df0[col_date]]
    df["Code"] = df0[col_code]
    print(df)
