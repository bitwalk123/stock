import pandas as pd
import wget

if __name__ == '__main__':
    # JPX ticker list
    tse = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    filename = wget.download(tse)
    df = pd.read_excel(filename)
    print(df)
