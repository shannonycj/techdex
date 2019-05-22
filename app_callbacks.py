import numpy as np
import plotly.graph_objs as go
from kernel import load_ts, IndiqueCalculator
from app_components import get_row


# tech indicator callbacks
# ------------------------------------------------------------------------------------------------------------
def update_rsi_figure(n1, n2, n3, n4, n5, click_cache, t1, t2, t3, t4, t5):
    click_cache = np.array(list(map(lambda n: int(n), click_cache[0].split(' '))))
    new_clicks = np.array([n1, n2, n3, n4, n5])
    idx = np.argmax(new_clicks - click_cache)
    t = np.array([t1, t2, t3, t4, t5])[idx]
    df = load_ts(t)
    df.sort_index(inplace=True)
    ic = IndiqueCalculator(df, t)
    rsi = ic.get_rsi()
    data = [go.Scatter(x=rsi.index, y=rsi.values)]
    layout = go.Layout(title='3 mos RSI', paper_bgcolor='rgba(0, 0, 0, 0.7)', plot_bgcolor='rgba(48, 48, 48, 0.7)',
                    margin={'l': 40, 'b': 40, 't': 40, 'r': 0}, font={'color': 'white'}, 
                    height=300)
    return go.Figure(data, layout=layout)

def update_adx_figure(n1, n2, n3, n4, n5, click_cache, t1, t2, t3, t4, t5):
    click_cache = np.array(list(map(lambda n: int(n), click_cache[0].split(' '))))
    new_clicks = np.array([n1, n2, n3, n4, n5])
    idx = np.argmax(new_clicks - click_cache)
    t = np.array([t1, t2, t3, t4, t5])[idx]
    df = load_ts(t)
    df.sort_index(inplace=True)
    ic = IndiqueCalculator(df, t)
    adx = ic.get_adx()
    data = [go.Scatter(x=adx.index, y=adx.values)]
    layout = go.Layout(title='3 mos ADX', paper_bgcolor='rgba(0, 0, 0, 0.7)', plot_bgcolor='rgba(48, 48, 48, 0.7)',
                    margin={'l': 40, 'b': 40, 't': 40, 'r': 0}, font={'color': 'white'}, 
                    height=300)
    return go.Figure(data, layout=layout)

def update_obv_figure(n1, n2, n3, n4, n5, click_cache, t1, t2, t3, t4, t5):
    click_cache = np.array(list(map(lambda n: int(n), click_cache[0].split(' '))))
    new_clicks = np.array([n1, n2, n3, n4, n5])
    idx = np.argmax(new_clicks - click_cache)
    t = np.array([t1, t2, t3, t4, t5])[idx]
    df = load_ts(t)
    df.sort_index(inplace=True)
    ic = IndiqueCalculator(df, t)
    obv = ic.get_obv()
    data = [go.Scatter(x=obv.index, y=obv.values)]
    layout = go.Layout(title='3 mos OBV', paper_bgcolor='rgba(0, 0, 0, 0.7)', plot_bgcolor='rgba(48, 48, 48, 0.7)',
                    margin={'l': 40, 'b': 40, 't': 40, 'r': 0}, font={'color': 'white'}, 
                    height=300)
    return go.Figure(data, layout=layout)

def update_vpt_figure(n1, n2, n3, n4, n5, click_cache, t1, t2, t3, t4, t5):
    click_cache = np.array(list(map(lambda n: int(n), click_cache[0].split(' '))))
    new_clicks = np.array([n1, n2, n3, n4, n5])
    idx = np.argmax(new_clicks - click_cache)
    t = np.array([t1, t2, t3, t4, t5])[idx]
    df = load_ts(t)
    df.sort_index(inplace=True)
    ic = IndiqueCalculator(df, t)
    vpt = ic.get_vpt()
    data = [go.Scatter(x=vpt.index, y=vpt.values)]
    layout = go.Layout(title='3 mos VPT', paper_bgcolor='rgba(0, 0, 0, 0.7)', plot_bgcolor='rgba(48, 48, 48, 0.7)',
                    margin={'l': 40, 'b': 40, 't': 40, 'r': 0}, font={'color': 'white'}, 
                    height=300)
    return go.Figure(data, layout=layout)

def update_mfi_figure(n1, n2, n3, n4, n5, click_cache, t1, t2, t3, t4, t5):
    click_cache = np.array(list(map(lambda n: int(n), click_cache[0].split(' '))))
    new_clicks = np.array([n1, n2, n3, n4, n5])
    idx = np.argmax(new_clicks - click_cache)
    t = np.array([t1, t2, t3, t4, t5])[idx]
    df = load_ts(t)
    df.sort_index(inplace=True)
    ic = IndiqueCalculator(df, t)
    mfi = ic.get_mfi()
    data = [go.Scatter(x=mfi.index, y=mfi.values)]
    layout = go.Layout(title='3 mos MFI', paper_bgcolor='rgba(0, 0, 0, 0.7)', plot_bgcolor='rgba(48, 48, 48, 0.7)',
                    margin={'l': 40, 'b': 40, 't': 40, 'r': 0}, font={'color': 'white'}, 
                    height=300)
    return go.Figure(data, layout=layout)

def update_wr_figure(n1, n2, n3, n4, n5, click_cache, t1, t2, t3, t4, t5):
    click_cache = np.array(list(map(lambda n: int(n), click_cache[0].split(' '))))
    new_clicks = np.array([n1, n2, n3, n4, n5])
    idx = np.argmax(new_clicks - click_cache)
    t = np.array([t1, t2, t3, t4, t5])[idx]
    df = load_ts(t)
    df.sort_index(inplace=True)
    ic = IndiqueCalculator(df, t)
    wr = ic.get_wr()
    data = [go.Scatter(x=wr.index, y=wr.values)]
    layout = go.Layout(title='3 mos William%R', paper_bgcolor='rgba(0, 0, 0, 0.7)', plot_bgcolor='rgba(48, 48, 48, 0.7)',
                    margin={'l': 40, 'b': 40, 't': 40, 'r': 0}, font={'color': 'white'}, 
                    height=300)
    return go.Figure(data, layout=layout)

tech_fig_callbacks = [update_rsi_figure, update_adx_figure, update_obv_figure, update_vpt_figure,
                    update_mfi_figure, update_wr_figure]
# ------------------------------------------------------------------------------------------------------------
# movement prediction callbacks
# ============================================================================================================
def update_up_pred(n1, n2, n3, n4, n5, click_cache, t1, t2, t3, t4, t5):
    click_cache = np.array(list(map(lambda n: int(n), click_cache[0].split(' '))))
    new_clicks = np.array([n1, n2, n3, n4, n5])
    idx = np.argmax(new_clicks - click_cache)
    t = np.array([t1, t2, t3, t4, t5])[idx]
    df = load_ts(t)
    df.sort_index(inplace=True)
    ic = IndiqueCalculator(df, t)
    pred = ic.load_predict()
    return str(round(pred[0][1]*100, 1)) + '%'

def update_down_pred(n1, n2, n3, n4, n5, click_cache, t1, t2, t3, t4, t5):
    click_cache = np.array(list(map(lambda n: int(n), click_cache[0].split(' '))))
    new_clicks = np.array([n1, n2, n3, n4, n5])
    idx = np.argmax(new_clicks - click_cache)
    t = np.array([t1, t2, t3, t4, t5])[idx]
    df = load_ts(t)
    df.sort_index(inplace=True)
    ic = IndiqueCalculator(df, t)
    pred = ic.load_predict()
    return str(round(pred[0][0]*100, 1)) + '%'

update_pred_callbacks = [update_up_pred, update_down_pred]
# ============================================================================================================

def display_ticker_1_list(n_b, n_c, n_x, s):
    if n_b == (n_c + n_x):
        s['display'] = 'none'
        return s
    else:
        s['display'] = 'block'
        return s

def update_row_1(n_c, n_x, ticker, c):
    if n_c > 0:
        return get_row(1, ticker, n_c + n_x)
    else:
        return c

def show_range_1(n_b, n_c, n_x):
    if n_b == n_c + n_x:
        return {'display': 'none'}
    else:
        return {'display': 'block'}

def display_ticker_2_list(n_b, n_c, n_x, s):
    if n_b == (n_c + n_x):
        s['display'] = 'none'
        return s
    else:
        s['display'] = 'block'
        return s

def update_row_2(n_c, n_x, ticker, c):
    if n_c > 0:
        return get_row(2, ticker, n_c + n_x)
    else:
        return c

def show_range_2(n_b, n_c, n_x):
    if n_b == n_c + n_x:
        return {'display': 'none'}
    else:
        return {'display': 'block'}

def display_ticker_3_list(n_b, n_c, n_x, s):
    if n_b == (n_c + n_x):
        s['display'] = 'none'
        return s
    else:
        s['display'] = 'block'
        return s

def update_row_3(n_c, n_x, ticker, c):
    if n_c > 0:
        return get_row(3, ticker, n_c + n_x)
    else:
        return c

def show_range_3(n_b, n_c, n_x):
    if n_b == n_c + n_x:
        return {'display': 'none'}
    else:
        return {'display': 'block'}

def display_ticker_4_list(n_b, n_c, n_x, s):
    if n_b == (n_c + n_x):
        s['display'] = 'none'
        return s
    else:
        s['display'] = 'block'
        return s

def update_row_4(n_c, n_x, ticker, c):
    if n_c > 0:
        return get_row(4, ticker, n_c + n_x)
    else:
        return c

def show_range_4(n_b, n_c, n_x):
    if n_b == n_c + n_x:
        return {'display': 'none'}
    else:
        return {'display': 'block'}

def display_ticker_5_list(n_b, n_c, n_x, s):
    if n_b == (n_c + n_x):
        s['display'] = 'none'
        return s
    else:
        s['display'] = 'block'
        return s

def update_row_5(n_c, n_x, ticker, c):
    if n_c > 0:
        return get_row(5, ticker, n_c + n_x)
    else:
        return c

def show_range_5(n_b, n_c, n_x):
    if n_b == n_c + n_x:
        return {'display': 'none'}
    else:
        return {'display': 'block'}

display_ticker_list_callbacks = [display_ticker_1_list, display_ticker_2_list, display_ticker_3_list,
                                display_ticker_4_list, display_ticker_5_list]

update_row_callbacks = [update_row_1, update_row_2, update_row_3, update_row_4, update_row_5]

show_range_callbacks = [show_range_1, show_range_2, show_range_3, show_range_4, show_range_5]