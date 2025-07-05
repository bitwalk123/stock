import pandas as pd


class ParabolicSAR:
    def __init__(self, af_init: float = 0.02, af_step: float = 0.02, af_max: float = 0.2):
        self.af_init = af_init
        self.af_step = af_step
        self.af_max = af_max

    def calc(self, df: pd.DataFrame):
        length = len(df)
        bull = True
        af = self.af_init
        t = df.index[0]
        ep = df.at[t, "Low"]
        price_high = df.at[t, "High"]
        price_low = df.at[t, "Low"]

        df["PSAR"] = df["Close"]

        for i in range(2, length):
            t0 = df.index[i - 2]
            t1 = df.index[i - 1]
            t2 = df.index[i]

            if bull:
                df.at[t2, "PSAR"] = df.at[t1, "PSAR"] + af * (price_high - df.at[t1, "PSAR"])
            else:
                df.at[t2, "PSAR"] = df.at[t1, "PSAR"] + af * (price_low - df.at[t1, "PSAR"])
            reverse = False

            if bull:
                if df.at[t2, "Low"] < df.at[t2, "PSAR"]:
                    bull = False
                    reverse = True
                    df.at[t2, "PSAR"] = price_high
                    price_low = df.at[t2, "Low"]
                    af = self.af_init
            else:
                if df.at[t2, "High"] > df.at[t2, "PSAR"]:
                    bull = True
                    reverse = True
                    df.at[t2, "PSAR"] = price_low
                    price_high = df.at[t2, "High"]
                    af = self.af_init

            if not reverse:
                if bull:
                    if df.at[t2, "High"] > price_high:
                        price_high = df.at[t2, "High"]
                        af = min(af + self.af_step, self.af_max)
                    if df.at[t1, "Low"] < df.at[t2, "PSAR"]:
                        df.at[t2, "PSAR"] = df.at[t1, "Low"]
                    if df.at[t0, "Low"] < df.at[t2, "PSAR"]:
                        df.at[t2, "PSAR"] = df.at[t0, "Low"]
                else:
                    if df.at[t2, "Low"] < price_low:
                        price_low = df.at[t2, "Low"]
                        af = min(af + self.af_step, self.af_max)
                    if df.at[t1, "High"] > df.at[t2, "PSAR"]:
                        df.at[t2, "PSAR"] = df.at[t1, "High"]
                    if df.at[t0, "High"] > df.at[t2, "PSAR"]:
                        df.at[t2, "PSAR"] = df.at[t0, "High"]

            if bull:
                df.at[t2, "Bull"] = df.at[t2, "PSAR"]
            else:
                df.at[t2, "Bear"] = df.at[t2, "PSAR"]
