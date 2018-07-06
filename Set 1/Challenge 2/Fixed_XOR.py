#XOR two equal-length buffers and return the production
from binascii import unhexlify, hexlify

def xor(string1, string2):
    encrypted = ""

    for i in range(len(string1)):
        encrypted += chr(string1[i]^string2[i])

    return encrypted.encode('utf-8').hex()

if __name__ == "__main__":
    print(xor(unhexlify("1c0111001f010100061a024b53535009181c"),unhexlify("686974207468652062756c6c277320657965")))
