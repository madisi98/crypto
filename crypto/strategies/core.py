import time
from datetime import datetime


class Strategy:
    def __init__(self, wallet, asset, backtesting=False, simulator=None):
        if backtesting:
            assert simulator is not None

        self.info = None
        self.date = None
        self.wallet = wallet
        self.asset = asset
        self.simulator = simulator
        self.backtesting = backtesting

    def execute_strategy(self):
        try:
            while True:
                self.loop()
        except KeyboardInterrupt:
            print('Finished trading.')
            print('The state your wallet is:')
            print(self.wallet)
            print('Saving wallet...')
            self.wallet.save()

    def update_date(self, date):
        date = datetime.fromtimestamp(date)
        date = str(date)[:7]
        if date != self.date:
            print(date)
            self.date = date
            self.wallet.assets[self.asset.fiat] += 100

    def has_fiat(self):
        return self.wallet.assets[self.asset.fiat] > 0

    def has_crypto(self):
        return self.wallet.assets[self.asset.crypto] > 0

    def never_lose(self):
        return self.info['price'] > self.wallet.last_movement['BUY']['price']

    def stop_loss(self):
        return self.info['price'] < self.wallet.last_movement['BUY']['price'] * 0.9

    def exec_buy(self):
        if self.has_fiat():
            self.wallet.buy(self.asset.pair, 1, self.info['price'])
            print('BUY:', self.wallet.last_movement['BUY'])

    def exec_sell(self):
        if self.has_crypto(): #and self.never_lose():
            self.wallet.sell(self.asset.pair, 1, self.info['price'])
            print('SELL:', self.wallet.last_movement['SELL'])

    def update_relevant_info(self):
        if self.backtesting:
            return self._update_relevant_info_backtesting()
        else:
            return self._update_relevant_info_real_time()

    def _update_relevant_info_backtesting(self):
        self.info = next(self.simulator.simulation)
        self.info['price'] = self.info['close']
        self.update_date(self.info.name)

    def _update_relevant_info_real_time(self):
        raise(NotImplementedError, 'This strategy does not have a _get_relevant_info_real_time method implemented')