import time


class Strategy:
    def __init__(self, wallet, asset):
        self.wallet = wallet
        self.asset = asset

    def execute_strategy(self):
        try:
            while True:
                self.loop()
        except KeyboardInterrupt:
            print('Finished trading.')
            print('The state your wallet is:')
            print(self.wallet)

    def loop(self):
        while not self.buy():
            time.sleep(1)
        self.wallet.buy('BTC', 'EUR', 1)
        print(self.wallet.last_movement['BUY'])
        while not self.sell():
            time.sleep(1)
        self.wallet.sell('BTC', 'EUR', 1)
        print(self.wallet.last_movement['SELL'])
        print()

    def buy(self):
        raise(NotImplementedError, 'This strategy does not have a buy method implemented')

    def sell(self):
        raise(NotImplementedError, 'This strategy does not have a sell method implemented')
