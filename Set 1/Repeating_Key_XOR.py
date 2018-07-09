#Repeating-key XOR
def repeatingKeyXOR(text, key):
    xorString = bytearray(len(text))
    i = 0

    for n in range(len(text)):
        xorString[n] = text[n]^key[i]

        if i == len(key)-1:
            i = 0
        else:
            i += 1

    return xorString

if __name__ == "__main__":
    text = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal""".encode('utf-8')
    key = "ICE".encode('utf-8')

    print(repeatingKeyXOR(text, key).hex())
