# Implement AES in CTR mode
from Cryptodome.Cipher import AES
from AES_in_ECB_mode import encryptAES_ECB
from struct import pack
from base64 import b64decode


def xor(string1, string2):
    assert len(string1) <= len(string2)
    xortext = bytearray()

    for byte in range(len(string1)):
        xortext += bytearray([string1[byte] ^ string2[byte]])

    return xortext


def cryptAES_CTR(key, nonce, plaintext):
    counter = 0
    nonce = bytearray(pack('<Q', nonce))
    ciphertext = bytearray()

    for n in range(0, len(plaintext), AES.block_size):
        cipher = encryptAES_ECB(nonce + bytearray(pack('<Q', counter)), key)
        ciphertext += xor(plaintext[n:n+AES.block_size], cipher)
        counter += 1

    return ciphertext


if __name__ == "__main__":
    ciphertext = b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")
    key = bytearray("YELLOW SUBMARINE", 'utf-8')
    plaintext = cryptAES_CTR(key, 0, ciphertext)
    print(plaintext)
    print(cryptAES_CTR(key, 0, plaintext) == ciphertext)
