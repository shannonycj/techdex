#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:25:54 2019

@author: chenjieyang
"""

import sqlite3
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta

def date_parser(d):
    return datetime.datetime.strptime(d, '%Y-%m-%d')

def load_ts(ticker, period='3m'):
    start = get_start_date(ticker, period)
    conn = sqlite3.connect('data/stocks.db')
    c = conn.cursor()
    cmd = f"SELECT * FROM stocks_{ticker} WHERE date(Date) >= date(?)"
    c.execute(cmd, (start, ))
    data = c.fetchall()
    ts_dict = {'Date': [], 'Open': [], 'High': [], 'Low': [], 'Close': [], 'Volume': []}
    for p in data:
        ts_dict['Date'].append(date_parser(p[0]))
        ts_dict['Open'].append(p[1])
        ts_dict['High'].append(p[2])
        ts_dict['Low'].append(p[3])
        ts_dict['Close'].append(p[4])
        ts_dict['Volume'].append(p[5])
    df = pd.DataFrame(ts_dict)
    df.set_index('Date', inplace=True)
    conn.close()
    return df

def get_start_date(ticker, period='3m'):
    conn = sqlite3.connect('data/stocks.db')
    c = conn.cursor()
    last_date = f"SELECT MAX(date(Date)) FROM stocks_{ticker}"
    c.execute(last_date)
    last_date = datetime.datetime.strptime(c.fetchall()[0][0], "%Y-%m-%d")
    if period == '3m':
        start_date = last_date + relativedelta(months=-3)
    elif period == '6m':
        start_date = last_date + relativedelta(months=-6)
    elif period == '1yr':
        start_date = last_date + relativedelta(years=-1)
    elif period == '3yr':
        start_date = last_date + relativedelta(years=-3)
    else:
        start_date = f"SELECT MIN(date(Date)) FROM stocks_{ticker}"
        c.execute(start_date)
        start_date = datetime.datetime.strptime(c.fetchall()[0][0], "%Y-%m-%d") 
    start = start_date.strftime('%Y-%m-%d')
    conn.close()
    return start

def ticker_list():
    conn = sqlite3.connect('data/stocks.db')
    c = conn.cursor()
    c.execute('SELECT ticker FROM stocks_meta')
    data = c.fetchall()
    tickers = []
    for d in data:
        tickers.append(d[0])
    return tickers

if __name__ == '__main__':
    import os
    load_ts('AAPL')