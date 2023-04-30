# Reference
# https://toukei-lab.com/python_stock

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import yfinance as yf

#ターゲットを指定
ticker = '4755.T'

#データを収集
data = yf.download(ticker , period='7d', interval = '1d')