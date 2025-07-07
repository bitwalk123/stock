import datetime
import os
import time

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import yfinance as yf

from funcs.tse import get_ticker_list
from module.psar import ParabolicSAR

if __name__ == '__main__':
    # 対象銘柄リストの取得
    df_tse = get_ticker_list()
    df_result = pd.DataFrame({
        "Date": list(),
        "Close": list(),
        "Volume": list(),
        "Trend": list(),
        "Go": list(),
        "Note": list(),
    })
    df_result.index.name = "Code"
    df_result = df_result.astype(object)
    base_dir = "parabolic"
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)

    path_dir_day = ""

    for r in range(len(df_tse)):
        code = df_tse.at[r, "コード"]
        name = df_tse.at[r, "銘柄名"]
        symbol = f"{code}.T"
        ticker = yf.Ticker(symbol)
        try:
            df0 = ticker.history(period="3y", interval="1d")
        except Exception as e:
            print(e)
            # ３分待って再試行
            time.sleep(180)
            df0 = ticker.history(period="3y", interval="1d")

        if len(df0) == 0:
            continue

        df_ticker_latest = df0.tail(1)
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
        psar.calc(df0)
        df_ticker_latest = df0.tail(1)
        if df0.tail(2)["Trend"].sum() == 0:
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

                date_str = f"{y}-{m}-{d}"
                df_result.at[code, "Date"] = date_str
                df_result.at[code, "Close"] = df_ticker_latest["Close"].iloc[0]
                df_result.at[code, "Volume"] = df_ticker_latest["Volume"].iloc[0]
                df_result.at[code, "Trend"] = df_ticker_latest["Trend"].iloc[0]

                # チャート
                dt_last = df0.index[len(df0) - 1]
                tdelta_1y = datetime.timedelta(days=365)
                df = df0[df0.index >= dt_last - tdelta_1y].copy()

                FONT_PATH = "fonts/RictyDiminished-Regular.ttf"
                fm.fontManager.addfont(FONT_PATH)

                # FontPropertiesオブジェクト生成（名前の取得のため）
                font_prop = fm.FontProperties(fname=FONT_PATH)
                font_prop.get_name()

                plt.rcParams["font.family"] = font_prop.get_name()
                plt.rcParams["font.size"] = 14
                fig = plt.figure(figsize=(12, 8))
                ax = dict()
                n = 2
                gs = fig.add_gridspec(
                    n, 1, wspace=0.0, hspace=0.0, height_ratios=[3 if i == 0 else 1 for i in range(n)]
                )
                for i, axis in enumerate(gs.subplots(sharex="col")):
                    ax[i] = axis
                    ax[i].grid()

                mm05 = df0["Close"].rolling(5).median()
                mm25 = df0["Close"].rolling(25).median()
                mm75 = df0["Close"].rolling(75).median()

                apds = [
                    mpf.make_addplot(mm05[df.index], width=0.75, label=" 5d moving median", ax=ax[0]),
                    mpf.make_addplot(mm25[df.index], width=0.75, label="25d moving median", ax=ax[0]),
                    mpf.make_addplot(mm75[df.index], width=0.75, label="75d moving median", ax=ax[0]),
                    mpf.make_addplot(
                        df["Bear"],
                        type="scatter",
                        marker="o",
                        markersize=5,
                        color="blue",
                        label="down trend",
                        ax=ax[0],
                    ),
                    mpf.make_addplot(
                        df["Bull"],
                        type="scatter",
                        marker="o",
                        markersize=5,
                        color="red",
                        label="up trend",
                        ax=ax[0],
                    ),
                ]

                mpf.plot(
                    df,
                    type="candle",
                    style="default",
                    volume=ax[1],
                    datetime_format="%m-%d",
                    addplot=apds,
                    xrotation=0,
                    ax=ax[0],
                )

                ax[0].legend(loc="best", fontsize=8)
                ax[0].set_title(f"{name} ({code}) on {date_str}")

                plt.tight_layout()
                chart_name = os.path.join(path_dir_day, f"{code}.png")
                plt.savefig(chart_name)
                plt.close()

    print(df_result)
    file_output = os.path.join(path_dir_day, "parabolic.xlsx")
    df_result.to_excel(file_output)