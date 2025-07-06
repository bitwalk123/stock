import time

import yfinance as yf

from funcs.tse import get_ticker_list
from module.psar import ParabolicSAR

if __name__ == '__main__':
    # 対象銘柄リストの取得
    df = get_ticker_list()

    for r in range(len(df)):
        code = df.at[r, 'コード']
        symbol = '%s.T' % code
        ticker = yf.Ticker(symbol)
        try:
            df_ticker = ticker.history(period="2y", interval="1d")
        except Exception as e:
            print(e)
            # ３分待って再試行
            time.sleep(180)
            df_ticker = ticker.history(period="2y", interval="1d")

        if len(df_ticker) == 0:
            continue

        # 指定範囲の株価を対象
        if df_ticker.tail(1)["Close"].iloc[0] < 100:
            continue
        if df_ticker.tail(1)["Close"].iloc[0] > 1000:
            continue

        # 出来高の小さいものは除外
        if df_ticker.tail(1)["Volume"].iloc[0] < 100000:
            continue

        psar = ParabolicSAR()
        psar.calc(df_ticker)
        if df_ticker.tail(2)["Trend"].sum() == 0:
            if df_ticker.tail(1)["Trend"].iloc[0] > 0:
                print(f"\n{code}")
                print(df_ticker.tail(2)[["Close", "Volume", "Trend"]])
