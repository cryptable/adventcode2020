def processAdapters(adapters):
    nbrDiff1 = 0
    nbrDiff2 = 0
    nbrDiff3 = 0
    for i in range(0, len(adapters)-1):
        diff = adapters[i+1] - adapters[i]
        if diff == 1:
            nbrDiff1 += 1
        if diff == 2:
            nbrDiff2 += 1
        if diff == 3:
            nbrDiff3 += 1
        if diff > 3 or diff <= 0:
            raise Exception("Unusable adapter")

    return (nbrDiff1, nbrDiff2, nbrDiff3)


if __name__ == '__main__':
    adapters = [0]
    with open("./input.txt", "r") as infile:
        for line in infile:
            adapters.append(int(line))
        infile.close()

    adapters.sort()
    adapters.append(adapters[-1]+3)
    differences = processAdapters(adapters)
    print(differences)
    print(differences[0] * differences[2])
