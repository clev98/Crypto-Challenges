#Decrypts and encrypts AES in ECB mode given a key
from Crypto.Cipher import AES
from binascii import a2b_base64

def readFile(path):
    with open(path) as cipherText:
        cipher = a2b_base64(''.join(cipherText.readlines()))

    return cipher

def decryptAES_ECB(cipher, key):
    return AES.new(key, AES.MODE_ECB).decrypt(cipher).decode('utf-8')

if __name__ == "__main__":
    cipher = readFile("\RIT\Crypto\Set 1\Challenge 7\\7.txt")
    print(decryptAES_ECB(cipher,"YELLOW SUBMARINE".encode('utf-8')))
