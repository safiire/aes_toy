class PKCS7Error(Exception):
    pass


def pad(data: bytes, block_size: int) -> bytes:
    if block_size < 1 or block_size > 255:
        raise PKCS7Error(f'Blocksize {block_size}: 1 > block size < 255')
    data_length = len(data)
    padding_needed = block_size - data_length % block_size
    padding = [padding_needed] * padding_needed
    return data + bytes(padding)


def unpad(data: bytes, block_size: int) -> bytes:
    if len(data) % block_size != 0:
        raise PKCS7Error(f'Invalid Block Size')
    padding_size = data[-1]
    padding_bytes = data[-padding_size:]
    if not all(byte == padding_size for byte in padding_bytes):
        raise PKCS7Error(f'Invalid Padding bytes')
    return data[0:-padding_size]
