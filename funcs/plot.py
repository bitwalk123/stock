import pandas as pd
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import mplfinance as mpf
import pingouin as pg
import seaborn as sns
import yfinance as yf

from funcs.technical import psar


def plot_fontconfig():
    FONT_PATH = "../fonts/RictyDiminished-Regular.ttf"
    fm.fontManager.addfont(FONT_PATH)

    # FontPropertiesオブジェクト生成（名前の取得のため）
    font_prop = fm.FontProperties(fname=FONT_PATH)
    font_prop.get_name()
    plt.rcParams["font.family"] = font_prop.get_name()
    plt.rcParams["font.size"] = 16


def plot_mm_palabolic(ticker: yf.Ticker, df: pd.DataFrame, df0: pd.DataFrame):
    plot_fontconfig()

    fig = plt.figure(figsize=(12, 6))
    ax = dict()
    n = 2
    gs = fig.add_gridspec(
        n, 1, wspace=0.0, hspace=0.0, height_ratios=[2 if i == 0 else 1 for i in range(n)]
    )
    for i, axis in enumerate(gs.subplots(sharex="col")):
        ax[i] = axis
        ax[i].grid()

    mm005 = df0["Close"].rolling(5).median()
    mm025 = df0["Close"].rolling(25).median()
    mm075 = df0["Close"].rolling(75).median()

    dict_psar = psar(df)
    apds = [
        mpf.make_addplot(mm005[df.index], width=0.75, label=" 5d moving median", ax=ax[0]),
        mpf.make_addplot(mm025[df.index], width=0.75, label="25d moving median", ax=ax[0]),
        mpf.make_addplot(mm075[df.index], width=0.75, label="75d moving median", ax=ax[0]),
        mpf.make_addplot(
            dict_psar["bear"],
            type="scatter",
            marker="o",
            markersize=10,
            color="blue",
            label="down trend",
            ax=ax[0],
        ),
        mpf.make_addplot(
            dict_psar["bull"],
            type="scatter",
            marker="o",
            markersize=10,
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

    if "longName" in ticker.info.keys():
        title = "Daily chart for %s (%s)\nwith Moving Medians and Parabolic SAR" % (
            ticker.info["longName"],
            ticker.info['symbol'],
        )
    elif "shortName" in ticker.info.keys():
        title = "Daily chart for %s (%s)\nwith Moving Medians and Parabolic SAR" % (
            ticker.info["shortName"],
            ticker.info['symbol'],
        )
    else:
        title = "Daily chart for %s\nwith Moving Medians and Parabolic SAR" % ticker.info['symbol']
    ax[0].set_title(title)

    ax[0].legend(loc="best", fontsize=9)


def plot_robust_bollinger(ticker: yf.Ticker, df: pd.DataFrame, df0: pd.DataFrame):
    plot_fontconfig()

    fig, ax = plt.subplots(figsize=(12, 6))

    # Bollinger bands
    period = 20
    mv_median = df0["Close"].rolling(period).median()
    mv_q1 = df0["Close"].rolling(period).quantile(0.25)
    mv_q3 = df0["Close"].rolling(period).quantile(0.75)
    mv_iqr = mv_q3 - mv_q1
    mv_lower = mv_q1 - mv_iqr * 1.5
    mv_upper = mv_q3 + mv_iqr * 1.5

    apds = [
        mpf.make_addplot(
            mv_upper[df.index],
            width=1.25,
            color="C1",
            linestyle="dotted",
            label="Upper bound",
            ax=ax,
        ),
        mpf.make_addplot(
            mv_q3[df.index],
            width=1,
            color="C2",
            linestyle="dashed",
            label="Q3 (75%)",
            ax=ax,
        ),
        mpf.make_addplot(
            mv_median[df.index], width=0.75, color="C3", label="Median", ax=ax
        ),
        mpf.make_addplot(
            mv_q1[df.index],
            width=1,
            color="C4",
            linestyle="dashed",
            label="Q1 (25%)",
            ax=ax,
        ),
        mpf.make_addplot(
            mv_lower[df.index],
            width=1.25,
            color="C5",
            linestyle="dotted",
            label="Lower bound",
            ax=ax,
        ),
    ]

    mpf.plot(
        df,
        type="candle",
        style="default",
        addplot=apds,
        datetime_format="%y-%m-%d",
        xrotation=0,
        ax=ax,
    )

    ax.grid()
    ax.legend(loc="best", fontsize=9)

    if "longName" in ticker.info.keys():
        title = "Daily chart for %s (%s)\nwith robust Bollinger bands (period=%ddays)" % (
            ticker.info["longName"],
            ticker.info['symbol'],
            period,
        )
    elif "shortName" in ticker.info.keys():
        title = "Daily chart for %s (%s)\nwith robust Bollinger bands (period=%ddays)" % (
            ticker.info["shortName"],
            ticker.info['symbol'],
            period,
        )
    else:
        title = "Daily chart for %s\nwith robust Bollinger bands (period=%ddays)" % (
            ticker.info['symbol'],
            period,
        )
    ax.set_title(title)


def plot_histogram_qqplot(ticker: yf.Ticker, df: pd.DataFrame):
    plot_fontconfig()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    sns.histplot(df["Close"], kde=True, ax=axes[0])

    # ヒストグラム
    axes[0].set_xlabel("Close")
    axes[0].set_ylabel("count")
    axes[0].grid(axis="y")
    axes[0].set_title("Histogram", fontsize=16)

    # Q-Q プロット
    pg.qqplot(df["Close"], s=10, ax=axes[1])
    axes[1].set_title("Q-Q plot", fontsize=16)
    axes[1].grid()

    if "longName" in ticker.info.keys():
        title = "Daily chart for %s (%s), n = %d" % (ticker.info["longName"], ticker.info['symbol'], len(df))
    elif "shortName" in ticker.info.keys():
        title = "Daily chart for %s (%s), n = %d" % (ticker.info["shortName"], ticker.info['symbol'], len(df))
    else:
        title = "Daily chart for %s, n = %d" % (ticker.info['symbol'], len(df))
    plt.suptitle(title, fontsize=18, )
