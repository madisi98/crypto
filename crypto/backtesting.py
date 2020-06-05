import os
import argparse
import traceback

from .config import data_dir
from .strategies import one, ema12, ema12_reversed, ovb, rsi
from .wallet import Wallet
from .asset import Asset
from .simulator import Simulator

strategies_dict = {
    'ema12': ema12.EMA12,
    'ema12_reversed': ema12_reversed.EMA12Reversed,
    'one': one.One,
    'ovb': ovb.OVB,
    'rsi': rsi.RSI
}


def main():
    print(f'BACKTESTING CRYPTO')
    parser = argparse.ArgumentParser()
    parser.add_argument('--asset', help='Crypto to trade')
    parser.add_argument('--strategy', help='Strategy to use')
    parser.add_argument('--params', help='Strategy modifier')
    parser.add_argument('--dataset_sim', help='Dataset for simulation')
    parser.add_argument('--dataset_stats', help='Dataset for getting averages and such')
    args = parser.parse_args()

    os.makedirs(data_dir, exist_ok=True)

    wallet_name = 'BACKTESTING'
    wallet = Wallet(wallet_name)
    asset = Asset(args.asset, 'EUR')
    asset.get_df(smas=(50, 100, 200), emas=(12, 26), rsis=14, return_colors=True, dataset=args.dataset_stats)
    simulator = Simulator(args.dataset_stats, asset.pair)
    print(f'BACKTESTING in {asset.pair} pair')
    print(f'Created a new wallet:')
    print(wallet)

    if args.params:
        strategy = strategies_dict[args.strategy](wallet, asset, True, simulator, *args.params.split('|'))
    else:
        strategy = strategies_dict[args.strategy](wallet, asset, True, simulator)

    try:
        strategy.execute_strategy()
    except StopIteration:
        if wallet.assets[asset.crypto]:
            wallet.sell(asset.pair, 1, strategy.info.name)
        print(wallet)
        print('Finished backtesting')
    except:
        print(wallet)
        print('An exception occurred. Saving wallet state before exitting... ')
        wallet.save()
        traceback.print_exc()

    print(f'Exiting crypto.')
