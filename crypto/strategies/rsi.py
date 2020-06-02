from .core import Strategy
from ..client import client


class RSI(Strategy):
    def __init__(self, wallet, asset, backtesting=False, simulator=None):
        super().__init__(wallet, asset, backtesting, simulator)
        # self.buy_margin = 50 - int(margin)
        # self.sell_margin = 50 + int(margin)
        self.buy_margin = 50
        self.sell_margin = 80
        self.days_count = 0

    def _get_relevant_info_real_time(self):
        return {
            'price': float(client.get_product_ticker(product_id=self.asset.pair)['price']),
            'rsi_14': self.asset.get_df(rsis=14)['RSI_14'][-1]
        }

    def loop(self):
        self.update_relevant_info()
        if self.info['RSI_14'] < self.buy_margin:
            self.days_count = 0
            self.exec_buy()

        elif self.info['RSI_14'] >= self.sell_margin:
            self.days_count += 1
            if self.days_count == 4:
                self.days_count = 0
                self.exec_sell()

        else:
            self.days_count = 0
