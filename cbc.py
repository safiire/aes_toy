import pkcs7
from aes import AES
from block_generator import BlockGenerator, Block

class CBC:
    def __init__(self, key: bytes, iv: bytes) -> None:
        self.iv = Block(iv)
        self.cipher = AES(key)

    def encrypt(self, plaintext: bytes) -> bytes:
        ciphertext = []
        prev_block = self.iv

        for block in BlockGenerator(plaintext, padding=True).blocks():
            ct = self.cipher.encrypt(bytes(block ^ prev_block))
            ciphertext.append(ct)
            prev_block = Block(ct)
        return b''.join(ciphertext)


    def decrypt(self, ciphertext: bytes) -> bytes:
        plaintext = []
        prev_block = self.iv
        for block in BlockGenerator(ciphertext).blocks():
            decrypted = Block(self.cipher.decrypt(bytes(block))) ^ prev_block
            plaintext.append(bytes(decrypted))
            prev_block = block
        return pkcs7.unpad(b''.join(plaintext), BlockGenerator.BLOCKSIZE)
