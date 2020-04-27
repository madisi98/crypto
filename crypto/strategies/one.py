import cbpro

from .core import Strategy

public_client = cbpro.PublicClient()


class One(Strategy):
    def buy(self):
        if 'SELL' not in self.wallet.last_movement:
            return True
        price = float(public_client.get_product_ticker(product_id=self.asset.pair)['price'])
        sell_price = self.wallet.last_movement['BUY']['price']
        return price < sell_price

    def sell(self):
        price = float(public_client.get_product_ticker(product_id=self.asset.pair)['price'])
        buy_price = self.wallet.last_movement['BUY']['price']
        return price > buy_price
