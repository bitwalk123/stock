import plotly.graph_objects as go
import yfinance as yf

symbol = '^N225'
ticker = yf.Ticker(symbol)
df = ticker.history(period='3mo', interval='1d')

fig = go.Figure(
    data=go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )
)
fig.update_layout(
    title='Nikkei 225',
    xaxis_title='Date',
    yaxis_title='Price',
    font_size=16,
)
fig.update_traces(
    line_width=1,
    selector=dict(type='candlestick')
)
fig.update(
    layout_xaxis_rangeslider_visible=False
)
#fig.write_html('report_20240913_daily_chart_n225.html')
fig.show()
