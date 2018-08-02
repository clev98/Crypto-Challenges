# CBC Bitflipping Attack Example
from Cryptodome.Cipher import AES
from os import urandom


randomAESKey = urandom(AES.block_size)
iv = urandom(AES.block_size)


def oracle(input):
    input = input.replace(";", '";"').replace("=", '"="')
    plaintext = "comment1=cooking%20MCs;userdata="+input+";comment2=%20like%20a%20pound%20of%20bacon"
    return encryptAES_ECB_CBC(plaintext.encode('utf-8'), randomAESKey, iv)


def isAdmin(ciphertext):
    plaintext = decryptAES_ECB_CBC(ciphertext, randomAESKey, iv)
    print(plaintext)
    return ";admin=true;".encode('utf-8') in plaintext


def crack():
    text = ("A"*AES.block_size) + "AadminAtrueA"
    ciphertext = oracle(text)

    ciphertext[32] ^= ord("A") ^ ord(";")
    ciphertext[32 + 6] ^= ord("A") ^ ord("=")
    ciphertext[32 + 11] ^= ord("A") ^ ord(";")

    print(isAdmin(ciphertext))


def addPKCS7Padding(text, blockSize):
    if len(text) % blockSize:
        neededPadding = blockSize - len(text) % blockSize
        text += bytearray((chr(neededPadding)*neededPadding), 'utf-8')

    return text


def removePKCS7Padding(text, blockSize):
    for n in range(len(text) - 1, len(text) - text[-1] - 1, -1):
        if text[n] != text[-1]:
            return text

    return text[:-text[-1]]


def decryptAES_ECB(ciphertext, key):
    return AES.new(key, AES.MODE_ECB).decrypt(ciphertext)


def decryptAES_ECB_CBC(ciphertext, key, iv):
    plaintext = bytearray(len(ciphertext))

    for n in range(0, len(ciphertext), AES.block_size):
        plaintext[n: n+AES.block_size] = xor(decryptAES_ECB(ciphertext[n: n+AES.block_size], key), iv)
        iv = ciphertext[n: n+AES.block_size]

    return removePKCS7Padding(plaintext, AES.block_size)


def encryptAES_ECB(plaintext, key):
    return AES.new(key, AES.MODE_ECB).encrypt(plaintext)


def encryptAES_ECB_CBC(plaintext, key, iv):
    plaintext = addPKCS7Padding(plaintext, AES.block_size)
    ciphertext = bytearray(len(plaintext))

    for n in range(0, len(plaintext), AES.block_size):
        ciphertext[n: n+AES.block_size] = encryptAES_ECB(xor(plaintext[n: n+AES.block_size], iv), key)
        iv = ciphertext[n: n+AES.block_size]

    return ciphertext


def xor(string1, string2):
    text = bytearray(len(string1))

    for i in range(len(string1)):
        text[i] = string1[i] ^ string2[i]

    return text


if __name__ == "__main__":
    crack()
