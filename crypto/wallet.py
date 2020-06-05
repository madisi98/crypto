import os
from datetime import datetime

import pickle as pkl

from .config import wallet_dir
from .client import client
movements_file_header = 'kind;price;origin;ori_amount;destiny;dest_amount\n'


class Wallet:
    def __init__(self, name):
        self.assets = {
            'EUR': 100.,
            'USD': 0.,
            'BTC': 0.,
            'ETH': 0.,
            'ZRX': 0.,
        }
        self.last_movement = {}
        self.file_state = os.path.join(wallet_dir, name) + '.pkl'
        self.file_movements = os.path.join(wallet_dir, name) + '.csv'
        with open(self.file_movements, 'w') as f:
            f.write(movements_file_header)

    def buy(self, pair, amount, timestamp, price=None):
        # Purchasing destiny with origin
        # Amount is a portion of origin in wallet
        destiny, origin = pair.split('-')
        assert 0 < amount <= 1
        assert self.assets[origin] > 0
        if price is None:
            price = float(client.get_product_ticker(product_id='-'.join((destiny, origin)))['price'])
        ori_amount = self.assets[origin] * amount
        dest_amount = ori_amount * 0.995 / price  # Coinbase pro fees factored in
        self.assets[origin] -= ori_amount
        self.assets[destiny] += dest_amount
        self.log_last_movement('BUY', price, origin, ori_amount, destiny, dest_amount, timestamp)

    def sell(self, pair, amount, timestamp, price=None):
        # Selling destiny with origin
        # Amount is a portion of origin in wallet
        origin, destiny = pair.split('-')
        assert 0 < amount <= 1
        assert self.assets[origin] > 0
        if price is None:
            price = float(client.get_product_ticker(product_id='-'.join((origin, destiny)))['price'])
        ori_amount = self.assets[origin] * amount
        dest_amount = ori_amount * price * 0.995
        self.assets[origin] -= ori_amount
        self.assets[destiny] += dest_amount
        self.log_last_movement('SELL', price, origin, ori_amount, destiny, dest_amount, timestamp)

    def log_last_movement(self, kind, price, origin, ori_amount, destiny, dest_amount, timestamp):
        self.last_movement[kind] = {
            'price': round(price, 4),
            'origin': origin,
            'amount': round(ori_amount, 4),
            'destiny': destiny,
            'dest_amount': round(dest_amount, 4),
            'time': datetime.fromtimestamp(timestamp).isoformat()
        }

        with open(self.file_movements, 'a') as f:
            f.write(f'{kind};{price};{origin};{ori_amount};{destiny};{dest_amount};{timestamp}\n')

        print(f'{kind}:', self.last_movement[kind])

    def save(self):
        pkl.dump(self, open(self.file_state, 'wb'))

    def __str__(self):
        return '\n'.join([f'{k}: {v}' for k, v in self.assets.items()])

    def __repr__(self):
        return self.__str__()