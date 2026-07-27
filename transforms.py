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


MIX_COLUMN = GF28([
    [ 0x2, 0x3, 0x1, 0x1 ],
    [ 0x1, 0x2, 0x3, 0x1 ],
    [ 0x1, 0x1, 0x2, 0x3 ],
    [ 0x3, 0x1, 0x1, 0x2 ]
])


INV_MIX_COLUMN = GF28([
    [ 0xe, 0xb, 0xd, 0x9 ],
    [ 0x9, 0xe, 0xb, 0xd ],
    [ 0xd, 0x9, 0xe, 0xb ],
    [ 0xb, 0xd, 0x9, 0xe ]
])


def sub_bytes(elements):
    inverse_elements = elements**INVERSE_EXPONENT
    bit_vectors = inverse_elements.vector() @ SBOX + C
    return GF28.Vector(bit_vectors)


def inv_sub_bytes(elements):
    bit_vectors = elements.vector()
    inverse_bit_vectors = bit_vectors @ INV_SBOX + C_INV
    return GF28.Vector(inverse_bit_vectors)**INVERSE_EXPONENT


def mix_columns(state):
    return (MIX_COLUMN @ state.T).T


def inv_mix_columns(state):
    return (INV_MIX_COLUMN @ state.T).T  # can I just transpose MIX_COLUMN instead?


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


'''
for n in range(256):
    g = GF28(n)
    s = sub_bytes(g)
    i = inv_sub_bytes(s)
    assert(g == i)

print('')

all_bytes = GF28(list(range(0x100)))
subbed = sub_bytes(all_bytes)
fixed = inv_sub_bytes(subbed)

for u in range(0x10):
    for l in range(0x10):
        index = (u << 4) + l
        b = subbed[index]
        i = int(b)
        print(f'{i:02x} ', end='')
    print('')
print('')

for u in range(0x10):
    for l in range(0x10):
        index = (u << 4) + l
        b = fixed[index]
        i = int(b)
        print(f'{i:02x} ', end='')
    print('')
'''
