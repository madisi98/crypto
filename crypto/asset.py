import os
from datetime import datetime

import pandas as pd
from .client import client


class Asset:
    def __init__(self, crypto, fiat, granularity=300):
        self.crypto = crypto
        self.fiat = fiat
        self.pair = '-'.join((crypto, fiat))
        self.granularity = int(granularity)
        self.df = None

    def calculate_colors(self):
        self.df['colors'] = self.df['close'] > self.df['open']

    def calculate_obv(self):
        obv = self.df['volume'].copy()
        obv[self.df['close'] < self.df['close'].shift(1)] = -obv
        obv.loc[self.df['close'] == self.df['close'].shift(1)] = 0
        self.df['OBV'] = obv.cumsum()

    def _calc_rsi(self, w):
        var = self.df['close']
        var = var / var.shift(1) - 1
        var = pd.concat([var.shift(x) for x in range(w)], axis=1).dropna()
        self.df[f'RSI_{w}'] = 100 - 100 / (1 + var[var > 0].mean(axis=1) / var[var < 0].mean(axis=1).abs())
        self.df[f'RSI_{w}'] = self.df[f'RSI_{w}'].fillna(50)

    def calculate_rsis(self, rsis):
        if isinstance(rsis, int):
            self._calc_rsi(rsis)
        elif isinstance(rsis, list) or isinstance(rsis, tuple):
            for rsi in rsis:
                self._calc_rsi(rsi)

    def _calc_sma(self, w):
        self.df[f'SMA_{w}'] = self.df['close'].rolling(w).mean()

    def calculate_smas(self, smas):
        if isinstance(smas, int):
            self._calc_sma(smas)
        elif isinstance(smas, list) or isinstance(smas, tuple):
            for sma in smas:
                self._calc_sma(sma)

    def _calc_ema(self, w):
        self.df[f'EMA_{w}'] = self.df['close'].ewm(span=w, adjust=False).mean()

    def calculate_emas(self, emas):
        if isinstance(emas, int):
            self._calc_ema(emas)
        elif isinstance(emas, list) or isinstance(emas, tuple):
            for ema in emas:
                self._calc_ema(ema)

    def get_df(self, smas=None, emas=None, rsis=None, return_colors=False, obv=None, dataset=None):
        columns = ['time', 'min', 'max', 'open', 'close', 'volume']
        if dataset is None:
            self.df = pd.DataFrame(client.get_product_historic_rates(self.pair, granularity=self.granularity),
                                   columns=columns)[::-1]
        elif os.path.isfile(dataset):
            self.df = pd.read_csv(dataset, sep=',')

        self.df.index = self.df['time']  # .apply(datetime.fromtimestamp)
        self.df = self.df.drop('time', axis=1)

        self.calculate_smas(smas)
        self.calculate_emas(emas)
        self.calculate_rsis(rsis)
        if return_colors:
            self.calculate_colors()
        if obv:
            self.calculate_obv()

        return self.df

    def plot_asset(self):
        pass

    def __str__(self):
        state = client.get_product_ticker(product_id=self.pair)
        return '\n'.join([f'{k}: {v}' for k, v in state.items()])