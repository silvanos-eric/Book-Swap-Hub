import os
import secrets


def generate_secret_key(filepath='secret_key.txt'):
    if not os.path.exists(filepath):
        # Generate a new secret key and store it in the file
        secret_key = secrets.token_hex(32)
        with open(filepath, 'w') as f:
            f.write(secret_key)
    else:
        # Load the secret key from the file
        with open(filepath, 'r') as f:
            secret_key = f.read().strip()

    return secret_key
