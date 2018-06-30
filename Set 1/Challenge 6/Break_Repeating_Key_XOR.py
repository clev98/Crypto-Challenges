#Break Repeating Key XOR
import base64

def readFile(path):
    data = ""
    
    with open(path, "r") as file:
        for line in file:
            data += line.strip().strip("\n")
            
    #data += "="*((4-len(data)%4)%4)
    return bytearray(base64.b64decode(data))

def hammingDistance(string1, string2):
    distance = 0
    string1 = ''.join(format(x, '08b') for x in string1)
    string2 = ''.join(format(x, '08b') for x in string2)

    for i in range(len(string1)):
        if string1[i] != string2[i]:
            distance += 1
            
    return distance

def guessKeySize(byteString):
    distance = float("inf")
    normalizedDistance = 0
    rKeysize = 0
    
    for keysize in range(2, 40):
        for j in range(len(byteString)//keysize):
            tmpDistance = hammingDistance(byteString[j:j+keysize], byteString[j+keysize:2*(j+keysize)])
            normalizedDistance += tmpDistance/keysize

        normalizedDistance //= len(byteString)//keysize
        
        if normalizedDistance < distance:
            distance = normalizedDistance
            rKeysize = keysize
            
    return rKeysize

def splitEncodedString(byteString, keysize):
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

    bestString = max(strings, key=lambda s: s.count(' '))
    
    for i in range(len(strings)):
        if bestString == strings[i]:
            return keys[i]

def xor(text, key):
    output = ""

    for n in range(len(text)):
        output += chr(text[n]^key[n])
        
    return output

if __name__ == "__main__":
    data = readFile("base64text.txt")
    keysize = guessKeySize(data)
    blockList = splitEncodedString(data, keysize)
    key = ""

    for block in blockList:
        key += breakSingleByteXOR(block)

    print("KEY: "+key+"\n")
    print(xor(data, (key*len(data)).encode('utf-8')))
