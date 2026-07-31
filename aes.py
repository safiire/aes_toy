from keys import Keys
from typing import cast
from galois_types import GF28, Matrix, Vector
from transforms import sub_bytes, shift_rows, mix_columns
from transforms import inv_sub_bytes, inv_shift_rows, inv_mix_columns


class AES:
    DIMENSION = 4

    def __init__(self, key: bytes) -> None:
        self.keys = Keys.from_bytes(key)


    def encrypt(self, block: bytes) -> bytes:
        state  = self.state_from_block(block)
        state += self.keys.user_key

        for round_key in self.keys.round_keys:
            state  = sub_bytes(state)
            state  = shift_rows(state)
            state  = mix_columns(state)
            state += round_key

        state  = sub_bytes(state)
        state  = shift_rows(state)
        state += self.keys.last_key
        return bytes(state)


    def decrypt(self, block: bytes) -> bytes:
        state  = self.state_from_block(block)
        state += self.keys.last_key

        for round_key in reversed(self.keys.round_keys):
            state  = inv_shift_rows(state)
            state  = inv_sub_bytes(state)
            state += round_key
            state  = inv_mix_columns(state)

        state  = inv_shift_rows(state)
        state  = inv_sub_bytes(state)
        state += self.keys.user_key
        return bytes(state)


    def state_from_block(self, block: bytes) -> Matrix:
        blocksize = self.DIMENSION**2
        if len(block) != blocksize:
            raise ValueError(f'Block size must be {blocksize}')

        as_galois = GF28(list(block))
        return cast(Matrix, as_galois.reshape(self.DIMENSION, self.DIMENSION))
