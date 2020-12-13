
def processAdapters(adapters, idx, history):

    print("begin {} : {}".format(idx, history))

    if idx == (len(adapters)-1):
        print("end")
        return 1
    diff = adapters[idx+1] - adapters[idx]
    idx += 1
    if diff == 1:
        if history[0] == 0 and history[1] == 0:
            history[1] = 0
            history[0] = 1
            return processAdapters(adapters, idx, history)
        else:
            history[1] = history[0]
            history[0] = 1
            possibilities = processAdapters(adapters, idx, history)
            history[1] = history[0]
            history[0] = 0
            possibilities += processAdapters(adapters, idx, history)
            return possibilities
    if diff == 2:
        if history[0] == 0 and history[1] == 0:
            return 0
        if history[0] == 1:
            history[0] = 0
            history[1] = 1
            possibilities = processAdapters(adapters, idx, history)
            history[0] = 0
            history[1] = 0
            possibilities += processAdapters(adapters, idx, history)
            return possibilities
        if history[0] == 1:
            history[0] = 0
            history[1] = 0
            return processAdapters(adapters, idx, history)
    if diff == 3:
        if history[0] == 1:
            history[0] = 0
            history[1] = 0
            return processAdapters(adapters, idx, history)

    if diff > 3 or diff <= 0:
        raise Exception("Unusable adapter")

    print("end {} : {}".format(diff, history))
    return 0


def createDifferences(list):
    diff_list = []
    for i in range(0, len(list)-1):
        diff_list.append(list[i+1] - list[i])
    return diff_list

# 0 conseq 1 = 1
# 1 conseq 1 = 1
# 2 conseq 1 = 2
# 3 conseq 1 = 4
# 4 conseq 1 = 7
# 5 conseq 1 = 13
# 6 conseq 1 = 24
# 7 conseq 1 = 44
# 8 conseq 1 = 81

# 1 1 1 1
# 2 1 1
# 1 2 1
# 1 1 2
# 3 1
# 1 3
# 2 2
# 1 + 3 + 2 + 1 = 7

# 1 1 1 1 1
# 2 1 1 1
# 1 2 1 1
# 1 1 2 1
# 1 1 1 2
# 3 1 1
# 1 3 1
# 1 1 3
# 1 2 2
# 2 1 2
# 2 2 1
# 2 3
# 3 2
# 1 + 4 + 3 + 3 + 2 = 13

# 1 1 1 1 1 1
# 2 1 1 1 1
# 1 2 1 1 1
# 1 1 2 1 1
# 1 1 1 2 1
# 1 1 1 1 2
# 3 1 1 1
# 1 3 1 1
# 1 1 3 1
# 1 1 1 3
# 2 2 1 1
# 2 1 2 1
# 2 1 1 2
# 1 2 2 1
# 1 2 1 2
# 1 1 2 2
# 2 2 2
# 3 2 1
# 3 1 2
# 2 3 1
# 2 1 3
# 1 2 3
# 1 3 2
# 3 3
# 1 + 5 + 4 + (3 + 2 + 1) + 1 + 3*2 + 1 = 24

# 1 1 1 1 1 1 1
# 2 1 1 1 1 1
# 3 1 1 1 1
# 2 2 1 1 1
# 2 2 2 1
# 3 2 1 1
# 3 2 2
# 3 3 1
# 1 + 6 + 5 + (4 + 3 + 2 + 1) + 4 + 4*3 + 3 + 3 = 44

# 1 1 1 1 1 1 1 1
# 2 1 1 1 1 1 1
# 3 1 1 1 1 1
# 2 2 1 1 1 1
# 2 2 2 1 1
# 2 2 2 2
# 3 2 1 1 1
# 3 2 2 1
# 3 3 1 1
# 3 3 2

# 1 + 7 + 6 + (5 + 4 + 3 + 2 + 1) + (4 + 3 + 2 + 1) + 1 + 5*4 + 4*3 + (3 + 2 + 1) + 3 = 81


def consecutiveOnes(list):
    ones = 0
    result = []
    for i in list:
        if i == 1:
            ones += 1
        else:
            result.append(ones)
            ones = 0
    return result


if __name__ == '__main__':
    adapters = [0]
    with open("./input.txt", "r") as infile:
        for line in infile:
            adapters.append(int(line))
        infile.close()

    adapters.sort()
    adapters.append(adapters[-1]+3)

    diff_list = createDifferences(adapters)

    cons_ones = consecutiveOnes(diff_list)
    # 0 conseq 1 = 1
    # 1 conseq 1 = 1
    # 2 conseq 1 = 2
    # 3 conseq 1 = 4
    # 4 conseq 1 = 7
    # 5 conseq 1 = 13
    # 6 conseq 1 = 24
    # 7 conseq 1 = 44
    # 8 conseq 1 = 81
    print(cons_ones)
    count_ones = [1, 1, 2, 4, 7, 13, 24, 44, 81]

    total = 1
    for i in cons_ones:
        total = total * count_ones[i]

    print(total)