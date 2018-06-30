#Decrypts AES in ECB mode given a key
#Using PyCryptodome module
from Crypto.Cipher import AES
from binascii import a2b_base64

def readFile(path):
    with open(path) as cipherText:
        cipher = a2b_base64(''.join(cipherText.readlines()))

    return cipher

def decryptAES_ECB(cipher, key):
    suite = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    return suite.decrypt(cipher).decode('utf-8')

if __name__ == "__main__":
    cipher = readFile("encryptedtext7.txt")
    print(decryptAES_ECB(cipher,"YELLOW SUBMARINE"))
