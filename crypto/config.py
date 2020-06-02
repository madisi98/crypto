import os

data_dir = os.path.join(os.path.expanduser('~'), 'crypto_data')
secrets_path = os.path.join(data_dir, 'secrets')
wallet_dir = os.path.join(data_dir, 'wallets')

if not os.path.isdir(data_dir):
    os.makedirs(data_dir, exist_ok=True)
if not os.path.isdir(secrets_path):
    os.makedirs(secrets_path, exist_ok=True)
if not os.path.isdir(wallet_dir):
    os.makedirs(wallet_dir, exist_ok=True)

tracking_assets = ['BTC', 'ETH']
