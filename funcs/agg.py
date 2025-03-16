import re

import unicodedata

import pandas as pd

from funcs.conv import df_to_html


def aggregate_up_down_ratio(df: pd.DataFrame, top: int = 100) -> tuple[list, str]:
    # 列名の変更
    list_col = list(df.columns)
    col = list(df.columns).index('市場・商品区分')
    list_col[col] = '区分'
    df.columns = list_col

    # 「日時」列が 'None' の行を除外
    df = df[df['日時'] != 'None'].copy()

    # ユニークな日時を抽出
    dates = df['日時'].unique()

    # 万が一複数の日時が存在した場合、一番新しい日時のデータのみ扱う
    dt = sorted(dates, reverse=True)
    df = df[df['日時'] == dt[0]].copy()

    # 「変化率」列で逆ソート
    df = df.sort_values('変化率', ascending=False).reset_index(drop=True)

    # 順位が判るようにインデックス列から「#」列を作成
    df['#'] = df.index + 1

    # 「銘柄名」列の文字列を規格化
    df['銘柄名'] = [unicodedata.normalize('NFKC', s) for s in df['銘柄名']]

    # 「市場・商品区分」列の '（内国株式）' を除外
    """
    pattern = re.compile(r'(.+)（内国株式）')
    list_s = list()
    for s in df['市場・商品区分']:
        m = pattern.match(s)
        if m:
            list_s.append(m.group(1))
        else:
            list_s.append(m)
    df['市場・商品区分'] = list_s
    """
    list_category = list()
    for s in df['区分']:
        if s == 'グロース（内国株式）':
            list_category.append('G')
        elif s == 'スタンダード（内国株式）':
            list_category.append('S')
        elif s == 'プライム（内国株式）':
            list_category.append('P')
        else:
            list_category.append(s)
    df['区分'] = list_category

    list_header = [
        '#',
        'コード',
        '銘柄名',
        '区分',
        '33業種区分',
        '高値',
        '安値',
        '変化率',
        '出来高',
        '増減',
    ]
    df_result = df[list_header].copy()
    list_col_format = ['int', 'code', 'str', 'str', 'str', 'int', 'int', 'float', 'int', 'str']

    list_html = df_to_html(df_result.iloc[0:top], list_col_format)
    file_html = 'report/%04d/up_down_ratio_%02d-%02d.html' % (dt[0].year, dt[0].month, dt[0].day)

    return list_html, file_html
