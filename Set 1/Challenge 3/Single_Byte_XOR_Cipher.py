#Breaking single byte XOR ciphers by counting spaces in possible solns.
from binascii import unhexlify

def breakSingleByteXOR(binary):
    strings = []
    
    for key in range(256):
        string = ""
        
        for num in binary:
            string += chr(num^key)

        strings.append(string)

    return strings

if __name__ == "__main__":
    hexStr = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    analysis = bruteForce(unhexlify(hexStr))
    print(max(analysis, key=lambda s: s.count(' ')))
