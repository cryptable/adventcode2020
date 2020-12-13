class TimeEntry:

    def __init__(self, id, delta):
        self.id = id
        self.delta = delta


def calculateDelta(testValue, id):
    result = testValue % id
    if result == 0:
        return result
    return result


def correctSequence(testValue, list):
    for entry in list:
        if calculateDelta(testValue + entry.delta, entry.id) != 0:
            return False
    return True


def printData(testValue, list):
    for entry in list:
        entry_delta = calculateDelta(testValue, entry.id)
        print("delta({}) => {} = {} - {} % {}".format(entry_delta, entry.delta, entry.id, testValue, entry.id))


if __name__ == '__main__':
    depart_time = 0
    time_table = []
    with open("input.txt") as inFile:
        depart_time = int(inFile.readline())
        tmp_time_table = inFile.readline().split(',')
        delta_min = 0
        for t in tmp_time_table:
            if t != 'x':
                time_table.append(TimeEntry(id=int(t), delta=delta_min))
            delta_min += 1
        inFile.close()

    time_table.sort(key=lambda entry: entry.id, reverse=True)

    notFinished = True
    # testValue = (int(100000000000000 / time_table[0].id) + 1) * time_table[0].id
    testValue = time_table[0].id - time_table[0].delta
    startValue = testValue
    printData(testValue, time_table)

    idx = 1
    delta = 1
    while notFinished:
        if correctSequence(testValue, time_table[:idx]):
            if idx == len(time_table):
                break
            delta *= time_table[(idx-1)].id
            print("where:" + str(testValue))
            print("delta:" + str(delta))
            idx += 1
        else:
            testValue += delta
        print(testValue)

    printData(testValue, time_table)
    print(testValue)