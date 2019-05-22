import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import randint as sp_randint
from sklearn.metrics import classification_report
from joblib import dump, load


class IndiqueCalculator:
    def __init__(self, df, ticker):
        self.df = df
        self.ticker = ticker
    
    def load_predict(self):
        self.prepare_data()
        self.clf = load(f'models/{self.ticker}_clf.joblib')
        self.scaler = load(f'models/{self.ticker}_scaler.joblib')
        X_pred = self.scaler.transform(self.df_feature.iloc[-1, :].values.reshape(1, -1))
        log_prob = self.clf.predict_log_proba(X_pred)
        return np.exp(log_prob)
        
    def prepare_data(self):
        keys = ['Date', 'rsi', 'adx', 'obv', 'vpt', 'mfi', 'wr']
        rsi = self.get_rsi()
        adx = self.get_adx()
        obv = self.get_obv()
        vpt = self.get_vpt()
        mfi = self.get_mfi()
        wr = self.get_wr()
        vals = [rsi.index, rsi.values, adx.values, obv.values, vpt.values, mfi.values, wr.values]
        df_feature = pd.DataFrame(dict(list(zip(keys, vals))))
        df_feature.set_index('Date', inplace=True)
        self.df_feature = df_feature
        
    def train_clf(self):
        df_feature = self._get_label(self.df_feature, self.df, 7)
        X = df_feature.drop('returns', axis=1).values
        y = df_feature.returns.values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        self.scaler = MinMaxScaler()
        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)
        y_train = y_train > 0
        y_test = y_test > 0
        
        param_grid = {"max_depth": [10, 20, 40, None],
                                  "max_features": sp_randint(1, 6),
                                  "min_samples_split": sp_randint(5, 50),
                                  "min_samples_leaf": sp_randint(5, 50),
                                  "bootstrap": [True, False],
                                  "criterion": ["gini", "entropy"]}
        clf = RandomForestClassifier(verbose=0, n_estimators=100)
        clf_grid = RandomizedSearchCV(clf, param_distributions=param_grid,
                                                   n_iter=10, cv=3, iid=False)
        clf_grid.fit(X_train, y_train)
        y_pred = clf_grid.predict(X_test)
        print(classification_report(y_test, y_pred))
        self.clf = clf_grid.best_estimator_
        dump(self.clf, f'models/{self.ticker}_clf.joblib')
        dump(self.scaler, f'models/{self.ticker}_scaler.joblib')
        
        
    @staticmethod
    def _get_label(df_feature, df, lag=1):
        ret = (df.Close - df.Close.shift(-lag))/df.Close.shift(-lag)
        df_feature['returns'] = ret
        return df_feature.dropna(how='any')
    
    def get_wr(self):
        wr = []
        dates = []
        for i in range(len(self.df)):
            if i + 14 > len(self.df) - 1:
                break
            high = self.df.iloc[i:i+14, :]['High'].max()
            low = self.df.iloc[i:i+14, :]['Low'].min()
            close = self.df.iloc[i+14, :]['Close']
            dates.append(self.df.index[i+14])
            wr.append((high - close)*(-100)/(high - low))
        wr = pd.Series(wr, dates)
        return wr[wr.index > self.df.index[14]]


    
    def get_vpt(self):
        vpt = self.df['Close'].pct_change() * self.df['Volume']
        vpt = vpt.cumsum()
        return vpt[vpt.index > self.df.index[14]]

    def get_mfi(self):
        n_mfi = len(self.df) - 13
        mfi = []
        idx = []
        for i in range(n_mfi):
            df_sous = self.df.iloc[i:i+14]    
            typical_price = (df_sous['Close'] + df_sous['Low'] + df_sous['High']) / 3
            pos_money_flow = np.sum(typical_price * (typical_price.diff() > 0).astype('float') * df_sous['Volume'])
            neg_money_flow = np.sum(typical_price * (typical_price.diff() < 0).astype('float') * df_sous['Volume'])
            money_ratio = pos_money_flow/neg_money_flow
            mfi.append(100 - (100/(1+money_ratio)))
            idx.append(df_sous.index[-1])
        mfi = pd.Series(mfi, idx)
        return mfi[mfi.index > self.df.index[14]]
        
    def get_obv(self):
        pos_diff = (self.df['Close'].diff() > 0).astype('float')
        neg_diff = (self.df['Close'].diff() < 0).astype('float')
        v = self.df['Volume'] * pos_diff - self.df['Volume'] * neg_diff
        obv = v.cumsum()
        return obv[obv.index > self.df.index[14]]

    def get_adx(self):
        up_move = self.df['High'].diff()
        down_move = self.df['Low'].shift(1) - self.df['Low']
        hl = self.df['High'] - self.df['Low']
        hc = np.abs(self.df['High'] - self.df['Close'].shift(1))
        lc = np.abs(self.df['Low'] - self.df['Close'].shift(1))
        tr = np.max([hl, hc, lc], axis=0)
        tr = pd.Series(tr, hl.index)
        pdi = 100 * (IndiqueCalculator.__exp_smooth((up_move > down_move) * (up_move > 0).astype('float') * up_move)) / tr
        ndi = 100 * (IndiqueCalculator.__exp_smooth((down_move > up_move) * (down_move > 0).astype('float') * down_move)) / tr
        adx = 100 * IndiqueCalculator.__exp_smooth(np.abs(pdi - ndi)/np.abs(pdi+ndi))
        return adx[adx.index > self.df.index[14]]

    def get_rsi(self):
        self.df.sort_index(inplace=True)
        diff = self.df['Close'].diff()
        U = IndiqueCalculator.__exp_smooth(np.maximum(diff, 0))
        D = IndiqueCalculator.__exp_smooth(np.maximum(-diff, 0))
        RS = U/D
        RSI = 100 - (100/(1 + RS))
        return RSI[RSI.index > self.df.index[14]]

    @staticmethod
    def __exp_smooth(arr, span=14):
        alpha = 1/span
        es_arr = []
        for i, a in enumerate(arr):
            if i < 14:
                es_arr.append(arr[:14].mean())
            else:
                es_arr.append(es_arr[i-1]*(1-alpha) + a*alpha)
        return pd.Series(es_arr, index=arr.index)