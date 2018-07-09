#Break single byte XOR
#Take all possible solns and take the one with the most spaces (' ')
from binascii import unhexlify

def breakSingleByteXOR(byteStr):
    strings = []
    
    for key in range(256):
        string = bytearray(len(byteStr))
        
        for num in range(len(byteStr)):
            string[num] = byteStr[num]^key

        strings.append(string)

    return max(strings, key=lambda s: s.count(' '.encode('utf-8')))

if __name__ == "__main__":
    hexStr = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    print(breakSingleByteXOR(unhexlify(hexStr)))
