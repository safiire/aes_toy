import numpy as np
from galois_types import GF2, GF28


C     = GF28(0b01100011).vector()
C_INV = GF28(0b00000101).vector()


INVERSE_EXPONENT = 254


SBOX = GF2([
    [1, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1, 1]
])


INV_SBOX = GF2([
    [0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0]
])


MIX_COLUMN_T = GF28([
    [ 0x2, 0x3, 0x1, 0x1 ],
    [ 0x1, 0x2, 0x3, 0x1 ],
    [ 0x1, 0x1, 0x2, 0x3 ],
    [ 0x3, 0x1, 0x1, 0x2 ]
]).T


INV_MIX_COLUMN_T = GF28([
    [ 0xe, 0xb, 0xd, 0x9 ],
    [ 0x9, 0xe, 0xb, 0xd ],
    [ 0xd, 0x9, 0xe, 0xb ],
    [ 0xb, 0xd, 0x9, 0xe ]
]).T


def sub_bytes(elements):
    inverse_elements = elements**INVERSE_EXPONENT
    bit_vectors = inverse_elements.vector() @ SBOX + C
    return GF28.Vector(bit_vectors)


def inv_sub_bytes(elements):
    bit_vectors = elements.vector()
    inverse_bit_vectors = bit_vectors @ INV_SBOX + C_INV
    return GF28.Vector(inverse_bit_vectors)**INVERSE_EXPONENT


def mix_columns(state):
    return state @ MIX_COLUMN_T


def inv_mix_columns(state):
    return state @ INV_MIX_COLUMN_T


def shift_rows(original_state):
    state = original_state.copy().T
    for i in range(len(state)):
        state[i] = np.roll(state[i], -i)
    return state.T


def inv_shift_rows(original_state):
    state = original_state.copy().T
    for i in range(len(state)):
        state[i] = np.roll(state[i], i)
    return state.T
