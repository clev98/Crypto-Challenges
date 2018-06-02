#XOR two equal-length buffers and return the production
from binascii import unhexlify, hexlify

def xor(hex, compare):
    binStr = unhexlify(hex)
    binCompare = unhexlify(compare)
    encrypted = ""

    for i in range(len(binStr)):
        encrypted += chr(binStr[i]^binCompare[i])

    return encrypted.encode('utf-8').hex()

if __name__ == "__main__":
    print(xor("1c0111001f010100061a024b53535009181c","686974207468652062756c6c277320657965"))
    
