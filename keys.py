import numpy as np
from typing import Self
from transforms import sub_bytes
from galois_types import GF28, Matrix, Vector


class Keys:
    DIMENSION = 4

    @classmethod
    def from_bytes(cls, key_bytes: bytes, num_rounds:int=10) -> Self:
        return cls(GF28(list(key_bytes)), num_rounds=num_rounds)


    def __init__(self, key: Vector, num_rounds:int=10) -> None:
        if len(key) != 16:
            raise ValueError('Key must be 128 bits')

        self.user_key = key.reshape(self.DIMENSION, self.DIMENSION)
        self.round_constants = self.build_round_constants(num_rounds)
        self.round_keys = self.key_expansion(self.user_key, num_rounds)


    def build_round_constants(self, num_rounds: int) -> Matrix:
        one, two = GF28([1, 2])
        constants = GF28.Zeros((num_rounds, self.DIMENSION))
        constants[0][0] = one

        for j in range(1, num_rounds):
            constants[j][0] = constants[j - 1][0] * two
        return constants


    def key_expansion(self, user_key: Matrix, num_rounds: int) -> Matrix:
        keys = GF28.Zeros((num_rounds, self.DIMENSION, self.DIMENSION))
        prev_key = user_key

        for round in range(num_rounds):
            w0, w1, w2, w3 = prev_key

            w4 = self.transform(w3, round) + w0
            w5 = w1 + w4
            w6 = w2 + w5
            w7 = w3 + w6

            keys[round] = GF28([w4, w5, w6, w7])
            prev_key = keys[round]

        self.last_key = keys[-1]
        return keys[0:-1]


    def transform(self, v0: Vector, round: int) -> Vector:
        v1 = np.roll(v0, -1)
        v2 = sub_bytes(v1)
        return v2 + self.round_constants[round]
