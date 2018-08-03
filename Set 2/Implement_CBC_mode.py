# Implement CBC mode
from Cryptodome.Cipher import AES
from binascii import a2b_base64
from Set1.Fixed_XOR import xor
from Set1.AES_in_ECB_mode import decryptAES_ECB, encryptAES_ECB
from Implement_PKCS7_Padding import addPKCS7Padding, removePKCS7Padding


def readFile(path):
    with open(path) as file:
        ciphertext = a2b_base64(''.join(file.readlines()))

    return ciphertext


def decryptAES_ECB_CBC(ciphertext, key, iv):
    plaintext = bytearray(len(ciphertext))

    for n in range(0, len(ciphertext), AES.block_size):
        plaintext[n: n+AES.block_size] = xor(decryptAES_ECB(ciphertext[n: n+AES.block_size], key), iv)
        iv = ciphertext[n: n+AES.block_size]

    return removePKCS7Padding(plaintext, AES.block_size)


def encryptAES_ECB_CBC(plaintext, key, iv):
    plaintext = addPKCS7Padding(plaintext, AES.block_size)
    ciphertext = bytearray(len(plaintext))

    for n in range(0, len(plaintext), AES.block_size):
        ciphertext[n: n+AES.block_size] = encryptAES_ECB(xor(plaintext[n: n+AES.block_size], iv), key)
        iv = ciphertext[n: n+AES.block_size]

    return ciphertext


if __name__ == "__main__":
    text = readFile(r"10.txt")
    key = "YELLOW SUBMARINE".encode('utf-8')
    # iv being the initialization vector
    iv = ("\x00"*AES.block_size).encode('utf-8')
    print(decryptAES_ECB_CBC(text, key, iv))

    # Test
    #plaintext = bytearray("Please work code", 'utf-8')
    #print(decryptAES_ECB_CBC(encryptAES_ECB_CBC(plaintext, key, iv), key, iv))
