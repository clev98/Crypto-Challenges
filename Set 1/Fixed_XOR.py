#XOR two equal-length buffers and return the production
from binascii import unhexlify, hexlify

def xor(string1, string2):
    assert len(string1) == len(string2)
    
    xorString = ""

    for i in range(len(string1)):
        xorString += chr(string1[i]^string2[i])

    return xorString.encode('utf-8').hex()

if __name__ == "__main__":
    string1 = "1c0111001f010100061a024b53535009181c"
    string2 = "686974207468652062756c6c277320657965"
    print(xor(unhexlify(string1),unhexlify(string2)))
