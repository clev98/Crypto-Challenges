# CBC Bitflipping Attack Example
from Cryptodome.Cipher import AES
from os import urandom
from Implement_CBC_mode import encryptAES_ECB_CBC, decryptAES_ECB_CBC


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


if __name__ == "__main__":
    crack()
