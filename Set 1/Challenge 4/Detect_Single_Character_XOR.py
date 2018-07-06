#Detect a string from a list of sixty that has been encrypted by a
#single character XOR.
from binascii import unhexlify

def readFile(file):
    dataList = []
    
    with open(file) as data:
        for line in data:
            dataList.append(line.strip())

    return dataList

def breakSingleByteXOR(binary):
    strings = []
    
    for key in range(256):
        string = ""
        
        for num in binary:
            string += chr(num^key)

        strings.append(string)

    return strings

if __name__ == "__main__":
    dataList = readFile("hex_strings.txt")

    for data in dataList:
        analysis = bruteForce(unhexlify(data))
        possibleSoln = max(analysis, key=lambda s: s.count(' ')).strip('\n')

        if possibleSoln.isprintable():
            print(possibleSoln)
            break
