import pandas as pd

from .core import Strategy
from ..client import client


class EMA12(Strategy):
    def __init__(self, wallet, asset, backtesting=False, simulator=None):
        super().__init__(wallet, asset, backtesting, simulator)
        self.buy_margin = 0.985  # Magic numbers
        self.sell_margin = 1.05
        # self.buy_margin = 0.985
        # self.sell_margin = 1.15

    def _update_relevant_info_real_time(self):
        self.info = self.asset.get_df(emas=12).iloc[-1]
        self.info['price'] = float(client.get_product_ticker(product_id=self.asset.pair)['price'])
        print(self.info)

    def sell(self):
        try:
            info = self.get_relevant_info()
            sell = info['price'] > info['last_ema12'] * self.sell_margin
            # stop_loss = self.simulator.price[0] < self.simulator.price[-1] * 0.9
            stop_loss = info['price'] < 0.65 * self.wallet.last_movement['BUY']['price']
            never_lose = info['price'] > self.sell_margin * self.wallet.last_movement['BUY']['price']
            if stop_loss:
                print(self.simulator.price)
                print('Stopping loss')
            return (sell and never_lose) or stop_loss
        except:
            return False

    def loop(self):
        self.update_relevant_info()
        if self.info['price'] < self.info['EMA_12'] * self.buy_margin:
            self.exec_buy()

        elif self.info['price'] > self.info['EMA_12'] * self.sell_margin:
            self.exec_sell()

    # def loop(self, skip_buy=False):
    #     if not skip_buy:
    #         while not self.buy():
    #             time.sleep(1)
    #         # TODO: Adjust Buy
    #         self.wallet.buy(self.asset.pair, 1)
    #         print('BUY:', self.wallet.last_movement['BUY'])
    #     while not self.sell():
    #         time.sleep(1)
    #     # TODO: Adjust Sell
    #     self.wallet.sell(self.asset.pair, 1)
    #     print('SELL:', self.wallet.last_movement['SELL'])
    #     print()
