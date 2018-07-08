#Convert a hex string to base64
import base64
from binascii import unhexlify

def hexToBase64(string):
    return base64.b64encode(unhexlify(string))

if __name__ == "__main__":
    hexStr = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    print(hexToBase64(hexStr))
