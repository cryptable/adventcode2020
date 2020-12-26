import copy
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
        self.id = 1

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
            self.floor.append([None] * len(self.floor[self.origin[0]]))

    def insert_row(self):
        if self.even_row_from_origin():
            self.floor.insert(0, [None] * (len(self.floor[self.origin[0]])+1))
        else:
            self.floor.insert(0, [None] * len(self.floor[self.origin[0]]))
        self.origin = (self.origin[0]+1, self.origin[1])
        self.curr_pos = (self.curr_pos[0]+1, self.curr_pos[1])

    def add_col(self):
        for tile_row in self.floor:
            tile_row.append(None)

    def insert_col(self):
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
                        print('O', end=' ')
                    else:
                        print('.', end=' ')
                else:
                    print(' ', end=' ')
            print()

    def print_id(self):
        for tile_row_id in range(len(self.floor)):
            if self.even_row_from_origin_and(tile_row_id):
                print('   ', end='')
            for tile in self.floor[tile_row_id]:
                if tile:
                    print('{0:3d}'.format(tile.id), end='   ')
                else:
                    print('NNN', end='   ')
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
        line_pos = 0
        self.curr_pos = self.origin

        while line_pos < len(line):
            if line[line_pos:].startswith('se'):
                if self.curr_pos[0] == len(self.floor) - 1:
                    self.add_row()
                if (self.curr_pos[1] == len(self.floor[self.curr_pos[0]]) - 1) and self.odd_row_from_origin():
                    self.add_col()
                self.curr_pos = (self.curr_pos[0] + 1,
                                 (self.curr_pos[1] + 1) if self.even_row_from_origin() else self.curr_pos[1])
                line_pos += 2
            elif line[line_pos:].startswith('sw'):
                if self.curr_pos[0] == len(self.floor) - 1:
                    self.add_row()
                if self.curr_pos[1] == 0 and self.odd_row_from_origin():
                    self.insert_col()
                self.curr_pos = (self.curr_pos[0] + 1,
                                self.curr_pos[1] if self.even_row_from_origin() else (self.curr_pos[1] - 1))
                line_pos += 2
            elif line[line_pos:].startswith('ne'):
                if self.curr_pos[0] == 0:
                    self.insert_row()
                if self.curr_pos[1] == len(self.floor[self.curr_pos[0]]) - 1 and self.odd_row_from_origin():
                    self.add_col()
                self.curr_pos = (self.curr_pos[0] - 1,
                                 (self.curr_pos[1] + 1) if self.even_row_from_origin() else self.curr_pos[1])
                line_pos += 2
            elif line[line_pos:].startswith('nw'):
                if self.curr_pos[0] == 0:
                    self.insert_row()
                if self.curr_pos[1] == 0 and self.odd_row_from_origin():
                    self.insert_col()
                self.curr_pos = (self.curr_pos[0] - 1,
                                self.curr_pos[1] if self.even_row_from_origin() else (self.curr_pos[1] - 1))
                line_pos += 2
            elif line[line_pos:].startswith('e'):
                if self.curr_pos[1] == len(self.floor[self.curr_pos[0]]) - 1:
                    self.add_col()
                self.curr_pos = (self.curr_pos[0], self.curr_pos[1] + 1)
                line_pos += 1
            elif line[line_pos:].startswith('w'):
                if self.curr_pos[1] == 0:
                    self.insert_col()
                self.curr_pos = (self.curr_pos[0], self.curr_pos[1] - 1)
                line_pos += 1
            else:
                raise Exception("Unknown command")
            if not self.floor[self.curr_pos[0]][self.curr_pos[1]]:
                self.floor[self.curr_pos[0]][self.curr_pos[1]] = Tile(self.id)
                self.id += 1

        self.floor[self.curr_pos[0]][self.curr_pos[1]].flip()
#            self.print_id()

    def fill_empty_tiles(self):
        for row_idx in range(len(self.floor)):
            for col_idx in range(len(self.floor[row_idx])):
                if not self.floor[row_idx][col_idx]:
                    self.floor[row_idx][col_idx] = Tile(self.id)
                    self.id += 1

    def _check_se(self):
        row = self.curr_pos[0]
        col = self.curr_pos[1]
        if row == len(self.floor) - 1:
            return 'N'
        if (col == (len(self.floor[row]) - 1)) and not self.even_row_from_origin_and(row):
            return 'N'
        if self.even_row_from_origin_and(row):
            if self.floor[row + 1][col + 1]:
                return self.floor[row + 1][col + 1].color
        else:
            if self.floor[row + 1][col]:
                return self.floor[row + 1][col].color
        return 'N'

    def _check_sw(self):
        row = self.curr_pos[0]
        col = self.curr_pos[1]
        if row == len(self.floor) - 1:
            return 'N'
        if (col == 0) and not self.even_row_from_origin_and(row):
            return 'N'
        if self.even_row_from_origin_and(row):
            if self.floor[row + 1][col]:
                return self.floor[row + 1][col].color
        else:
            if self.floor[row + 1][col - 1]:
                return self.floor[row + 1][col - 1].color
        return 'N'

    def _check_ne(self):
        row = self.curr_pos[0]
        col = self.curr_pos[1]
        if row == 0:
            return 'N'
        if (col == (len(self.floor[row]) - 1)) and not self.even_row_from_origin_and(row):
            return 'N'
        if self.even_row_from_origin_and(row):
            if self.floor[row - 1][col + 1]:
                return self.floor[row - 1][col + 1].color
        else:
            if self.floor[row - 1][col]:
                return self.floor[row - 1][col].color
        return 'N'

    def _check_nw(self):
        row = self.curr_pos[0]
        col = self.curr_pos[1]
        if row == 0:
            return 'N'
        if (col == 0) and not self.even_row_from_origin_and(row):
            return 'N'
        if self.even_row_from_origin_and(row):
            if self.floor[row - 1][col]:
                return self.floor[row - 1][col].color
        else:
            if self.floor[row - 1][col - 1]:
                return self.floor[row - 1][col - 1].color
        return 'N'

    def _check_e(self):
        row = self.curr_pos[0]
        col = self.curr_pos[1]
        if col == (len(self.floor[row]) - 1):
            return 'N'
        if self.floor[row][col + 1]:
            return self.floor[row][col + 1].color
        return 'N'

    def _check_w(self):
        row = self.curr_pos[0]
        col = self.curr_pos[1]
        if col == 0:
            return 'N'
        if self.floor[row][col - 1]:
            return self.floor[row][col - 1].color
        return 'N'

    def _number_of_black_tiles(self):
        nbr_black_tiles = 0
        if self._check_se() == 'black':
            nbr_black_tiles += 1
        if self._check_sw() == 'black':
            nbr_black_tiles += 1
        if self._check_ne() == 'black':
            nbr_black_tiles += 1
        if self._check_nw() == 'black':
            nbr_black_tiles += 1
        if self._check_e() == 'black':
            nbr_black_tiles += 1
        if self._check_w() == 'black':
            nbr_black_tiles += 1
        return nbr_black_tiles

    def flip_tile(self, newfloor):
        row = self.curr_pos[0]
        col = self.curr_pos[1]
        nbr_black_tiles = self._number_of_black_tiles()

        if self.floor[row][col].color == 'black':
            if nbr_black_tiles == 0 or nbr_black_tiles > 2:
                newfloor[row][col].flip()
                return
        if self.floor[row][col].color == 'white':
            if nbr_black_tiles == 2:
                newfloor[row][col].flip()

    def flip_tiles(self):
        new_floor = copy.deepcopy(self.floor)
        for row_idx in range(len(self.floor)):
            for col_idx in range(len(self.floor[row_idx])):
                self.curr_pos = (row_idx, col_idx)
                self.flip_tile(new_floor)
        self.floor = new_floor

    def _row_of_white(self, row):
        res = True
        for tile in self.floor[row]:
            if tile and tile.color == 'black':
                return False
        return True

    def _col_of_white(self, col):
        res = True
        max_row_idx_origin = len(self.floor[self.origin[0]]) - 1
        for row_idx in range(len(self.floor)):
            if col > max_row_idx_origin and self.even_row_from_origin_and(row_idx):
                if self.floor[row_idx][col - 1] and self.floor[row_idx][col - 1].color == 'black':
                    return False
            else:
                if self.floor[row_idx][col] and self.floor[row_idx][col].color == 'black':
                    return False
        return True

    def grow_floor(self):
        self.curr_pos = ((len(self.floor) - 1), 0)
        if not self._row_of_white((len(self.floor) - 1)):
            self.add_row()
        if not self._col_of_white(len(self.floor[0]) - 1):
            self.add_col()
        self.curr_pos = (0, 0)
        if not self._row_of_white(0):
            self.insert_row()
        if not self._col_of_white(0):
            self.insert_col()

if __name__ == '__main__':
    id = 0
    floor = TileFloor()

    with open("input.txt", "r") as inFile:
        for line in inFile:
            floor.create_floor(line.rstrip('\n'))

    for i in range(10):
        floor.grow_floor()
        floor.fill_empty_tiles()
        floor.flip_tiles()
        print("nbr blacks: {}".format(floor.count_black()))
    for i in range(10, 100):
        floor.grow_floor()
        floor.fill_empty_tiles()
        floor.flip_tiles()
        if (i % 10) == 9:
            print("nbr blacks: {}".format(floor.count_black()))

    floor.print()
    print("nbr blacks: {}".format(floor.count_black()))