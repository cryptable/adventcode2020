import re
import copy

class AddressElement:
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


def processMask(idx, mask, address):
    if idx == 36:
        return [address]

    tmp_idx = idx + 1
    addresses = processMask(tmp_idx, mask, address)

    if mask[idx] == 'X':
        tmp_addresses = []
        for addr in addresses:
            addr.setBit(idx, 1)
            tmp_addresses.append(copy.deepcopy(addr))
        for addr in addresses:
            addr.setBit(idx, 0)
            tmp_addresses.append(copy.deepcopy(addr))
        return tmp_addresses

    if mask[idx] == '1':
        for addr in addresses:
            addr.setBit(idx, 1)

    return addresses


def processMasking(mask, value):
    address = AddressElement(value)

    return processMask(0, mask, address)


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
                address = mem_regex.match(entries[0]).group(1)
                value = int(entries[1].strip(' ').rstrip('\n'))
                for addr in processMasking(mask, int(address)):
                    memory[addr.getValue()] = value

    sum = 0
    print(mask)
    print(memory)
    for value in memory.values():
        print(value)
        sum += value

    print(sum)