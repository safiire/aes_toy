from keys import Keys
from galois_types import GF28
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
        return as_galois.reshape(self.DIMENSION, self.DIMENSION)

'''
fips_key = b'\x2b\x7e\x15\x16\x28\xae\xd2\xa6\xab\xf7\x15\x88\x09\xcf\x4f\x3c'
pt       = b'\x32\x43\xf6\xa8\x88\x5a\x30\x8d\x31\x31\x98\xa2\xe0\x37\x07\x34'
print(list(map(lambda b: f'{b:02x}', list(pt))))

cipher = AES(fips_key)
ct = cipher.encrypt(pt)
print(list(map(lambda b: f'{b:02x}', list(ct))))

pt2 = cipher.decrypt(ct)
print(list(map(lambda b: f'{b:02x}', list(pt2))))

assert(pt == pt2)
'''
