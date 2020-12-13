def invalidNumber(premem, value):
    for i in range(0, len(premem)):
        for j in range((i+1), len(premem)):
            if (premem[i] + premem[j]) == value:
                return False
    return True


def processMemory(mem, preamble):
    max = len(mem) - preamble
    for idx in range(preamble, len(mem)):
        premem = mem[(idx-preamble):idx]
        if invalidNumber(premem, mem[idx]):
            return (idx, mem[idx])


def sum(mem):
    sum = 0
    for term in mem:
        sum += term
    return sum


def findSequenceSum(nbr, mem):
    for i in range(0, len(mem)):
        for j in range(i+1, len(mem)):
            if sum(mem[i:j]) > nbr:
                break
            if sum(mem[i:j]) == nbr:
                return mem[i:j]
    return []


if __name__ == '__main__':
    mem = []
    with open("./input.txt", "r") as infile:
        for line in infile:
            mem.append(int(line))
        infile.close()

    (idx, wrong_nbr) = processMemory(mem, 25)
    print(wrong_nbr)

    region = findSequenceSum(wrong_nbr, mem[0:idx])
    region.sort()
    print(region)
    print(region[0] + region[len(region)-1])