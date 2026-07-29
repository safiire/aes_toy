#!/usr/bin/env python

import argparse
from ecb import ECB
from cbc import CBC
from hashlib import pbkdf2_hmac
from base64 import b64encode, b64decode
from json import dumps, loads


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='AES Decrypt')
    parser.add_argument('password', help='Password')
    parser.add_argument('in_file', help='Path to input file')
    parser.add_argument('out_file', help='Path to output file')
    return parser.parse_args()


def create_key(password: str, salt: bytes) -> bytes:
    block_size = 16
    iterations = 600_000
    return pbkdf2_hmac('sha256', password.encode(), salt, iterations, dklen=block_size)


if __name__ == '__main__':
    args = parse()

    with open(args.in_file, 'r') as fp:
        input_data = loads(fp.read())

    salt = b64decode(input_data['salt'])
    ct = b64decode(input_data['ciphertext'])

    key = create_key(args.password, salt)

    if input_data['mode'] == 'ecb':
        cipher = ECB(key)
        pt = cipher.decrypt(ct)

    elif input_data['mode'] == 'cbc':
        iv = b64decode(input_data['iv'])
        cipher = CBC(key, iv)
        pt = cipher.decrypt(ct)

    with open(args.out_file, 'wb') as fp:
        fp.write(pt)
