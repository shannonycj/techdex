import datetime
import dash_html_components as html
import dash_core_components as dcc
from kernel import load_ts, IndiqueCalculator

indique_style = {'marginLeft': '0', 'marginRight': '0'}

rsi_indique = html.Div([
    dcc.Graph(id='rsi_graph')
    ],
    className='four columns',
    style=indique_style
)
adx_indique = html.Div([
    dcc.Graph(id='adx_graph')
    ],
    className='four columns',
    style=indique_style
)
obv_indique = html.Div([
    dcc.Graph(id='obv_graph')
    ],
    className='four columns',
    style=indique_style
)

vpt_indique = html.Div([
    dcc.Graph(id='vpt_graph')
    ],
    className='four columns',
    style=indique_style
)
mfi_indique = html.Div([
    dcc.Graph(id='mfi_graph')
    ],
    className='four columns',
    style=indique_style
)
wr_indique = html.Div([
    dcc.Graph(id='wr_graph')
    ],
    className='four columns',
    style=indique_style
)

first_indiques = html.Div([
        rsi_indique, adx_indique, obv_indique
        ],
        className='row',
        style={'float': 'center', 'padding-left': '5%', 'padding-right': '5%'}
    )
second_indiques = html.Div([
        vpt_indique, mfi_indique, wr_indique
        ],
        className='row',
        style={'float': 'center', 'padding-left': '5%', 'padding-right': '5%'}
    )


tech_indiques = html.Div([first_indiques, second_indiques], className='row')
    




