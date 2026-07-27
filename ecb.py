import pkcs7
from aes import AES
from block_generator import BlockGenerator

class ECB:
    def __init__(self, key: bytes) -> None:
        self.cipher = AES(key)


    def encrypt(self, plaintext: bytes) -> bytes:
        ciphertext = []
        for block in BlockGenerator(plaintext, padding=True).blocks():
            ciphertext.append(self.cipher.encrypt(bytes(block)))
        return b''.join(ciphertext)


    def decrypt(self, ciphertext: bytes) -> bytes:
        plaintext = []
        for block in BlockGenerator(ciphertext, padding=False).blocks():
            plaintext.append(self.cipher.decrypt(bytes(block)))
        return pkcs7.unpad(b''.join(plaintext), BlockGenerator.BLOCKSIZE)

'''
fips_key = b'YELLOW SUBMARINE'
pt       = b'what the fuck'

cipher = ECB(fips_key)
ct = cipher.encrypt(pt)
print(ct)

pt2 = cipher.decrypt(ct)
print(pt2)
'''
