import os

import cbpro

from .config import data_dir

public_client = cbpro.PublicClient()
movements_file_header = 'kind;price;origin;ori_amount;destiny;dest_amount\n'


class Wallet:
    def __init__(self, name):
        self.assets = {
            'EUR': 1000.,
            'USD': 0.,
            'BTC': 0.,
            'ETH': 0.,
        }
        self.last_movement = {}
        self.file = os.path.join(data_dir, name)
        with open(self.file, 'w') as f:
            f.write(movements_file_header)

    def buy(self, destiny, origin, amount):
        # Purchasing destiny with origin
        # Amount is a portion of origin in wallet
        assert 0 < amount <= 1
        assert self.assets[origin] > 0
        price = float(public_client.get_product_ticker(product_id='-'.join((destiny, origin)))['price'])
        ori_amount = self.assets[origin] * amount
        dest_amount = ori_amount / price
        self.assets[origin] -= ori_amount
        self.assets[destiny] += dest_amount
        self.log_last_movement('BUY', price, origin, ori_amount, destiny, dest_amount)

    def sell(self, origin, destiny, amount):
        # Selling destiny with origin
        # Amount is a portion of origin in wallet
        assert 0 < amount <= 1
        assert self.assets[origin] > 0
        price = float(public_client.get_product_ticker(product_id='-'.join((origin, destiny)))['price'])
        ori_amount = self.assets[origin] * amount
        dest_amount = ori_amount * price
        self.assets[origin] -= ori_amount
        self.assets[destiny] += dest_amount
        self.log_last_movement('SELL', price, origin, ori_amount, destiny, dest_amount)

    def log_last_movement(self, kind, price, origin, ori_amount, destiny, dest_amount):
        self.last_movement[kind] = {
            'price': price,
            'origin': origin,
            'amount': ori_amount,
            'destiny': destiny,
            'dest_amount': dest_amount
        }

        with open(self.file, 'a') as f:
            f.write(f'{kind};{price};{origin};{ori_amount};{destiny};{dest_amount}\n')

    def __str__(self):
        return '\n'.join([f'{k}: {v}' for k, v in self.assets.items()])

    def __repr__(self):
        return self.__str__()