#Validate PKCS7 Padding
from Cryptodome.Cipher import AES

def testPadding(text, blocksize):
    if len(text) % blocksize:
        raise Exception("Invalid PKCS7 Padding")
    
    for n in range(len(text) - 1, len(text) - text[-1] - 1, -1):
        if text[n] != text[-1]:
            raise Exception("Invalid PKCS7 Padding")

    return text

if __name__ == "__main__":
    print(testPadding("ICE ICE BABY\x04\x04\x04\x04".encode('utf-8'), AES.block_size))
