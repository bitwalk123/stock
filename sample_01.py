# Reference
# https://toukei-lab.com/python_stock

import yfinance as yf

#ターゲットを指定
ticker = '4755.T'

#データを収集
data = yf.download(ticker , period='7d', interval = '1d')