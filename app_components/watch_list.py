import datetime
import dash_html_components as html
import dash_core_components as dcc
from kernel import load_ts, ticker_list

modal_style = {
    'display': 'block',
    'position': 'fixed',
    'z-index': '1000',
    'left': '0',
    'top': '0',
    'width': '100%',
    'height': '100%',
    'overflow': 'auto',
    'background-color': 'rgba(0,0,0,0.4)'
}


tickers = ticker_list()

def extract_data(ticker):
    df = load_ts(ticker)
    return df['Close'].values[-1], df['Volume'].values[-1]

def get_row(idx, ticker, n_clicks=0):
    close, volume = extract_data(ticker)

    summary = html.Summary([
        html.Div([
            html.P(ticker, id=f'ticker_{idx}',className='three columns'),
            html.P(close, id=f'close_{idx}', className='three columns'),
            html.P(volume, id=f'volume_{idx}', className='three columns')
            ],
            className="row eleven columns",
            style={"height": "25","float":"right"},
        )],
        className='row',
        style={"paddingLeft":"10", 'color': 'white'}
)
    change_btn = html.Button(
                "Change",
                id=f"change_{idx}_btn",
                n_clicks=n_clicks,
                style={"margin": "0px 7px 7px 10px","textAlign": "center", "color": '#4286f4'},
                className='four columns'
            )
    chart_btn = html.Button(
                "Chart",
                id=f"chart_{idx}_btn",
                n_clicks=n_clicks,
                style={"margin": "0px 7px 7px 10px","textAlign": "center", "color": '#4286f4'},
                className='four columns'
    )
    
    btns = html.Div([change_btn, chart_btn], className='row')
    return html.Details([summary, btns], style={"textAlign": "center","paddingTop":"4"})

def get_picker(idx, ticker):
    content = html.Div([
        html.P(f'Asset {idx}'),
        dcc.Dropdown(
            id=f'ticker_select_{idx}',
            options=[
                {'label': t, 'value': t} for t in tickers
            ],
            value=ticker,
            style={'color': '#FAF69D'}
        ),
        dcc.Dropdown(
            id=f'range_select_{idx}',
            options=[
                {'label': '3 Months', 'value': '3m'},
                {'label': '6 Months', 'value': '6m'},
                {'label': '1 Year', 'value': '1yr'},
                {'label': '3 Years', 'value': '3yr'},
                {'label': 'Max', 'value': 'max'}],
            value='3m',
            style={'color': '#FAF69D'},
        )
        ],
        className='row'
    )
    btns = html.Div([
        html.Button('Confirm', id=f'ticker_{idx}_confirm', n_clicks=0, className='six columns'),
        html.Button('Cancel', id=f'ticker_{idx}_cancel', n_clicks=0, className='six columns'),
        ],
        className='row'
    )
    picker = html.Div([
        html.Div([
            content,
            html.Br(),
            btns
            ],
            className='container'
        )],
        className='modal-content',
        style={'backgroundColor': '#000000', 'color': 'white'}
    )
    return html.Div([picker], id=f'ticker_picker_{idx}', className='modal', style=modal_style) 

prediction = html.Div([
    html.H5('Next 7-day Predicted Movement', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.P(['Up (Probability)'],style={'textAlign': 'left'}),
            html.P(id='up_pred',style={'textAlign': 'left', 'color': 'white'})
        ],
        className='six columns',
        style={'padding-left': '5%'}
        ),
        html.Div([
            html.P(['Down (Probability)'],style={'textAlign': 'left'}),
            html.P(id='down_pred',style={'textAlign': 'left', 'color': 'white'})
        ],
        className='six columns'
        )],
        className='row'
    )
])

watchlist_content = html.Div([
    html.Div([
        html.P(
            "Code",
            className="five columns",
            style={'text-align': 'center', 'color': 'white'}
        ),
        html.P(
            "Close",
            className="two columns",
            style={'color': 'white'}
        ),
        html.P(
            "Volume",
            className="five columns",
            style={'color': 'white'}
        )],
        className='row'
    ),
    html.Div([get_row(1, 'AAPL')], id='row_1', style={"backgroundColor": "#222021"}),
    get_picker(1, 'AAPL'),
    html.Div(get_row(2, 'GS'), id='row_2'),
    get_picker(2, 'GS'),
    html.Div(get_row(3, 'NKE'), id='row_3', style={"backgroundColor": "#222021"}),
    get_picker(3, 'NKE'),
    html.Div([get_row(4, 'JNJ')], id='row_4'),
    get_picker(4, 'JNJ'),
    html.Div([get_row(5, 'WMT')], id='row_5', style={"backgroundColor": "#222021"}),
    get_picker(5, 'WMT'),
    prediction
])