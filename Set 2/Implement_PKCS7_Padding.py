# Implement PKCS#7 Padding
def addPKCS7Padding(text, blockSize):
    if len(text) % blockSize:
        neededPadding = blockSize - len(text) % blockSize
        text += bytearray((chr(neededPadding)*neededPadding), 'utf-8')
    else:
        text += bytearray((chr(blockSize)*blockSize), 'utf-8')

    return text


def removePKCS7Padding(text, blockSize):
    for n in range(len(text) - 1, len(text) - text[-1] - 1, -1):
        if text[n] != text[-1]:
            return text

    return text[:-text[-1]]


if __name__ == "__main__":
    text = bytearray("YELLOW SUBMARINE", 'utf-8')

    addedPKCS = addPKCS7Padding(text, 16)
    print(addedPKCS)
    removedPKCS = removePKCS7Padding(addedPKCS, 16)
    print(removedPKCS)
