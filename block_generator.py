import pkcs7

class Block:
    def __init__(self, data: bytes) -> None:
        self.data = data

    def __bytes__(self) -> bytes:
        return self.data

    def __len__(self) -> int:
        return len(self.data)

    def __xor__(self, other):
        ret = bytes(x ^ y for x, y in zip(self.data, other.data))
        return self.__class__(ret)

    def __repr__(self):
        return f'Block: {self.data}'


class BlockGenerator:
    BLOCKSIZE = 16

    class BlockError(Exception):
        pass


    def __init__(self, data: bytes, padding=False):
        if padding:
            self.data = pkcs7.pad(data, self.BLOCKSIZE)
        else:
            if len(data) % self.BLOCKSIZE != 0:
                raise self.BlockError(f'Bad blocksize {len(data)}')
            self.data = data


    def blocks(self):
        range_iter = range(0, len(self.data), self.BLOCKSIZE)
        block = lambda i: Block(self.data[i:i + self.BLOCKSIZE])
        yield from (block(i) for i in range_iter)
