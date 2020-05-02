import time

from .core import Strategy
from ..client import client


class EMA12(Strategy):
    def __init__(self, wallet, asset, ticks):
        super().__init__(wallet, asset)
        self.ticks = int(ticks)

    def buy(self):
        price = float(client.get_product_ticker(product_id=self.asset.pair)['price'])
        last_ema12 = self.asset.get_df(emas=12)['EMA_12'][0]
        return price < last_ema12

    def sell(self):
        price = float(client.get_product_ticker(product_id=self.asset.pair)['price'])
        last_ema12 = self.asset.get_df(emas=12)['EMA_12'][0]
        return price > last_ema12

    def loop(self):
        for i in range(self.ticks):
            while not self.buy():
                time.sleep(1)
        self.wallet.buy('BTC', 'EUR', 1)
        print(self.wallet.last_movement['BUY'])
        for i in range(self.ticks):
            while not self.sell():
                time.sleep(1)
        self.wallet.sell('BTC', 'EUR', 1)
        print(self.wallet.last_movement['SELL'])
        print()