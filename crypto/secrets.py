import os
import getpass

import pickle as pkl
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

from .config import secrets_path


def load_key_and_decrypt():
    with open(os.path.join(secrets_path, 'private_key.pem'), 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=getpass.getpass('Password for decrypting private key: ').encode(),
            backend=default_backend()
        )
    encrypted = pkl.load(open(os.path.join(secrets_path, 'secrets.pkl'), 'rb'))
    decrypted = {key: private_key.decrypt(
        value,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA512()),
            algorithm=hashes.SHA512(),
            label=None
        )
    ).decode() for key, value in encrypted.items()}
    return decrypted


secrets = load_key_and_decrypt()
