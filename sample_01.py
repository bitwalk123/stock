# Reference
# https://toukei-lab.com/python_stock

import yfinance as yf

#ターゲットを指定
symbol = '4755.T'
ticker = yf.Ticker(symbol)

#データを収集
df = ticker.history(period='5d', interval = '1d')
print(df)