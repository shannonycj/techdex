#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 17:08:03 2019

@author: chenjieyang
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import quandl
#%%
quandl.ApiConfig.api_key = 'cvB2sbT5kazKsUd6MWgW'
quandl.get('WSE/TSGAMES', start_date='2019-05-16', end_date='2019-05-16')
#%%
import pandas as pd
df_meta = pd.read_csv('data/WSE_metadata.csv')
#%%
import sqlite3
#%%

#%%
meta.columns
#%%
cols = [t + ' text,' for t in meta.columns]
cols = ' '.join(cols)
cols = cols[:-1]
#%%
print(cols[:-1])
#%%
command = f"CREATE TABLE wse_meta ({cols})"
c.execute(command)
#%%
conn.commit()
#%%
meta.values[1]
#%%
', '.join(meta.values[0])
#%%
for i in range(len(meta)):
    
    conn.commit()
#%%
c.execute("SELECT * FROM wse_meta")
#%%

meta = c.fetchall()
#%%
import datetime

#%%
df = get_ts('ZUE', '2010-11-03', '2019-05-16')
#%%
def get_ts(ticker, s, e):
    code = 'WSE/{}'.format(ticker)
    ts = quandl.get(code, start_date=s, end_date=e)
    return ts
conn = sqlite3.connect('data/stocks.db')
c = conn.cursor()
for i in range(len(meta)):
    if i > 501:
        try:
            meta_data = meta[i]
            ticker = meta_data[0]
            s = meta_data[-2]
            e = meta_data[-1]
            drop_command = f"DROP TABLE IF EXISTS stock_{ticker}"
            c.execute(drop_command)
            conn.commit()
            cols = 'date text, Open real, High real, Low real, Close real, pct_change real, Volume real, num_of_trades real, Turnover real'
            command = f"CREATE TABLE stock_{ticker} ({cols})"
            c.execute(command)
            conn.commit()
            
            df = get_ts(ticker, s, e)
            for j in range(len(df)):
                date = str(df.index[j])[:-9]
                insert_cmd = f"INSERT INTO stock_{ticker} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                v = df.values[j]
                c.execute(insert_cmd, (date, v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7]))
                conn.commit()
            print('finished {}/{}'.format(i+1, len(meta)))
        except Exception as e:
            print(str(e))
#%%
conn.close()
            


