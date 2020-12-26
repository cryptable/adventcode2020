
opposites = {'e':'w', 'ne':'sw', 'se':'nw', 'w':'e', 'nw':'se', 'sw':'ne'}


def opposite(direction):
    return opposites[direction]


class Tile:

    def __init__(self, id):
        self.id = id
        self.color = 'white'

    def flip(self):
        if self.color == 'white':
            self.color = 'black'
        else:
            self.color = 'white'

    def print(self):
        print("Tile id {} is {}".format(self.id, self.color))


class TileFloor:

    def __init__(self):
        self.origin = (0, 0)
        self.floor = [[Tile(0)]]
        self.curr_pos = (0, 0)

    # We're on an N+1-long row
    def odd_row_from_origin(self):
        return (abs(self.curr_pos[0]-self.origin[0]) % 2) == 1

    # We're on an N-long row
    def even_row_from_origin(self):
        return (abs(self.curr_pos[0]-self.origin[0]) % 2) == 0

    def even_row_from_origin_and(self, this):
        return (abs(this-self.origin[0]) % 2) == 0

    def add_row(self):
        if self.even_row_from_origin():
            self.floor.append([None] * (len(self.floor[self.origin[0]]) + 1))
        else:
            self.floor.append([None] * len(self.floor[0]))

    def insert_row(self):
        if self.even_row_from_origin():
            self.floor.insert(0, [None] * (len(self.floor[self.origin[0]])+1))
        else:
            self.floor.insert(0, [None] * len(self.floor[0]))
        self.origin = (self.origin[0]+1, self.origin[1])
        self.curr_pos = (self.curr_pos[0]+1, self.curr_pos[1])

    def add_col(self):
        for tile_row in self.floor:
            tile_row.append(None)

    def insert_col(self, update_cur_pos=False):
        for tile_row in self.floor:
            tile_row.insert(0, None)
        self.origin = (self.origin[0], self.origin[1]+1)
        self.curr_pos = (self.curr_pos[0], self.curr_pos[1]+1)

    def print(self):
        for tile_row_id in range(len(self.floor)):
            if self.even_row_from_origin_and(tile_row_id):
                print(' ', end='')
            for tile in self.floor[tile_row_id]:
                if tile:
                    if tile.color == 'black':
                        print('B', end=' ')
                    else:
                        print('W', end=' ')
                else:
                    print('N', end=' ')
            print()

    def print_id(self):
        for tile_row_id in range(len(self.floor)):
            if self.even_row_from_origin_and(tile_row_id):
                print(' ', end='')
            for tile in self.floor[tile_row_id]:
                if tile:
                    print('{}'.format(tile.id), end=' ')
                else:
                    print('N', end=' ')
            print()
        print('Origin {} {}'.format(self.origin[0], self.origin[1]))
        print('Cur Pos {} {}'.format(self.curr_pos[0], self.curr_pos[1]))

    def count_black(self):
        count_black = 0
        for tile_row in self.floor:
            for tile in tile_row:
                if tile and tile.color == 'black':
                    count_black += 1
        return count_black

    def create_floor(self, line):
        pos = 0
        id = 1
        while pos < len(line):
            if line[pos:].startswith('se'):
                if self.curr_pos[0] == len(self.floor) - 1:
                    self.add_row()
                if (self.curr_pos[1] == len(self.floor[self.curr_pos[0]]) - 1) and self.odd_row_from_origin():
                    self.add_col()
                self.curr_pos = (self.curr_pos[0] + 1,
                                 (self.curr_pos[1] + 1) if self.even_row_from_origin() else self.curr_pos[1])
                if not self.floor[self.curr_pos[0]][self.curr_pos[1]]:
                    self.floor[self.curr_pos[0]][self.curr_pos[1]] = Tile(id)
                self.print_id()
                pos += 2
            elif line[pos:].startswith('sw'):
                if self.curr_pos[0] == len(self.floor) - 1:
                    self.add_row()
                if self.curr_pos[1] == 0 and self.odd_row_from_origin():
                    self.insert_col()
                self.curr_pos = (self.curr_pos[0] + 1,
                                self.curr_pos[1] if self.even_row_from_origin() else (self.curr_pos[1] - 1))
                if not self.floor[self.curr_pos[0]][self.curr_pos[1]]:
                    self.floor[self.curr_pos[0]][self.curr_pos[1]] = Tile(id)
                self.print_id()
                pos += 2
            elif line[pos:].startswith('ne'):
                if self.curr_pos[0] == 0:
                    self.insert_row()
                if self.curr_pos[1] == len(self.floor[self.curr_pos[0]]) - 1 and self.odd_row_from_origin():
                    self.add_col()
                self.curr_pos = (self.curr_pos[0] - 1,
                                 (self.curr_pos[1] + 1) if self.even_row_from_origin() else self.curr_pos[1])
                if not self.floor[self.curr_pos[0]][self.curr_pos[1]]:
                    self.floor[self.curr_pos[0]][self.curr_pos[1]] = Tile(id)
                self.print_id()
                pos += 2
            elif line[pos:].startswith('nw'):
                if self.curr_pos[0] == 0:
                    self.insert_row()
                if self.curr_pos[0] == 0 and self.odd_row_from_origin():
                    self.insert_col()
                self.curr_pos = (self.curr_pos[0] - 1,
                                self.curr_pos[1] if self.even_row_from_origin() else (self.curr_pos[1] - 1))
                if not self.floor[self.curr_pos[0]][self.curr_pos[1]]:
                    self.floor[self.curr_pos[0]][self.curr_pos[1]] = Tile(id)
                self.print_id()
                pos += 2
            elif line[pos:].startswith('e'):
                if self.curr_pos[1] == len(self.floor[self.curr_pos[0]]) - 1:
                    self.add_col()
                self.curr_pos = (self.curr_pos[0], self.curr_pos[1] + 1)
                if not self.floor[self.curr_pos[0]][self.curr_pos[1]]:
                    self.floor[self.curr_pos[0]][self.curr_pos[1]] = Tile(id)
                self.print_id()
                pos += 1
            elif line[pos:].startswith('w'):
                if self.curr_pos[1] == 0:
                    self.insert_col(True)
                self.curr_pos = (self.curr_pos[0], self.curr_pos[1] - 1)
                if not self.floor[self.curr_pos[0]][self.curr_pos[1]]:
                    self.floor[self.curr_pos[0]][self.curr_pos[1]] = Tile(id)
                self.print_id()
                pos += 1
            else:
                raise Exception("Unknown command")
            id += 1

        self.floor[self.curr_pos[0]][self.curr_pos[1]].flip()


if __name__ == '__main__':
    id = 0
    floor = TileFloor()

    with open("input_test5.txt", "r") as inFile:
        for line in inFile:
            floor.create_floor(line.rstrip('\n'))

    floor.print_id()
    print("nbr blacks: {}".format(floor.count_black()))