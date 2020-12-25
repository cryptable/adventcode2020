import cProfile

class Node:

    def __init__(self, cup):
        self.next_cup = cup

class CircleBuffer:

    def __init__(self, init):
        print(init)
        tmp_buffer = [int(x) for x in list(init)]
        self.buffer = [None] * (len(tmp_buffer)+1)
        for idx in range(len(tmp_buffer)):
            if idx == len(tmp_buffer)-1:
                self.buffer[tmp_buffer[idx]] = Node(len(tmp_buffer)+1)
            else:
                next_cup = tmp_buffer[idx+1]
                self.buffer[tmp_buffer[idx]] = Node(next_cup)
        for i in range(len(tmp_buffer), 1000000):
            self.buffer.append(Node(i+2 if i != 999999 else tmp_buffer[0]))

        print("Node {}".format(self.buffer[7].next_cup))
        self.curr_cup = tmp_buffer[0]

    def _cup_in_taken_cups(self, first_taken_cups, old_cup):
        tmp = first_taken_cups
        for _ in range(3):
            if tmp == old_cup:
                return True
            tmp = self.buffer[tmp].next_cup
        return False

    def _calculate_position(self, first_taken_cups, old_cup):
        old_cup -= 1
        if old_cup == 0:
            old_cup = len(self.buffer) - 1
        while self._cup_in_taken_cups(first_taken_cups, old_cup):
            old_cup -= 1
            if old_cup == 0:
                old_cup = len(self.buffer) - 1
        return old_cup

    def _take_cups(self, from_cup):
        result = self.buffer[from_cup].next_cup
        tmp = self.buffer[from_cup].next_cup
        tmp = self.buffer[tmp].next_cup
        tmp = self.buffer[tmp].next_cup
        self.buffer[from_cup].next_cup = self.buffer[tmp].next_cup
        return result

    def _insert_cups(self, elements, cur_cup):
        after_cup = self._calculate_position(elements, cur_cup)
#        print("Position : {}".format(after_cup))
        cup_after_cup = self.buffer[after_cup].next_cup
        self.buffer[after_cup].next_cup = elements
        tmp = self.buffer[elements].next_cup
        tmp = self.buffer[tmp].next_cup
        self.buffer[tmp].next_cup = cup_after_cup


    def step(self):
#        print("Index pos {}".format(self.curr_cup))
#        print("Buffer: ", end='')
#        self.print_all()

        take_cups = self._take_cups(self.curr_cup)

#        print("Taken: ",end='')
#        self.print_taken(take_cups)

        self._insert_cups(take_cups, self.curr_cup)

#        print("Buffer - after: ", end='')
#        self.print_all()

        self.curr_cup = self.buffer[self.curr_cup].next_cup

    def print_taken(self, cup):
        tmp = cup
        for i in range(3):
            print(tmp, end='')
            tmp = self.buffer[tmp].next_cup
        print()

    def print_all(self):
        tmp = self.buffer[1]
        for i in range(1, len(self.buffer)):
            print(tmp.next_cup, end='')
            tmp = self.buffer[tmp.next_cup]
        print()

    def print_buf(self):
        print("buf: ", end='')
        for i in range(1, len(self.buffer)):
            print(self.buffer[i].next_cup, end='')
        print()

    def print(self):
        tmp = self.buffer[1]
        for i in range(1, len(self.buffer) - 1):
            print(tmp.next_cup, end='')
            tmp = self.buffer[tmp.next_cup]
        print()

    def print_two_values_after_one(self):
        print("Position N+1 of 1: {}".format(self.buffer[1].next_cup))
        print("Position N+2 of 1: {}".format(self.buffer[self.buffer[1].next_cup].next_cup))
        print("Multiplication of N+1 and N+2: {}".format(format(self.buffer[1].next_cup * self.buffer[self.buffer[1].next_cup].next_cup)))

if __name__ == '__main__':
    #input = "389125467"
    input = "137826495"

    circle = CircleBuffer(input)

    for i in range(10000000):
 #       if (i%1000) == 0:
 #           print("-- Move {} --".format(i+1))
        circle.step()
 #   circle.print()
    circle.print_two_values_after_one()