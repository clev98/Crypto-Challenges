# Detect AES in ECB mode
from collections import defaultdict


def detectECB(ciphertext, blocksize=16):
    repeats = defaultdict(lambda: -1)

    for n in range(0, len(ciphertext), blocksize):
        repeats[ciphertext[n:n+blocksize]] += 1

    return sum(repeats.values())


if __name__ == "__main__":
    lines = []

    with open(r"8.txt") as file:
        for line in file:
            lines.append(line)

    for line in lines:
        if detectECB(line) > 0:
            print(line)
