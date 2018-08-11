#CBC Padding Oracle Attack demonstration
from Implement_CBC_mode import encryptAES_ECB_CBC, decryptAES_ECB_CBC
from PKCS7_Padding_Validation import testPadding
from os import urandom
from random import randint
from Cryptodome.Cipher import AES
from base64 import b64decode


randomAESKey = urandom(AES.block_size)


def CBCOracle():
    iv = urandom(AES.block_size)
    stringTuple = ("MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
                   "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
                   "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
                   "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
                   "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
                   "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
                   "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
                   "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
                   "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
                   "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93")
    plaintext = b64decode(stringTuple[randint(0, 9)])
    ciphertext = encryptAES_ECB_CBC(plaintext, randomAESKey, iv)
    return ciphertext, iv


def paddingOracle(ciphertext, iv):
    plaintext = decryptAES_ECB_CBC(ciphertext, randomAESKey, iv)

    try:
        testPadding(plaintext)
        return True
    except Exception:
        return False


def decipher(ciphertext, iv):
    ciphertext = iv + ciphertext
    plaintext = bytearray()
    blocks = []

    for n in range(1, len(ciphertext)//AES.block_size + 1):
        blocks.append(ciphertext[(n-1)*AES.block_size:n*AES.block_size])

    for block in range(len(blocks) - 1, 0, -1):
        next = bytearray()
        plaintextBlock = bytearray(AES.block_size)

        for char in range(1, AES.block_size + 1):
            for byte in range(256):
                cp = bytearray([0]*(AES.block_size - char)) + bytearray([byte]) + next

                if paddingOracle(blocks[block], cp):
                    plaintextBlock[AES.block_size - char] = char ^ byte ^ blocks[block - 1][AES.block_size - char]

                    for i in range(len(next)):
                        next[i] ^= char ^ (char + 1)

                    next = bytearray([(char + 1) ^ char ^ byte]) + next
                    break
            else:
                raise Exception("No padding found!")
        plaintext = plaintextBlock + plaintext
    return plaintext


if __name__ == "__main__":
    ciphertext, iv = CBCOracle()
    plaintext = decipher(ciphertext, iv)
    print(plaintext)
