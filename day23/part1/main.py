class CircleBuffer:

    def __init__(self, init):
        self.buffer = [int(x) for x in list(init)]
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

    def _remove_cups(self, elements):
        for el in elements:
            self.buffer.remove(el)

    def _insert_cups(self, elements, cur_cup):
        after_cup = self._calculate_position(elements, cur_cup)
        after_cup_idx = self.buffer.index(after_cup) + 1
        for el in elements:
            self.buffer.insert(after_cup_idx, el)
            after_cup_idx += 1

    def _rotate_left(self):
        tmp = self.buffer[0]
        for i in range(len(self.buffer)-1):
            self.buffer[i] = self.buffer[i+1]
        self.buffer[len(self.buffer)-1] = tmp

    def _rotate_cup_to_index(self, cur_cup):
        cup_idx = self.buffer.index(cur_cup)
        while cup_idx > self.idx:
            self._rotate_left()
            cup_idx = self.buffer.index(cur_cup)

    def step(self):
        print("Index pos {}".format(self.idx))
        cur_cup = self.buffer[self.idx]
        take_cups = [self.buffer[(self.idx+i+1)%self.max] for i in range(3)]
        print(take_cups)
        self._remove_cups(take_cups)
        self._insert_cups(take_cups, cur_cup)
        self._rotate_cup_to_index(cur_cup)
        self.idx = (self.idx + 1) % self.max

    def print(self):
        idx_one = self.buffer.index(1)
        for i in range(len(self.buffer)-1):
            print(self.buffer[(idx_one+1+i) % len(self.buffer)], end='')

if __name__ == '__main__':
    input = "389125467"
    #input = "137826495"

    circle = CircleBuffer(input)
    for i in range(100):
        print("Move {}".format(i))
        circle.step()
        print(circle.buffer)
    circle.print()