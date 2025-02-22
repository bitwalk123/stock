import os
import re
import sys
import time
import unicodedata

import numpy as np
import pandas as pd
import yfinance as yf

from structs.res import AppRes
from funcs.conv import df_to_html

if __name__ == '__main__':
    # JPX ticker list
    res = AppRes()
    df_tse = res.getJPXTickerList()

    market_target = ['グロース（内国株式）', 'スタンダード（内国株式）', 'プライム（内国株式）']
    df_target = df_tse[df_tse['市場・商品区分'].isin(market_target)].reset_index(drop=True)
    df_target['コード'] = df_target['コード'].astype(str)
    df_target['日時'] = None
    df_target['日時'] = df_target['日時'].astype(str)
    df_target['高値'] = np.nan
    df_target['安値'] = np.nan
    df_target['変化率'] = np.nan
    df_target['出来高'] = np.nan
    df_target['増減'] = None
    df_target['増減'] = df_target['増減'].astype(str)

    for r in range(len(df_target)):
        code = df_target.at[r, 'コード']
        symbol = '%s.T' % code
        ticker = yf.Ticker(symbol)
        try:
            df = ticker.history(period='1d')
        except Exception as e:
            print(e)
            time.sleep(60)
            df = ticker.history(period='1d')

        if len(df) > 0:
            v_open = df['Open'].iloc[0]
            v_high = df['High'].iloc[0]
            v_low = df['Low'].iloc[0]
            v_close = df['Close'].iloc[0]
            v_volume = df['Volume'].iloc[0]

            df_target.at[r, '高値'] = v_high
            df_target.at[r, '安値'] = v_low
            df_target.at[r, '変化率'] = (v_high - v_low) * 2 / (v_high + v_low)
            df_target.at[r, '出来高'] = v_volume
            df_target.at[r, '日時'] = df.index[0]

            if v_open > v_close:
                df_target.at[r, '増減'] = '▼'
            elif v_open < v_close:
                df_target.at[r, '増減'] = '△'
            else:
                df_target.at[r, '増減'] = '-'

    # 「日時」列が 'None' の行を除外
    df_target = df_target[df_target['日時'] != 'None'].copy()

    # ユニークな日時を抽出
    dates = df_target['日時'].unique()
    # 万が一複数の日時が存在した場合、一番新しい日時のデータのみ扱う
    dt = sorted(dates, reverse=True)
    df_target = df_target[df_target['日時'] == dt[0]].copy()

    # 「変化率」列で逆ソート
    df_target = df_target.sort_values('変化率', ascending=False).reset_index(drop=True)

    # 順位が判るようにインデックス列から「#」列を作成
    df_target['#'] = df_target.index + 1

    # 「銘柄名」列の文字列を規格化
    df_target['銘柄名'] = [unicodedata.normalize('NFKC', s) for s in df_target['銘柄名']]

    # 「市場・商品区分」列の '（内国株式）' を除外
    pattern = re.compile(r'(.+)（内国株式）')
    list_s = list()
    for s in df_target['市場・商品区分']:
        m = pattern.match(s)
        if m:
            list_s.append(m.group(1))
        else:
            list_s.append(m)
    df_target['市場・商品区分'] = list_s

    list_header = ['#', 'コード', '銘柄名', '市場・商品区分', '33業種区分', '高値', '安値', '変化率', '出来高', '増減']
    df_result = df_target[list_header].copy()

    list_col_format = ['int', 'str', 'str', 'str', 'str', 'int', 'int', 'float', 'int', 'str']
    list_html = df_to_html(df_result.iloc[0:50], list_col_format)

    file_html = 'report/%04d/up_down_ratio_%02d-%02d.html' % (dt[0].year, dt[0].month, dt[0].day)
    with open(file_html, mode='w') as f:
        f.writelines(list_html)
