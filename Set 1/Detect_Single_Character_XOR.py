# Detect a string from a list of sixty that has been encrypted by a
# single character XOR.
from binascii import unhexlify
from Break_Single_Byte_XOR import breakSingleByteXOR


def readFile(file):
    strList = []

    with open(file) as data:
        for line in data:
            strList.append(line.strip())

    return strList


if __name__ == "__main__":
    strList = readFile(r"C:\Users\Connor\Desktop\Code\Python3\Crypto\Set 1\4.txt")

    for string in strList:
        possibleSoln = breakSingleByteXOR(unhexlify(string))

        try:
            possibleSoln = possibleSoln.decode('utf-8').strip("\n")

            if possibleSoln.isprintable():
                print(possibleSoln)
                break

        except UnicodeDecodeError:
            continue
