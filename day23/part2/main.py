import cProfile


class CircleBuffer:

    def __init__(self, init):
        self.buffer = [int(x) for x in list(init)]
        for i in range(len(self.buffer), 1000000):
            self.buffer.append(i)
        self.idx = 0
        self.max = len(self.buffer)

    def _calculate_position(self, taken_cups, old_cup):
        old_cup -= 1
        if old_cup == 0:
            old_cup = 9
        while old_cup in taken_cups:
            old_cup -= 1
            if old_cup == 0:
                old_cup = 9
        return old_cup

    def _take_remove_cups(self, idx):
        cups = []
        for i in range(3):
            remove_cup_idx = (idx + i) % self.max
            cup = self.buffer[remove_cup_idx]
            cups.append(cup)
        return cups

    def add_idx(self, idx, val):
        return (idx + val) % self.max

    def dec_idx(self, idx):
        return (idx - 1) % self.max

    def _move_memory(self, after_cup_idx):
        # 3 places free after self.idx
        mem_idx = self.idx
        if (mem_idx + 1) == after_cup_idx:
            return
        stop_idx = self.dec_idx(after_cup_idx)
        while mem_idx != stop_idx:
            to_idx = self.add_idx(mem_idx, 3)
            self.buffer[to_idx] = self.buffer[mem_idx]
            mem_idx = self.dec_idx(mem_idx)
        self.idx = self.add_idx(self.idx, 3)

    def _insert_cups(self, elements, cur_cup):
        after_cup = self._calculate_position(elements, cur_cup)
        after_cup_idx = self.add_idx(self.buffer.index(after_cup), 1)
        self._move_memory(after_cup_idx)
        for el in elements:
            self.buffer[after_cup_idx] = el
            after_cup_idx = self.add_idx(after_cup_idx, 1)

    def step(self):
        # print("Index pos {}".format(self.idx))
        cur_cup = self.buffer[self.idx]
        # print(self.buffer)

#        with cProfile.Profile() as pr:
        take_cups = self._take_remove_cups(self.idx+1)
        self._insert_cups(take_cups, cur_cup)
#        pr.print_stats()

        # print(take_cups)
        self.idx = self.add_idx(self.idx, 1)

    def print(self):
        idx_one = self.buffer.index(1)
        for i in range(len(self.buffer) - 1):
            print(self.buffer[(idx_one + 1 + i) % len(self.buffer)], end='')
        print()

    def print_two_values_after_one(self):
        idx_one = self.buffer.index(1)
        print("Position N+1 of 1: {}".format(self.buffer[(idx_one + 1) % len(self.buffer)]))
        print("Position N+2 of 1: {}".format(self.buffer[(idx_one + 2) % len(self.buffer)]))

if __name__ == '__main__':
    #input = "389125467"
    input = "137826495"

    circle = CircleBuffer(input)

    for i in range(1000000):
        if (i%1000) == 0:
            print("-- Move {} --".format(i+1))
        circle.step()
    circle.print()
    circle.print_two_values_after_one()