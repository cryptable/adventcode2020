class TimeEntry:

    def __init__(self, id, delta):
        self.id = id
        self.delta = delta


def correctSequence(testValue, list):
    result = True
    for entry in list:
        if entry.delta != calculateDelta(testValue, entry.id):
            result = False
    return result


def calculateDelta(testValue, id):
    result = testValue % id
    if result == 0:
        return result
    return id - result


def printData(testValue, list):
    for entry in list:
        entry_delta = calculateDelta(testValue, entry.id)
        print("{}: {} = {} - {} % {}".format(entry_delta, entry.delta, entry.id, testValue, entry.id))


if __name__ == '__main__':
    depart_time = 0
    time_table = []
    with open("input.txt") as inFile:
        depart_time = int(inFile.readline())
        tmp_time_table = inFile.readline().split(',')
        delta_min = 0
        highest = TimeEntry(0,0)
        for t in tmp_time_table:
            if t != 'x':
                if int(t) > highest.id:
                    highest = TimeEntry(int(t), delta_min)
                time_table.append(TimeEntry(int(t), delta_min))
            delta_min += 1
        inFile.close()

    notFinished = True
    testValue = (int(100000000000000 / highest.id) + 1) * highest.id
    # testValue = highest.id
    if highest.delta > 0:
        testValue = testValue - highest.delta
    print(testValue)
    printData(testValue, time_table)

    while notFinished:
        if correctSequence(testValue, time_table):
            break
#        print(testValue)
        testValue += highest.id

    printData(testValue, time_table)
    print(testValue)
