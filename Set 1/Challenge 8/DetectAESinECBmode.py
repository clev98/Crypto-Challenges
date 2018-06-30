#Detect AES in ECB mode
from collections import defaultdict

def detectECB(path, blockLength=16):
    with open(path) as file:
        maxRepeats = 0
        probableCiphertext = ""
        
        for line in file:
            repeats = defaultdict(lambda: -1)
            line = line.strip()
            
            for n in range(0, len(line), blockLength):
                repeats[line[n:n+blockLength]] += 1

            loopSum = sum(repeats.values())

            if loopSum > maxRepeats:
                maxRepeats = loopSum
                probableCiphertext = line

    return probableCiphertext

if __name__ == "__main__":
    print(detectECB("8.txt"))
