#Detect a string from a list of sixty that has been encrypted by a
#single character XOR.
from binascii import unhexlify

def readFile(file):
    strList = []
    
    with open(file) as data:
        for line in data:
            strList.append(line.strip())

    return strList

def breakSingleByteXOR(byteStr):
    strings = []
    
    for key in range(256):
        string = ""
        
        for num in byteStr:
            string += chr(num^key)

        strings.append(string)

    return max(strings, key=lambda s: s.count(' ')).strip('\n')

if __name__ == "__main__":
    strList = readFile("4.txt")

    for string in strList:
        possibleSoln = breakSingleByteXOR(unhexlify(string))

        if possibleSoln.isprintable():
            print(possibleSoln)
            break
