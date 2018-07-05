#Implement PKCS#7 Padding
def addPKCS7Padding(text, blockSize, paddingChar):
    neededPadding = blockSize - (len(text) % blockSize)

    if neededPadding > 0:
        for n in range(neededPadding):
            text += paddingChar
    return text

def removePKCS7Padding(text, paddingChar):
    for n in range(len(text)-1, -1, -1):
        if text[n] == ord(paddingChar):
            text.remove(ord(paddingChar))
    return text

if __name__ == "__main__":
    text = bytearray("YELLOW SUBMARINE", 'utf-8')
    paddingChar = bytearray("\x04", 'utf-8')
    
    addedPKCS = addPKCS7Padding(text, 20, paddingChar)
    print(addedPKCS)
    removedPKCS = removePKCS7Padding(addedPKCS, paddingChar)
    print(removedPKCS)
