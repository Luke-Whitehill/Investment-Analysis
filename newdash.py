import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import mysql.connector
import plotly.express as px
import talib as ta
from collections import deque
import plotly.graph_objs as go
import plotly.tools as tls
import plotly
import talib as ta


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = ['https://codepen.io/saransh/pen/BKJun.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


my_connect = mysql.connector.connect(
    host = "",
    user = '',
    passwd = "",
    database = "")

df1 = pd.read_sql("SELECT * FROM cnnfgifull", my_connect)


fig = px.line(df1, x = 'Date', y = 'today')






app.layout = html.Div(#style = {'backgroundColor': 'black'},
children=[
    html.H1('Dashboard'),
    
    html.P(
        children = "Attemping to make a dashboard with useful analytics for visual analysis of equities. "
    ),
    html.H3('Price'),
    dcc.Input(id = 'input', value = 'a2masx', placeholder = 'Enter ASX Ticker...', type = 'text'),
    html.Div(id = 'output-graph'),
    html.Div(id = 'rets-histogram'),
    #New Div

    
    # html.Div([
    #     html.Div([
    #         html.H3(children = 'Histogram of Returns'),
    #         dcc.Graph(id = 'histogram_graph', figure = fig1
    #         ),
    #     ], className ='six columns'),
    #     html.Div([
    #         html.H3(children = 'Time Sries of % Returns'),
    #         dcc.Graph(
    #             id = 'timeseries_returns',
    #             figure = fig2
    #         ),
    #     ], className ='six columns'),
    # ],className = 'row'),


    #New Div
    html.Div([
        html.H3(children = 'CNN Fear Greed Index'),

        html.Div(children = '''
            What emotion is driving the market now?
            '''),
        dcc.Graph(
            id = 'graph2',
            figure = fig
        ),              
    ]),

    #New Div
    # html.Div([
    #     dcc.Dropdown(
    #         id = 'dropdown',
    #         options = [
    #             {'label': 'A2 Milk', 'value': 'a2masx'},
    #             {'label': 'ADBRI Limited', 'value':'abcasx'},
    #             {'label': 'Abacus Property Group', 'value':'abpasx'},
    #             {'label': 'AGL Energy Limited', 'value': 'aglasx'}
    #         ],
    #         value = 'MTL'
    #     )
    # ]),
    # #New Div
    # html.Div([
    #     html.Div('Example Div', style = {'color':'blue', 'fontSize': 14}),
    #     html.P('Example P', className = 'my-class', id='my-p-element')
    # ], style = {'marginBottom': 50, 'martinTop':250})
])


@app.callback(
    Output(component_id = 'output-graph', component_property = 'children'),
    [Input(component_id = 'input', component_property = 'value')]
    )
def update_graph(input_data):
    my_connect = mysql.connector.connect(
    host = "192.168.0.15",
    user = 'user1',
    passwd = "stocks",
    database = "financialdata")

    query = "SELECT * FROM "+input_data
    df = pd.read_sql(query, my_connect)
    def slowstochsignal(fastkperiod = 14, slowkperiod = 3, slowkmatype = 0 , slowdperiod = 3, slowdmatype = 0):
        df['slowk'], df['slowd'] = ta.STOCH(df['High'], df['Low'], df['Close'], fastk_period= fastkperiod, 
        slowk_period= slowkperiod, slowk_matype= slowkmatype, slowd_period= slowdperiod, slowd_matype= slowdmatype)
        return df
    df = slowstochsignal()
    df['date'] = pd.to_datetime(df['Date']).dt.date
    df['MMA30'] = df.Close.rolling(window = 30).mean()
    df['dailyrets'] = df['Adj Close'].pct_change()

    price_graph =  dcc.Graph(
        id = 'example-graph',
        figure={
            'data':[
                {'x' : df['Date'], 'y': df['Adj Close'], 'type':'line', 'name': input_data}
            ],
            'layout': {
                'title':"Price of: "+input_data
            }
        }
    )
    returns_graph = dcc.Graph(
        id = 'returns-graph',
        figure = {
            'data':[
                {'x': df['Date'], 'y': df['dailyrets'], 'type':'line', 'name': input_data}
            ],
            'layout': {
                'title': "Price of: "+input_data
            }
        }
    )
    trace1 = go.Scatter(
        x = df['Date'],
        y = df['Close'],
        name = "Price"
    )
    trace2 = go.Scatter(
        x = df['Date'],
        y = df['MMA30'],
        name = "MMA30"
    )
    trace3 = go.Bar(
        x = df['Date'],
        y = df['Volume']
    )
    data = [trace1,trace2]
    #fig = go.Figure(data=data)
    fig = go.Figure(data = data).set_subplots(4,1, shared_xaxes = True, vertical_spacing = 0.012)
    #fig = make_subplots(rows = 2, cols = 1, shared_xaxes= True)
    # fig.add_trace(
    #     go.scatter(x = df['Date'], y = df['Close']),
    #     row = 1, col = 1
    # )
    # fig.add_trace(
    #     go.scatter(x = df['Date'], y = df['MMA30']),
    #     row = 1, col = 1
    # )
    fig.add_trace(
        go.Bar(x = df['Date'], y = df['Volume'], name = "Volume", marker_color = "black"),
        row = 2, col = 1
    )
    # fig.update_layout(
    #     title = "Chart of "+input_data,
    #     legend_title = "Legend",
    #     # title = {
    #     #     'text': "Chart of "+input_data,
    #     #     'xanchor': 'centre',
    #     #     'yanchor': 'top'
    #     # }
    # )
    fig.add_trace(
        go.Scatter(x = df['Date'], y = df['dailyrets'], name = 'Daily Returns %', marker_color = 'steelblue'),
        row = 3, col = 1
    )
    fig.add_trace(
        go.Scatter(x = df['Date'], y = df['slowk'], name = 'Slow Stochastics'),
        row = 4, col = 1
    )
    fig.update_layout(
    title={
        'text': "Chart of "+input_data,
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    showlegend = False,

        )
    figure_graph = dcc.Graph(figure = fig)
    x = df['dailyrets']
    fig1 = go.Figure(data = [go.Histogram(x = x)])
    figure1_graph = dcc.Graph(figure = fig1)

    


    return figure_graph, figure1_graph #,price_graph, returns_graph, 
@app.callback(
    Output(component_id = 'timeseriesreturns', component_property = 'children'),
    [Input(component_id = 'input1', component_property = 'value')]
    )
def update_timeseries(input_data1):
    my_connect = mysql.connector.connect(
    host = "192.168.0.15",
    user = 'user1',
    passwd = "stocks",
    database = "financialdata")
    query = "SELECT * FROM "+input_data1
    df = pd.read_sql(query, my_connect)
    #query = "SELECT * FROM"+input_data
    df = pd.read_sql(query, my_connect)
    df['date'] = pd.to_datetime(df['Date']).dt.date
    df['dailyrets'] = df['Adj Close'].pct_change()

    return dcc.Graph(
        id = 'timeseriesreturns',
        figure = {
            'data':[
                {'x': df['Date'], 'y': df['dailyrets'], 'type':'line', 'name':input_data1}
            ],
            'layout': {
                'title':"Daily Time Series Returns of: "+input_data1
            }
        }
    )
if __name__ == '__main__':
    app.run_server(debug = True)

