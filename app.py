import os
import datetime
import numpy as np
import pandas as pd
import flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
from app_components import get_clock, get_logo, watchlist_content, get_row, tech_indiques
from kernel import load_ts, IndiqueCalculator
from app_callbacks import tech_fig_callbacks, update_row_callbacks, display_ticker_list_callbacks, update_pred_callbacks

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.config.supress_callback_exceptions = True
app.title = 'Chenjie Demo'

external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
    "https://cdn.rawgit.com/amadoukane96/8f29daabc5cacb0b7e77707fc1956373/raw/854b1dc5d8b25cd2c36002e1e4f598f5f4ebeee3/test.css",
    "https://use.fontawesome.com/releases/v5.2.0/css/all.css",
    "static/s4.css"
]
for css in external_css:
    app.css.append_css({"external_url": css})

left_div = html.Div([
    dcc.Interval(id="interval", interval=1 * 1000, n_intervals=0),
    html.Div([
        get_logo(),
        get_clock(),
        ],
        className='row'
    ),
    watchlist_content,
    ],
    className='container',
    style={"backgroundColor": "#080808","paddingLeft": "2%",
            "border":"2px solid #C8D4E3", 'float': 'center', 'marginRight': '20px'}
)

right_div = html.Div([
    dcc.Graph(id='ts_plot', figure=go.Figure([go.Scatter(x=[0],y=[0])])) 
    ],
    className='eleven columns',
    style={'backgroundColor': '#EFF5F5', "border": "2px solid #B5C0C7",
            "border-radius": "3px", 'float': 'left'})

visual = html.Div([
    html.Br(),
    html.Div([
        html.Div([left_div], className='four columns'),
        html.Div([right_div], className='eight columns')
        ],
        className='row'
    ),
    html.Br(),
    html.P(['0 0 0 0 0'], id='click_cache', style={'display': 'none'}),
    tech_indiques
    ],
    #style={'backgroundColor': '#191919'},
    style={'background-image': 'url(https://www.robovent.com/wp-content/uploads/blue-AutomotiveCalc_2018-background-1024x631.jpg)'}
)

disclaimer = html.Div([
    html.Br(),
    html.P("""Nothing on this web-app is to be taken as investment advice. 
    They are only for educational and research purposes. Questions: chenjie.yang@aiesec.net """),
    html.Br()
    ],
    className='row',
    style = {'backgroundColor': '#02101D', 'padding-left': '5%'}
    )

app.layout = html.Div([
    visual,
    disclaimer
    ]
) 

tech_inds = ['rsi', 'adx', 'obv', 'vpt', 'mfi', 'wr']
for i, ind in enumerate(tech_inds):
    app.callback(Output(f'{ind}_graph', 'figure'),
        [Input('chart_1_btn', 'n_clicks'),
        Input('chart_2_btn', 'n_clicks'),
        Input('chart_3_btn', 'n_clicks'),
        Input('chart_4_btn', 'n_clicks'),
        Input('chart_5_btn', 'n_clicks')],
        [State('click_cache', 'children'),
        State('ticker_1', 'children'),State('ticker_2', 'children'),
        State('ticker_3', 'children'),State('ticker_4', 'children'),
        State('ticker_5', 'children')]
    )(tech_fig_callbacks[i])

trends = ['up', 'down']
for i, tr in enumerate(trends):
    app.callback(Output(f'{tr}_pred', 'children'),
        [Input('chart_1_btn', 'n_clicks'),
        Input('chart_2_btn', 'n_clicks'),
        Input('chart_3_btn', 'n_clicks'),
        Input('chart_4_btn', 'n_clicks'),
        Input('chart_5_btn', 'n_clicks')],
        [State('click_cache', 'children'),
        State('ticker_1', 'children'),State('ticker_2', 'children'),
        State('ticker_3', 'children'),State('ticker_4', 'children'),
        State('ticker_5', 'children')]
    )(update_pred_callbacks[i])

@app.callback(Output("live_clock", "children"), [Input("interval", "n_intervals")])
def update_time(n):
    return datetime.datetime.now().strftime("%H:%M:%S")

for i in range(1, 6):
    idx = str(i)
    app.callback(
        Output(f'ticker_picker_{idx}', 'style'),
        [Input(f'change_{idx}_btn', 'n_clicks'), Input(f'ticker_{idx}_confirm', 'n_clicks'),
        Input(f'ticker_{idx}_cancel', 'n_clicks')],
        [State(f'ticker_picker_{idx}', 'style')]
    )(display_ticker_list_callbacks[i-1])

    app.callback(Output(f'row_{idx}', 'children'),
        [Input(f'ticker_{idx}_confirm', 'n_clicks')],
        [State(f'ticker_{idx}_cancel', 'n_clicks'), State(f'ticker_select_{idx}', 'value'), 
        State(f'row_{idx}', 'children')]
    )(update_row_callbacks[i-1])

@app.callback(Output('ts_plot', 'figure'),
    [Input('chart_1_btn', 'n_clicks'),
    Input('chart_2_btn', 'n_clicks'),
    Input('chart_3_btn', 'n_clicks'),
    Input('chart_4_btn', 'n_clicks'),
    Input('chart_5_btn', 'n_clicks')],
    [State('click_cache', 'children'),
    State('ticker_1', 'children'),State('ticker_2', 'children'),
    State('ticker_3', 'children'),State('ticker_4', 'children'),
    State('ticker_5', 'children'),State('range_select_1', 'value'),
    State('range_select_2', 'value'),State('range_select_3', 'value'),
    State('range_select_4', 'value'),State('range_select_5', 'value')]
)
def update_figure(n1, n2, n3, n4, n5, click_cache, t1, t2, t3, t4, t5, r1, r2, r3, r4, r5):
    click_cache = np.array(list(map(lambda n: int(n), click_cache[0].split(' '))))
    new_clicks = np.array([n1, n2, n3, n4, n5])
    idx = np.argmax(new_clicks - click_cache)
    t = np.array([t1, t2, t3, t4, t5])[idx]
    r = np.array([r1, r2, r3, r4, r5])[idx]
    df = load_ts(t, r)
    layout = go.Layout(title=t, paper_bgcolor='rgb(0,0,0)', plot_bgcolor='rgba(48, 48, 48, 0.3)',
                    margin={'l': 25, 'b': 0, 't': 40, 'r': 0}, font={'color': 'white'})
    data = [go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])]

    return go.Figure(data, layout=layout)

@app.callback(Output('click_cache', 'children'),
    [Input('ts_plot', 'figure')],
    [State('chart_1_btn', 'n_clicks'),
    State('chart_2_btn', 'n_clicks'),
    State('chart_3_btn', 'n_clicks'),
    State('chart_4_btn', 'n_clicks'),
    State('chart_5_btn', 'n_clicks')])
def update_cache(fig, n1, n2, n3, n4, n5):
    n_clicks = ' '.join([str(n1+0), str(n2+0), str(n3+0), str(n4+0), str(n5+0)])
    return [n_clicks]

if __name__ == '__main__':
    app.run_server(debug=True)