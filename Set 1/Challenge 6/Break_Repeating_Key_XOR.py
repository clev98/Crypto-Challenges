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
        result = ""

        for item in encryptedText:
            result += chr(item^key)

        keys.append(chr(key))
        strings.append(result)

    bestString = max(strings, key=lambda s: s.count(' '))
    
    for i in range(len(strings)):
        if bestString == strings[i]:
            return keys[i]

def decryptXOR(text, key):
    key = key*len(text)
    decrypted = ""

    for n in range(len(text)):
        decrypted += chr(text[n]^ord(key[n]))
        
    return decrypted

if __name__ == "__main__":
    data = readFile("\RIT\Crypto\\base64text.txt")
    keysize = guessKeySize(data)
    blockList = splitEncodedString(data, keysize)
    key = ""

    for block in blockList:
        key += breakSingleByteXOR(block)

    print("KEY: "+key+"\n")
    print(decryptXOR(data, key))
