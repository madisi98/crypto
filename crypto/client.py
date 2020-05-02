import os

import cbpro

from .config import secrets_path

client = cbpro.PublicClient()
if os.path.isfile(os.path.join(secrets_path, 'secrets.pkl')):
    try:
        from .secrets import secrets
        client = cbpro.AuthenticatedClient(
            key=secrets['key'],
            b64secret=secrets['b64secret'],
            passphrase=secrets['passphrase']
        )
        print(f'Succesfully authenticated client. Continuing as {secrets["key"]}')

    except ValueError:
        print('Wrong password. Continuing with Public Client...')
    except TypeError:
        print('Password needed for authentication. Continuing with Public Client...')
else:
    print('Continuing with Public Client...')