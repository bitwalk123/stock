import os
import unicodedata

import pandas as pd

if __name__ == '__main__':
    url_yahoo = "https://finance.yahoo.co.jp/quote"
    path_base = "swing"
    dir_year = "2025"
    name_excel = "20250719.xlsx"
    path_file = os.path.join(path_base, dir_year, name_excel)
    df0 = pd.read_excel(path_file)
    col_date = "約定日\n受渡日"
    col_code = "銘柄\n銘柄コード"
    col_profit = "実現損益(円)"

    df = pd.DataFrame()
    df["Date"] = [s.split("\n")[0] for s in df0[col_date]]
    df["Code"] = [f'{s.split("\n")[1]}' for s in df0[col_code]]
    df["Name"] = [f'{s.split("\n")[0]}' for s in df0[col_code]]
    df["Profit"] = df0[col_profit]

    # HTML のテーブルを標準出力
    print('<table class="simple">')

    print('<thead>')
    print('<tr>')
    print('<th>Date</th>')
    print('<th>Code</th>')
    print('<th>Name</th>')
    print('<th>Profit</th>')
    print('</tr>')
    print('</thead>')

    print('<tbody>')
    for r in range(len(df)):
        print('<tr>')
        # 約定日
        print(f'<td nowrap>{df.at[r, "Date"]}</td>')

        # コード
        code = df.at[r, "Code"]
        url_quote = os.path.join(url_yahoo, f"{code}.T")
        print(f'<td nowrap><a href="{url_quote}" target="_blank">{code}</a></td>')

        # 銘柄名
        name = unicodedata.normalize('NFKC', df.at[r, "Name"])
        print(f'<td nowrap>{name}</td>')

        # 損益
        print(f'<td nowrap style="text-align: right;">{int(df.at[r, "Profit"]):,}</td>')
        print('</tr>')

    print('<tr>')
    print(f'<td nowrap>&nbsp;</td>')
    print(f'<td nowrap>&nbsp;</td>')
    print(f'<td nowrap style="text-align: right;">実現損益</td>')
    print(f'<td nowrap style="text-align: right;">{int(df["Profit"].sum()):,}</td>')
    print('</tr>')

    print('</tbody>')
    print('</table>')
    total = df["Profit"].sum()
