from datetime import datetime

import pandas as pd
from .client import client


class Asset:
    def __init__(self, crypto, fiat):
        self.pair = '-'.join((crypto, fiat))
        self.df = None

    def calc_sma(self, w):
        self.df[f'SMA_{w}'] = self.df['close'].rolling(w).mean().shift(-(w - 1))

    def calculate_smas(self, smas):
        if isinstance(smas, int):
            self.calc_sma(smas)
        elif isinstance(smas, list) or isinstance(smas, tuple):
            for sma in smas:
                self.calc_sma(sma)

    def calc_ema(self, w):
        self.df[f'EMA_{w}'] = self.df['close'][::-1].ewm(span=w, adjust=False).mean()[::-1]

    def calculate_emas(self, emas):
        if isinstance(emas, int):
            self.calc_ema(emas)
        elif isinstance(emas, list) or isinstance(emas, tuple):
            for ema in emas:
                self.calc_ema(ema)

    def get_df(self, granularity=300, smas=None, emas=None):
        columns = ['time', 'min', 'max', 'open', 'close', 'volume']
        self.df = pd.DataFrame(client.get_product_historic_rates(self.pair, granularity=granularity),
                               columns=columns)
        self.df.index = self.df['time'].apply(datetime.fromtimestamp)
        self.df = self.df.drop('time', axis=1)

        self.calculate_smas(smas)
        self.calculate_emas(emas)

        return self.df

    def plot_asset(self):
        pass

    def __str__(self):
        state = client.get_product_ticker(product_id=self.pair)
        return '\n'.join([f'{k}: {v}' for k, v in state.items()])