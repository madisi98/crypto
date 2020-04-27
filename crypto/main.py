import argparse

from .strategies import one, ema12, ema12_reversed, ovb
from .wallet import Wallet
from .asset import Asset

strategies_dict = {
    'ema12': ema12.EMA12,
    'ema12_reversed': ema12_reversed.EMA12Reversed,
    'one': one.One,
    'ovb': ovb.OVB
}


def main():
    print(f'EXECUTING CRYPTO')
    parser = argparse.ArgumentParser()
    parser.add_argument("--wallet", help="Wallet name")
    parser.add_argument("--asset", help="Crypto to trade")
    parser.add_argument("--strategy", help="Strategy to use")
    parser.add_argument("--param", help="Strategy modifier")
    args = parser.parse_args()

    wallet = Wallet(args.wallet)
    asset = Asset(args.asset, 'EUR')
    print(f'Trading in {asset.pair} pair')
    print(f'Created a new wallet:')
    print(wallet)

    if args.param:
        strategy = strategies_dict[args.strategy](wallet, asset, args.param)
    else:
        strategy = strategies_dict[args.strategy](wallet, asset)
    strategy.execute_strategy()

    print(f'Exiting crypto.')
