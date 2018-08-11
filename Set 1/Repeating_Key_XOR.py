# Repeating-key XOR
from Fixed_XOR import xor


def repeatingKeyXOR(text, key):
    assert len(text) >= len(key)

    if not len(text) % len(key):
        return xor(text, key*(len(text)/len(key)))
    else:
        count = 0
        encoded = bytearray()

        for char in range(len(text)):
            encoded += bytearray([text[char] ^ key[count]])

            if count == len(key) - 1:
                count = 0
            else:
                count += 1
        return encoded


if __name__ == "__main__":
    text = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal""".encode('utf-8')
    key = "ICE".encode('utf-8')

    print(repeatingKeyXOR(text, key).hex())
