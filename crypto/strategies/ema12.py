from .core import Strategy
from ..client import client


class EMA12(Strategy):
    def __init__(self, wallet, asset, backtesting=False, simulator=None):
        super().__init__(wallet, asset, backtesting, simulator)
        self.buy_margin = 0.985  # Magic numbers
        self.sell_margin = 1.05

    def _update_relevant_info_real_time(self):
        self.info = self.asset.get_df(emas=12).iloc[-1]
        self.info['price'] = float(client.get_product_ticker(product_id=self.asset.pair)['price'])

    def loop(self):
        self.update_relevant_info()
        if self.info['price'] < self.info['EMA_12'] * self.buy_margin:
            self.exec_buy()

        elif self.info['price'] > self.info['EMA_12'] * self.sell_margin:
            self.exec_sell()