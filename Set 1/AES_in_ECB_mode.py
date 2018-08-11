# Decrypts and encrypts AES in ECB mode given a key
from Cryptodome.Cipher import AES
from binascii import a2b_base64


def decryptAES_ECB(ciphertext, key):
    return AES.new(key, AES.MODE_ECB).decrypt(ciphertext)


def encryptAES_ECB(ciphertext, key):
    return AES.new(key, AES.MODE_ECB).encrypt(ciphertext)


if __name__ == "__main__":
    with open(r"7.txt") as file:
        ciphertext = a2b_base64(''.join(file.readlines()))

    key = "YELLOW SUBMARINE".encode('utf-8')
    print(decryptAES_ECB(ciphertext, key))
