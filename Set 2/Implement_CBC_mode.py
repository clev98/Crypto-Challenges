#Implement CBC mode
from Cryptodome.Cipher import AES
from binascii import a2b_base64

def readFile(path):
    with open(path) as file:
        ciphertext = a2b_base64(''.join(file.readlines()))

    return ciphertext

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

    for n in range(0, len(text), AES.block_size):
        plaintext[n: n+AES.block_size] = xor(decryptAES_ECB(ciphertext[n: n+AES.block_size], key), iv)
        iv = ciphertext[n: n+AES.block_size]

    return removePKCS7Padding(plaintext, AES.block_size)

def encryptAES_ECB(plaintext, key):
    return AES.new(key, AES.MODE_ECB).encrypt(plaintext)

def encryptAES_ECB_CBC(plaintext, key, iv):
    plaintext = addPKCS7Padding(plaintext, AES.block_size)
    ciphertext = bytearray(len(plaintext))

    for n in range(0, len(text), AES.block_size):
        ciphertext[n: n+AES.block_size] = encryptAES_ECB(xor(plaintext[n: n+AES.block_size], iv), key)
        iv = ciphertext[n: n+AES.block_size]

    return ciphertext

def xor(string1, string2):
    text = bytearray(len(string1))

    for i in range(len(string1)):
        text[i] = string1[i]^string2[i]

    return text

if __name__ == "__main__":
    text = readFile("10.txt")
    key = "YELLOW SUBMARINE".encode('utf-8')
    #iv being the initialization vector 
    iv = ("\x00"*AES.block_size).encode('utf-8')
    print(decryptAES_ECB_CBC(text, key, iv))

    #Test
    #plaintext = bytearray("Please work code", 'utf-8')
    #print(decryptAES_ECB_CBC(encryptAES_ECB_CBC(plaintext, key, iv), key, iv))
