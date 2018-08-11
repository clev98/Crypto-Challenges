#Basic demonstration of a Padding Oracle Attack
from Cryptodome.Cipher import AES
from base64 import b64decode
from os import urandom
from AES_in_ECB_mode import encryptAES_ECB
from Detect_AES_in_ECB_mode import detectECB
from Implement_PKCS7_Padding import addPKCS7Padding, removePKCS7Padding

RandomAESKey = urandom(AES.block_size)
unknownText = bytearray(b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"))


def oracle(knownText):
    return encryptAES_ECB(addPKCS7Padding(knownText+unknownText, AES.block_size), RandomAESKey)


def byteAtATime():
    roundedStringSize = len(oracle(bytearray()))

    unknownString = bytearray()

    for i in range(roundedStringSize - 1, 0, -1):
        addString = bytearray("A"*i, 'utf-8')
        tmpString1 = oracle(addString)[:roundedStringSize]

        for j in range(256):
            tmpString2 = oracle(addString+unknownString+chr(j).encode('utf-8'))[:roundedStringSize]

            if tmpString1 == tmpString2:
                unknownString += chr(j).encode('utf-8')
                break

    return removePKCS7Padding(unknownString)


if __name__ == "__main__":
    if detectECB(bytes(oracle(bytearray("YELLOW SUBMARINEYELLOW SUBMARINE", 'utf-8'))), AES.block_size):
        print(byteAtATime().decode('utf-8'))
