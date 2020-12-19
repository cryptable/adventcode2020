import time

def newNumberToSpeak(value, list):
    first = -1
    second = -1
    for idx in range(len(list)-1, -1, -1):
        if list[idx] == value:
            if first == -1:
                first = idx
            elif second == -1:
                return first-idx
    return 0


if __name__ == '__main__':
#    startingNumbers = [0, 3, 6]
#    startingNumbers = [1, 3, 2]
#    startingNumbers = [2, 1, 3]
#    startingNumbers = [1, 2, 3]
#    startingNumbers = [2, 3, 1]
#    startingNumbers = [3, 2, 1]
#    startingNumbers = [3, 1, 2]
    startingNumbers = [1, 0, 16, 5, 17, 4]
    turn = len(startingNumbers)
    numberPosition = {}
    for idx in range(len(startingNumbers)):
        numberPosition[startingNumbers[idx]] = [idx]

    lastNumber = startingNumbers[turn - 1]
#    LAST = 2020
    LAST = 30000000

    time1 = time.perf_counter()
    while turn < LAST:
        if len(numberPosition[lastNumber]) >= 2:
            positions = numberPosition[lastNumber]
            lastNumber = positions[len(positions)-1] - positions[len(positions)-2]
        else:
            lastNumber = 0
        if lastNumber in numberPosition:
            numberPosition[lastNumber].append(turn)
        else:
            numberPosition[lastNumber] = [turn]
        turn += 1
    time2 = time.perf_counter()

    print(time2 - time1)
    print(lastNumber)


