#Break Repeating Key XOR
import base64

def readFile(path):
    data = ""
    
    with open(path, "r") as file:
        for line in file:
            data += line.strip().strip("\n")
            
    return bytearray(base64.b64decode(data))

def hammingDistance(string1, string2):
    xorString = ''.join(format(x, '08b') for x in xor(string1, string2))
    distance = 0

    for num in xorString:
        if num == "1":
            distance += 1
            
    return distance

def guessKeySize(byteString):
    distance = float("inf")
    normalizedDistance = 0
    rKeysize = 0
    
    for keysize in range(2, 40):
        for j in range(len(byteString)//keysize):
            normalizedDistance += hammingDistance(byteString[j:j+keysize], byteString[j+keysize:j+2*keysize])/keysize

        normalizedDistance //= len(byteString)//keysize
        
        if normalizedDistance < distance:
            distance = normalizedDistance
            rKeysize = keysize
            
    return rKeysize

def tranposeEncodedString(byteString, keysize):
    byteList = [byteString[i:i+keysize] for i in range(0, len(byteString), keysize)]
    blockList = [[] for n in range(keysize)]
    
    for item in byteList:
        for n in range(len(item)):
            blockList[n].append(item[n])
            
    return blockList

def breakSingleByteXOR(encryptedText):
    keys = []
    strings = []

    for key in range(256):
        keys.append(chr(key))
        strings.append(xor(encryptedText, (chr(key)*len(encryptedText)).encode('utf-8')))

    bestString = max(strings, key=lambda s: s.count(' '.encode('utf-8')))
    
    for i in range(len(strings)):
        if bestString == strings[i]:
            return keys[i]

def xor(text, key):
    output = bytearray(len(text))

    for n in range(len(text)):
        output[n] = text[n]^key[n]
        
    return output

if __name__ == "__main__":
    encodedString = readFile("6.txt")
    keysize = guessKeySize(encodedString)
    blockList = tranposeEncodedString(encodedString, keysize)
    key = ""

    for block in blockList:
        key += breakSingleByteXOR(block)

    print("KEY: "+key+"\n")
    print(xor(encodedString, (key*len(encodedString)).encode('utf-8')))
