import cbpro

from .core import Strategy

public_client = cbpro.PublicClient()


class OVB(Strategy):
    def buy(self):
        price = float(public_client.get_product_ticker(product_id='BTC-EUR')['price'])
        last_ema12 = self.asset.get_df(emas=12)['EMA_12'][0]
        return price < last_ema12

    def sell(self):
        price = float(public_client.get_product_ticker(product_id='BTC-EUR')['price'])
        last_ema12 = self.asset.get_df(emas=12)['EMA_12'][0]
        return price > last_ema12
