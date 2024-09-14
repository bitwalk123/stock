from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import yfinance as yf

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Nikkei 225 index candlestick chart'),
    dcc.Checklist(
        id='toggle-rangeslider',
        options=[{'label': 'Include Rangeslider',
                  'value': 'slider'}],
        value=['slider']
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"),
    Input("toggle-rangeslider", "value"))
def display_candlestick(value):
    symbol = '^N225'
    ticker = yf.Ticker(symbol)
    df = ticker.history(period='6mo', interval='1d')

    """
    df = pd.read_csv(
        'https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')  # replace with your own data source
    """
    fig = go.Figure(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    ))

    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value
    )

    return fig


app.run_server(debug=True)
