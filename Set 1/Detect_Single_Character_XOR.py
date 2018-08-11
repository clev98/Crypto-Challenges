# Detect a string from a list of sixty that has been encrypted by a
# single character XOR.
from binascii import unhexlify
from Break_Single_Byte_XOR import breakSingleByteXOR


if __name__ == "__main__":
    strList = []

    with open(r"4.txt") as data:
        for line in data:
            strList.append(line.strip())

    for string in strList:
        possibleSoln = breakSingleByteXOR(unhexlify(string))

        try:
            possibleSoln = possibleSoln.decode('utf-8').strip("\n")

            if possibleSoln.isprintable():
                print(possibleSoln)
                break

        except UnicodeDecodeError:
            continue
