#Detect whether ECB or CBC is being used.
#This will not correctly determine the encryption used on shorter messages.
#Provided the plaintext has the same 16 bytes of text repeated at least once, the encryption method will be properly determined. 
from os import urandom
from Cryptodome.Cipher import AES
from random import randint
from collections import defaultdict

def encryption_oracle(plaintext):
    paddedPlaintext = addPKCS7Padding(urandom(randint(5,10))+plaintext+urandom(randint(5,10)), AES.block_size)

    if randint(0, 1):
        return encryptAES_ECB(paddedPlaintext, urandom(AES.block_size))
    else:
        return encryptAES_ECB_CBC(paddedPlaintext, urandom(AES.block_size), urandom(AES.block_size))

def detectECB(ciphertext, blocksize): 
    repeats = defaultdict(lambda: -1)
            
    for n in range(0, len(ciphertext), blocksize):
        repeats[ciphertext[n:n+blocksize]] += 1

    return sum(repeats.values())

def addPKCS7Padding(text, blockSize):
    if len(text) % blockSize:
        neededPadding = blockSize - len(text) % blockSize
        text += bytearray((chr(neededPadding)*neededPadding), 'utf-8')
            
    return text

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
        text[i] = string1[i]^string2[i]

    return text

if __name__ == "__main__":
    text = """You might think I'm crazy
To hang around with you
Maybe you think I'm lucky
To have something to do
But I think that you're wild
Inside me is some child
You might think I'm foolish
Or maybe it's untrue
(You might think) you might think I'm crazy
(All I want) but all I want is you
You might think it's hysterical
But I know when you're weak
You think you're in the movies
And everything's so deep
But I think that you're wild
When you flash that fragile smile
You might think it's foolish
What you put me through
(You might think) you might think I'm crazy
(All I want) but all I want is you
And it was hard, so hard to take
There's no escape without a scrape
You kept it going 'till the sun fell down
You kept it going
Well you might think I'm delirious
The way I run you down
But somewhere sometimes, when you're curious
I'll be back around
Oh I think that you're wild
And so uniquely styled
You might think it's foolish
This chancy rendezvous
(You might think) you might think I'm crazy
(All I want) but all I want is you
All I want is you
All I want is you"""
    
    plaintext = bytearray(text, 'utf-8')
    
    if detectECB(bytes(encryption_oracle(plaintext)), AES.block_size) > 0:
        print("Encrypted with ECB")
    else:
        print("Encrypted with CBC")
