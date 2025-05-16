import time

import yfinance as yf

from funcs.agg import aggregate_up_down_ratio
from funcs.tse import get_ticker_list

if __name__ == '__main__':
    # 対象銘柄リストの取得
    df = get_ticker_list()

    for r in range(len(df)):
        code = df.at[r, 'コード']
        symbol = '%s.T' % code
        ticker = yf.Ticker(symbol)
        try:
            df_ticker = ticker.history(period='1d')
        except Exception as e:
            print(e)
            # ３分待って再試行
            time.sleep(180)
            df_ticker = ticker.history(period='1d')

        if len(df_ticker) == 0:
            continue

        v_open = df_ticker['Open'].iloc[0]
        v_high = df_ticker['High'].iloc[0]
        v_low = df_ticker['Low'].iloc[0]
        v_close = df_ticker['Close'].iloc[0]
        v_volume = df_ticker['Volume'].iloc[0]

        # 始値と終値の平均が 100 円未満の銘柄は除外
        if (v_open + v_close) / 2 < 100:
            continue

        # 出来高が 1,000,000 株未満の銘柄は除外
        if v_volume < 1000000:
            continue

        df.at[r, '高値'] = v_high
        df.at[r, '安値'] = v_low
        df.at[r, '変動率'] = (v_high - v_low) * 2 / (v_open + v_close)
        df.at[r, '出来高'] = v_volume
        df.at[r, '日時'] = df_ticker.index[0]

        if v_open > v_close:
            df.at[r, '増減'] = '▼'
        elif v_open < v_close:
            df.at[r, '増減'] = '△'
        else:
            df.at[r, '増減'] = '-'

    # 変動率の集計
    list_html, file_html = aggregate_up_down_ratio(df)

    # 結果の出力
    with open(file_html, mode='w') as f:
        f.writelines(list_html)
