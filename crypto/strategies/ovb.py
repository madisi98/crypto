from .core import Strategy
from ..client import client


class OVB(Strategy):
    def buy(self):
        price = float(client.get_product_ticker(product_id='BTC-EUR')['price'])
        last_ema12 = self.asset.get_df(emas=12)['EMA_12'][0]
        return price < last_ema12

    def sell(self):
        price = float(client.get_product_ticker(product_id='BTC-EUR')['price'])
        last_ema12 = self.asset.get_df(emas=12)['EMA_12'][0]
        return price > last_ema12
