import re
class MemoryElement:
    SIZE = 36

    def __init__(self, value):
        self.memory = [ 0 for x in range(self.SIZE)]
        idx = 35
        while value > 0 and idx >= 0:
            rest = value % 2
            if rest == 1:
                self.memory[idx] = 1
                value -= 1
            value = value / 2
            idx -= 1
        if value > 0:
            raise Exception("Value too big")

    def getValue(self):
        result = 0
        for value in self.memory:
            result *= 2
            if value == 1:
                result += 1
        return result

    def setBit(self, idx, value):
        self.memory[idx] = value


def processMasking(mask, value):
    memEl = MemoryElement(value)

    for idx in range(len(mask)):
        if mask[idx] == '1':
            memEl.setBit(idx, 1)
        if mask[idx] == '0':
            memEl.setBit(idx, 0)

    return memEl


if __name__ == '__main__':
    mask = []
    memory = {}
    mem_regex = re.compile("mem\[(\d+)\]")
    with open("input.txt", "r") as inFile:
        for line in inFile:
            entries = line.split('=')
            if entries[0].strip(' ') == 'mask':
                mask = list(entries[1].strip(' ').rstrip('\n'))
            else:
                print(entries[0])
                m = mem_regex.match(entries[0]).group(1)
                print(m)
                memory[m] = processMasking(mask, int(entries[1].strip(' ').rstrip('\n')))

    sum = 0
    print(mask)
    for value in memory.values():
        print(value.memory)
        sum += value.getValue()

    print(sum)