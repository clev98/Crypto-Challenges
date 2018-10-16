# Break Repeating Key XOR
from base64 import b64decode
from Fixed_XOR import xor
from Repeating_Key_XOR import repeatingKeyXOR


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

    for keysize in range(2, len(byteString)//2):
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
        strings.append(xor(encryptedText, bytearray([key]*len(encryptedText))))

    bestString = max(strings, key=lambda s: s.count(' '.encode('utf-8')))

    for i in range(len(strings)):
        if bestString == strings[i]:
            return keys[i]


def breakRepeatingKeyXOR(encodedString):
    keysize = guessKeySize(encodedString)
    blockList = tranposeEncodedString(encodedString, keysize)
    key = ""

    for block in blockList:
        key += breakSingleByteXOR(block)

    return key


if __name__ == "__main__":
    data = bytearray()

    with open(r"6.txt", "r") as file:
        for line in file:
            data += b64decode(line.strip().strip("\n"))

    key = breakRepeatingKeyXOR(data)

    print("KEY: "+key+"\n")
    print(repeatingKeyXOR(data, bytearray(key, 'utf-8')))
