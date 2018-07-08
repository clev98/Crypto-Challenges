#Repeating-key XOR
def repeatingKeyXOR(text, key):
    xorString = ""
    key = key*len(text)

    for n in range(len(text)):
        xorString += chr(text[n]^key[n])

    return xorString.encode('utf-8').hex()

if __name__ == "__main__":
    text = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal""".encode('utf-8')
    key = "ICE".encode('utf-8')

    print(repeatingKeyXOR(text, key))
