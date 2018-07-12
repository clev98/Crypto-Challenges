from Crypto.Cipher import AES
from base64 import b64decode
from collections import defaultdict
from os import urandom

RandomAESKey = urandom(AES.block_size)
unknownText = bytearray(b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"))

def oracle(knownText):
    return encryptAES_ECB(addPKCS7Padding(knownText+unknownText, AES.block_size, "\x04".encode('utf-8')), RandomAESKey)

def byteAtATime(oracle):
    blockSize = findBlocksize(oracle)
    roundedStringSize = int((len(oracle(bytearray()))/blockSize + 1)*blockSize)
    unknownString = bytearray()

    for i in range(roundedStringSize - 1, 0, -1):
        addString = bytearray("A"*i, 'utf-8')
        tmpString1 = oracle(addString)[:roundedStringSize]

        for j in range(256):
            tmpString2 = oracle(addString+unknownString+chr(j).encode('utf-8'))[:roundedStringSize]
            
            if tmpString1 == tmpString2:
                unknownString += chr(j).encode('utf-8')
                break
    return removePKCS7Padding(unknownString, "\x04".encode('utf-8'))

def findBlocksize(oracle):
    unknownTextLength = len(oracle(bytearray()))
    i = 1

    while True:
        newTextLength = len(oracle(bytearray("A" * i, 'utf-8')))
        
        if newTextLength - unknownTextLength:
            return newTextLength - unknownTextLength
        i += 1

def detectECB(ciphertext, blocksize): 
    repeats = defaultdict(lambda: -1)
            
    for n in range(0, len(ciphertext), blocksize):
        repeats[ciphertext[n:n+blocksize]] += 1

    return sum(repeats.values()) > 0

def encryptAES_ECB(plaintext, key):
    return bytearray(AES.new(key, AES.MODE_ECB).encrypt(plaintext))

def addPKCS7Padding(text, blockSize, paddingChar):
    if len(text) % blockSize:
        neededPadding = blockSize - (len(text) % blockSize)
        
        for n in range(neededPadding):
            text += paddingChar
            
    return text

def removePKCS7Padding(text, paddingChar):
    for n in range(len(text)-1, -1, -1):
        if text[n] == ord(paddingChar):
            text.remove(ord(paddingChar))
            
    return text

if __name__ == "__main__":
    if detectECB(bytes(oracle(bytearray("YELLOW SUBMARINEYELLOW SUBMARINE", 'utf-8'))), AES.block_size):
        print(byteAtATime(oracle).decode('utf-8'))
