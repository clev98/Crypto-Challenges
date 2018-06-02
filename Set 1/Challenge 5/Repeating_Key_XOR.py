#Repeating-key XOR encryption
from binascii import unhexlify, hexlify

def repeatingKeyXOR(string, key):
    keySpace = 0
    encrypted = ""

    for letter in string:
        encrypted += chr(letter^key[keySpace])

        if keySpace == len(key)-1:
            keySpace = 0
        else:
            keySpace += 1

    return encrypted.encode('utf-8').hex()

if __name__ == "__main__":
    org = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
    key = "ICE"

    print(repeatingKeyXOR(unhexlify(org.encode('utf-8').hex()), unhexlify(key.encode('utf-8').hex())))
