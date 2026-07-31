#!/usr/bin/env python

import argparse
from ecb import ECB
from cbc import CBC
from hashlib import pbkdf2_hmac
from os import urandom
from base64 import b64encode, b64decode
from json import dumps


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='AES Encrypt')
    parser.add_argument('mode', choices=['ecb', 'cbc'], help='AES Mode')
    parser.add_argument('password', help='Password')
    parser.add_argument('in_file', help='Path to input file')
    parser.add_argument('out_file', help='Path to output file')
    return parser.parse_args()


def create_key(password: str) -> tuple[bytes, bytes]:
    block_size = 16
    iterations = 600_000
    salt = urandom(block_size)
    key = pbkdf2_hmac('sha256', password.encode(), salt, iterations, dklen=block_size)
    return (key, salt)


if __name__ == '__main__':
    args = parse()
    output = { 'mode': args.mode }

    with open(args.in_file, 'rb') as fp_in:
        input_data = fp_in.read()

    key, salt = create_key(args.password)
    output['salt'] = b64encode(salt).decode()

    if args.mode == 'ecb':
        ecb = ECB(key)
        ct = ecb.encrypt(input_data)

    elif args.mode == 'cbc':
        iv = urandom(16)
        output['iv'] = b64encode(iv).decode()
        cbc = CBC(key, iv)
        ct = cbc.encrypt(input_data)

    output['ciphertext'] = b64encode(ct).decode()

    with open(args.out_file, 'w') as fp_out:
        fp_out.write(dumps(output, indent=2))
