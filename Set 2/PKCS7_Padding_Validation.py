# Validate PKCS7 Padding
def testPadding(text):
    paddingByte = text[-1]
    padding = text[-paddingByte:]

    for byte in padding:
        if byte != paddingByte:
            raise Exception("Invalid PKCS7 Padding")
    return text


if __name__ == "__main__":
    test = b'\x94\x84\x12\t\xa5\xe6\xc6\x8b\x1a\xa7o\x8c\xf6@\xaf\x01'
    print(test)
    testPadding(test)
