# ECB cut and paste
from os import urandom
from Cryptodome.Cipher import AES
from Set1.AES_in_ECB_mode import encryptAES_ECB, decryptAES_ECB
from Implement_PKCS7_Padding import addPKCS7Padding


AESKey = urandom(AES.block_size)


def kvparsing(kv):
    kvdict = {}
    kv = kv.split("&".encode('utf-8'))

    for pair in kv:
        pair = pair.split("=".encode('utf-8'))
        kvdict[pair[0]] = pair[1]

    return kvdict


def profileFor(email):  # oracle
    assert not ("&".encode('utf-8') in email) and not ("=".encode('utf-8') in email)
    encoded = ("email=".encode('utf-8'))+email+("&uid=10&role=user".encode('utf-8'))
    return bytearray(encryptAES_ECB(addPKCS7Padding(encoded, AES.block_size), AESKey))


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
