#Decrypts and encrypts AES in ECB mode given a key
from Crypto.Cipher import AES
from binascii import a2b_base64

def readFile(path):
    with open(path) as cipherText:
        ciphertext = a2b_base64(''.join(cipherText.readlines()))

    return ciphertext

def decryptAES_ECB(cipher, key):
    return AES.new(key, AES.MODE_ECB).decrypt(cipher).decode('utf-8')

if __name__ == "__main__":
    ciphertext = readFile("7.txt")
    key = "YELLOW SUBMARINE".encode('utf-8')
    print(decryptAES_ECB(ciphertext, key))
