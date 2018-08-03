from Cryptodome.Cipher import AES
from base64 import b64decode
from os import urandom
from random import randint
from Set1.AES_in_ECB_mode import encryptAES_ECB
from Implement_PKCS7_Padding import addPKCS7Padding, removePKCS7Padding

RandomAESKey = urandom(AES.block_size)
unknownText = bytearray(b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"))
randomPrefix = urandom(randint(0, 256))


def oracle(knownText):
    return encryptAES_ECB(addPKCS7Padding(randomPrefix+knownText+unknownText, AES.block_size), RandomAESKey)


def byteAtATime():
    blockSize = findBlocksize()
    prefixPadding, prefixRoundedSize = findPrefixLength(blockSize)
    roundedStringSize = len(oracle(bytearray())) - prefixRoundedSize
    unknownString = bytearray()

    for i in range(roundedStringSize - 1, 0, -1):
        addString = bytearray("A"*(i + prefixPadding), 'utf-8')
        tmpString1 = oracle(addString)[prefixRoundedSize:roundedStringSize+prefixRoundedSize]

        for j in range(256):
            tmpString2 = oracle(addString+unknownString+chr(j).encode('utf-8'))[prefixRoundedSize:roundedStringSize+prefixRoundedSize]

            if tmpString1 == tmpString2:
                unknownString += chr(j).encode('utf-8')
                break

    return removePKCS7Padding(unknownString, blockSize)


def findPrefixLength(blocksize):
    for i in range(blocksize):
        prefix = bytearray("A"*i, "utf-8")
        ciphertext = oracle(prefix+bytearray(("YELLOW SUBMARINE"*5), "utf-8"))
        lastBlock = count = None

        for n in range(0, len(ciphertext), blocksize):
            currentBlock = ciphertext[n : n+blocksize]

            if currentBlock == lastBlock:
                count += 1
            else:
                lastBlock = currentBlock
                count = 1

            if count == 5:
                return i, n-4*blocksize


def findBlocksize():
    unknownTextLength = len(oracle(bytearray()))
    i = 1

    while True:
        newTextLength = len(oracle(bytearray("A" * i, 'utf-8')))

        if newTextLength - unknownTextLength:
            return newTextLength - unknownTextLength
        i += 1


if __name__ == "__main__":
    print(byteAtATime().decode('utf-8'))
