import pandas as pd


class AppRes:
    tse = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"

    def getJPXTickerList(self) -> pd.DataFrame:
        return pd.read_excel(self.tse)
