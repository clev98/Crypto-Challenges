#ECB cut and paste
from os import urandom
from Cryptodome.Cipher import AES

AESKey = urandom(AES.block_size)

def kvparsing(kv):
    kvdict = {}
    kv = kv.split("&".encode('utf-8'))

    for pair in kv:
        pair = pair.split("=".encode('utf-8'))
        kvdict[pair[0]] = pair[1]

    return kvdict

def profileFor(email): #oracle
    assert not ("&".encode('utf-8') in email) and not ("=".encode('utf-8') in email)
    encoded = ("email=".encode('utf-8'))+email+("&uid=10&role=user".encode('utf-8'))
    return encryptAES_ECB(encoded, AESKey)

def encryptAES_ECB(plaintext, key):
    return bytearray(AES.new(key, AES.MODE_ECB).encrypt(addPKCS7Padding(plaintext, AES.block_size)))

def decryptAES_ECB(ciphertext, key):
    return AES.new(key, AES.MODE_ECB).decrypt(ciphertext)

def addPKCS7Padding(text, blockSize):
    if len(text) % blockSize:
        neededPadding = blockSize - len(text) % blockSize
        text += bytearray((chr(neededPadding)*neededPadding), 'utf-8')
            
    return text

def findBlocksize(oracle):
    unknownTextLength = len(oracle(bytearray()))
    i = 1

    while True:
        newTextLength = len(oracle(bytearray("A" * i, 'utf-8')))
        
        if newTextLength - unknownTextLength:
            return newTextLength - unknownTextLength
        i += 1

if __name__ == "__main__":
    blockSize = findBlocksize(profileFor)
    currentBytes = len("email=&uid=10&role=")

    if currentBytes % blockSize != 0:
        neededBytes = blockSize - currentBytes % blockSize
    else:
        neededBytes = 0

    email = bytearray("A"*neededBytes, 'utf-8')
    prefix = profileFor(email)[:neededBytes + currentBytes]
    currentBytes = len("email=")

    if currentBytes % blockSize != 0:
        neededBytes = blockSize - currentBytes % blockSize
    else:
        neededBytes = 0

    email = bytearray("A"*neededBytes, 'utf-8') + addPKCS7Padding("admin".encode('utf-8'), blockSize)
    postfix = profileFor(email)[currentBytes + neededBytes:2*blockSize]
    adminUser = prefix + postfix

    kvpairs = kvparsing(decryptAES_ECB(adminUser, AESKey))

    for item in kvpairs.keys():
        print(item.decode('utf-8')+": "+kvpairs[item].decode('utf-8'))
