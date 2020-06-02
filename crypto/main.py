import os
import argparse
import traceback

import pickle as pkl

from .config import data_dir, wallet_dir
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
    parser.add_argument('--wallet', help='Wallet name')
    parser.add_argument('--asset', help='Crypto to trade')
    parser.add_argument('--strategy', help='Strategy to use')
    parser.add_argument('--granularity', type=int, default=300, help='Granularity in seconds for periods')
    parser.add_argument('--params', help='Strategy modifier')
    parser.add_argument('--real_wallet', default=False, action="store_true")
    args = parser.parse_args()

    os.makedirs(data_dir, exist_ok=True)

    if not args.real_wallet:
        wallet_file = os.path.join(wallet_dir, args.wallet + '.pkl')
        if os.path.isfile(wallet_file):
            wallet = pkl.load(open(wallet_file, 'rb'))
        else:
            wallet = Wallet(args.wallet)
    else:
        # Instanciate Real wallet
        raise NotImplementedError('Real wallets not implemented yet.')
    asset = Asset(args.asset, 'EUR', args.granularity)
    print(f'Trading in {asset.pair} pair')
    print(f'Created a new wallet:')
    print(wallet)

    if args.params:
        strategy = strategies_dict[args.strategy](wallet, asset, *args.params.split('|'))
    else:
        strategy = strategies_dict[args.strategy](wallet, asset)
    try:
        strategy.execute_strategy()
    except:
        print(wallet)
        print('An exception occurred. Saving wallet state before exitting... ')
        wallet.save()
        traceback.print_exc()

    print(f'Exiting crypto.')
