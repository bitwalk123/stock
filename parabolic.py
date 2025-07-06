import os
import time

import pandas as pd
import yfinance as yf

from funcs.tse import get_ticker_list
from module.psar import ParabolicSAR

if __name__ == '__main__':
    # 対象銘柄リストの取得
    df = get_ticker_list()
    df_result = pd.DataFrame({
        "Date": list(),
        "Close": list(),
        "Volume": list(),
        "Trend": list(),
    })
    df_result.index.name = "Code"
    df_result = df_result.astype(object)
    base_dir = "parabolic"
    path_dir_day = ""

    for r in range(len(df)):
        code = df.at[r, "コード"]
        symbol = f"{code}.T"
        ticker = yf.Ticker(symbol)
        try:
            df_ticker = ticker.history(period="3y", interval="1d")
        except Exception as e:
            print(e)
            # ３分待って再試行
            time.sleep(180)
            df_ticker = ticker.history(period="3y", interval="1d")

        if len(df_ticker) == 0:
            continue

        df_ticker_latest = df_ticker.tail(1)
        # 指定範囲の株価を対象
        price_min = 100
        price_max = 1000
        volume_min = 100000
        if df_ticker_latest["Close"].iloc[0] < price_min:
            continue
        if df_ticker_latest["Close"].iloc[0] > price_max:
            continue

        # 出来高の小さいものは除外
        if df_ticker_latest["Volume"].iloc[0] < 100000:
            continue

        psar = ParabolicSAR()
        psar.calc(df_ticker)
        df_ticker_latest = df_ticker.tail(1)
        if df_ticker.tail(2)["Trend"].sum() == 0:
            if df_ticker_latest["Trend"].iloc[0] > 0:
                dt_latest = df_ticker_latest.index[0]
                y = f"{dt_latest.year:04}"
                m = f"{dt_latest.month:02}"
                d = f"{dt_latest.day:02}"

                path_dir_year = os.path.join(base_dir, y)
                if not os.path.exists(path_dir_year):
                    os.mkdir(path_dir_year)
                path_dir_month = os.path.join(path_dir_year, m)
                if not os.path.exists(path_dir_month):
                    os.mkdir(path_dir_month)
                path_dir_day = os.path.join(path_dir_month, d)
                if not os.path.exists(path_dir_day):
                    os.mkdir(path_dir_day)

                df_result.at[code, "Date"] = f"{y}-{m}-{d}"
                df_result.at[code, "Close"] = df_ticker_latest["Close"].iloc[0]
                df_result.at[code, "Volume"] = df_ticker_latest["Volume"].iloc[0]
                df_result.at[code, "Trend"] = df_ticker_latest["Trend"].iloc[0]

    print(df_result)
    file_output = os.path.join(path_dir_day, "parabolic.xlsx")
    df_result.to_excel(file_output)