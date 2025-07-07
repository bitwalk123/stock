import os

import pandas as pd

if __name__ == '__main__':
    url_base = "https://raw.githubusercontent.com/bitwalk123/stock/refs/heads/main/parabolic"
    y = "2025"
    m = "07"
    d = "07"
    url_target = os.path.join(url_base, y, m, d)
    url_table = os.path.join(url_target, "parabolic.xlsx")
    df = pd.read_excel(url_table)
    list_html = list()
    list_html.append('<table class="simple">')
    list_html.append('<thead>')
    list_html.append('<tr>')
    list_html.append('<th>Code</th>')
    list_html.append('<th>Date</th>')
    list_html.append('<th>Close</th>')
    list_html.append('<th>Volume</th>')
    list_html.append('<th>Trend</th>')
    list_html.append('<th>Go</th>')
    list_html.append('<th>Note</th>')
    list_html.append('</tr>')
    list_html.append('</thead>')
    list_html.append('<tbody>')

    for r in range(len(df)):
        list_html.append('<tr>')
        for c in df.columns:
            v = df.at[r, c]
            if c == "Code":
                url_image = os.path.join(url_target, f"{v}.png")
                list_html.append(f'<td nowrap><a href="{url_image}" target="_blank">{v}</a></td>')
            elif c == "Date":
                list_html.append(f'<td nowrap>{v}</td>')
            elif c == "Close":
                list_html.append(f'<td nowrap style="text-align: right;">{v:.1f}</td>')
            elif c == "Volume":
                list_html.append(f'<td nowrap style="text-align: right;">{v:d}</td>')
            elif c == "Trend":
                list_html.append(f'<td nowrap style="text-align: right;">{v:d}</td>')
            elif c == "Note":
                if pd.isna(v):
                    list_html.append(f'<td></td>')
                else:
                    list_html.append(f'<td style="text-align: left;">{v}</td>')
            else:
                list_html.append(f'<td>{v}</td>')

        list_html.append('</tr>')

    list_html.append('</tbody>')
    list_html.append('</table>')

    for line in list_html:
        print(line)
