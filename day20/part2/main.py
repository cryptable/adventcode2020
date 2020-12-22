import math
import copy

class Cube:

    def __init__(self, id, square):
        self.id = id
        self.square = square
        self.left_cube = None
        self.right_cube = None
        self.top_cube = None
        self.bottom_cube = None
        self.checked = False

    def print(self):
        for line in self.square:
            print(line)

    def print_side_ids(self):
        if self.left_cube:
            print("l({}): {}".format(self.id, self.left_cube.id))
        if self.right_cube:
            print("r({}): {}".format(self.id, self.right_cube.id))
        if self.top_cube:
            print("t({}): {}".format(self.id, self.top_cube.id))
        if self.bottom_cube:
            print("b({}): {}".format(self.id, self.bottom_cube.id))

    def top(self):
        return self.square[0]

    def bottom(self):
        return self.square[len(self.square)-1]

    def left(self, idx=0):
        result = ''
        for line in self.square:
            result += line[idx]
        return result

    def right(self, idx=0):
        result = ''
        for line in self.square:
            result += line[-(1+idx)]
        return result

    def rotate(self):
        tmp_square = []
        for i in range(len(self.square)):
            tmp_square.append(self.left(i)[::-1])
        self.square = tmp_square

    def hflip(self):
        tmp_square = self.square[::-1]
        self.square = tmp_square

    def vflip(self):
        tmp_square = []
        for line in self.square:
            tmp_square.append(line[::-1])
        self.square = tmp_square

    def tag_left(self, cube):
        self.left_cube = cube

    def tag_right(self, cube):
        self.right_cube = cube

    def tag_top(self, cube):
        self.top_cube = cube

    def tag_bottom(self, cube):
        self.bottom_cube = cube

    def is_tagged(self):
        return self.left_cube or self.right_cube or self.top_cube or self.bottom_cube

    def nbr_tagged_sides(self):
        nbr_sides = 0
        if self.left_cube:
            nbr_sides += 1
        if self.right_cube:
            nbr_sides += 1
        if self.top_cube:
            nbr_sides += 1
        if self.bottom_cube:
            nbr_sides += 1
        return nbr_sides

    def get_left_cube(self):
        return self.left_cube

    def get_right_cube(self):
        return self.right_cube

    def get_top_cube(self):
        return self.top_cube

    def get_bottom_cube(self):
        return self.bottom_cube

    def is_checked(self):
        return self.checked

    def remove_border(self):
        del self.square[0]
        del self.square[len(self.square)-1]
        for idx in range(len(self.square)):
            self.square[idx] = self.square[idx][1:-1]

    def check_pattern(self, row, col, pattern):
        for pattern_row_idx in range(len(pattern.square)):
            for pattern_col_idx in range(len(pattern.square[0])):
                if pattern.square[pattern_row_idx][pattern_col_idx] == ' ':
                    continue
                if pattern.square[pattern_row_idx][pattern_col_idx] != self.square[row + pattern_row_idx][col + pattern_col_idx]:
                    return False
        return True

    def search_pattern(self, pattern):
        pattern_idxs = []
        for row_idx in range(len(self.square) - len(pattern.square)):
            for col_idx in range(len(self.square[0]) - len(pattern.square[0])):
                if self.check_pattern(row_idx, col_idx, pattern):
                    pattern_idxs.append((row_idx, col_idx))
        return pattern_idxs

    def del_pattern(self, row, col, pattern):
        for pattern_row_idx in range(len(pattern.square)):
            for pattern_col_idx in range(len(pattern.square[0])):
                if pattern.square[pattern_row_idx][pattern_col_idx] == '#':
                    self.square[row + pattern_row_idx] = self.square[row + pattern_row_idx][:col + pattern_col_idx] + 'O' + self.square[row + pattern_row_idx][col + pattern_col_idx + 1:]

    def count_waves(self):
        waves = 0
        for row_idx in range(len(self.square)):
            for col_idx in range(len(self.square[0])):
                if self.square[row_idx][col_idx] == '#':
                    waves += 1
        return waves


def compare_left(a, b):
    return a.left() == b.right()


def compare_right(a, b):
    return a.right() == b.left()


def compare_top(a, b):
    return a.top() == b.bottom()


def compare_bottom(a, b):
    return a.bottom() == b.top()


def tag_left(a, b):
    a.tag_left(b)
    b.tag_right(a)


def tag_right(a, b):
    a.tag_right(b)
    b.tag_left(a)


def tag_top(a, b):
    a.tag_top(b)
    b.tag_bottom(a)


def tag_bottom(a, b):
    a.tag_bottom(b)
    b.tag_top(b)


def check(cube1, cube2, compare_fn, tag_fn):
    if compare_fn(cube1, cube2):
        tag_fn(cube1, cube2)
        return 1
    if cube2.is_tagged():
        return 0
    cube2.rotate()
    if compare_fn(cube1, cube2):
        tag_fn(cube1, cube2)
        return 1
    cube2.rotate()
    if compare_fn(cube1, cube2):
        tag_fn(cube1, cube2)
        return 1
    cube2.rotate()
    if compare_fn(cube1, cube2):
        tag_fn(cube1, cube2)
        return 1
    cube2.rotate()
    cube2.vflip()
    if compare_fn(cube1, cube2):
        tag_fn(cube1, cube2)
        return 1
    cube2.rotate()
    if compare_fn(cube1, cube2):
        tag_fn(cube1, cube2)
        return 1
    cube2.rotate()
    if compare_fn(cube1, cube2):
        tag_fn(cube1, cube2)
        return 1
    cube2.rotate()
    if compare_fn(cube1, cube2):
        tag_fn(cube1, cube2)
        return 1
    cube2.rotate()
    return 0


def has_untagged_cubes(cubes):
    for cube in cubes:
        if cube.is_tagged():
            return False
    return True


def all_cubes_checked(cubes):
    for cube in cubes:
        if not cube.is_checked():
            return False
    return True


def traverse(tbc_cubes, cubes):

    while not all_cubes_checked(cubes) and len(tbc_cubes):
        tbc_cube = tbc_cubes.pop()
        if tbc_cube.is_checked():
            continue
        for cube in cubes:
            if check(tbc_cube, cube, compare_fn=compare_left, tag_fn=tag_left) > 0:
                tbc_cubes.append(cube)
            if check(tbc_cube, cube, compare_fn=compare_right, tag_fn=tag_right) > 0:
                tbc_cubes.append(cube)
            if check(tbc_cube, cube, compare_fn=compare_top, tag_fn=tag_top) > 0:
                tbc_cubes.append(cube)
            if check(tbc_cube, cube, compare_fn=compare_bottom, tag_fn=tag_bottom) > 0:
                tbc_cubes.append(cube)
        tbc_cube.checked = True


def reorden(cubes):
    left_cube = None
    newcubes = []
    for id in range(len(cubes)):
        if cubes[id].nbr_tagged_sides() == 2 and cubes[id].get_right_cube() and cubes[id].get_bottom_cube():
            left_cube = cubes[id]
            break

    current_cube = left_cube
    while True:
        newcubes.append(current_cube)
        if not current_cube.get_right_cube():
            if current_cube.get_bottom_cube():
                left_cube = left_cube.get_bottom_cube()
                current_cube = left_cube
            else:
                break
        else:
            current_cube = current_cube.get_right_cube()
    return newcubes


class Pattern:

    def __init__(self):
        self.id = id
        self.square = ["                  # ", "#    ##    ##    ###", " #  #  #  #  #  #   "]

    def print(self):
        for line in self.square:
            print(line)

    def top(self):
        return self.square[0]

    def bottom(self):
        return self.square[len(self.square)-1]

    def left(self, idx=0):
        result = ''
        for line in self.square:
            result += line[idx]
        return result

    def right(self, idx=0):
        result = ''
        for line in self.square:
            result += line[-(1+idx)]
        return result

    def rotate(self):
        tmp_square = []
        for i in range(len(self.square)):
            tmp_square.append(self.left(i)[::-1])
        self.square = tmp_square

    def hflip(self):
        tmp_square = self.square[::-1]
        self.square = tmp_square

    def vflip(self):
        tmp_square = []
        for line in self.square:
            tmp_square.append(line[::-1])
        self.square = tmp_square


def search_rotations(orig_cube, new_cube, pattern):
    all_pos = []
    pattern_positions = orig_cube.search_pattern(pattern)
    for pos in pattern_positions:
        new_cube.del_pattern(pos[0], pos[1], pattern)
    orig_cube.rotate()
    new_cube.rotate()
    all_pos += pattern_positions
    pattern_positions = orig_cube.search_pattern(pattern)
    for pos in pattern_positions:
        new_cube.del_pattern(pos[0], pos[1], pattern)
    orig_cube.rotate()
    new_cube.rotate()
    all_pos += pattern_positions
    pattern_positions = orig_cube.search_pattern(pattern)
    for pos in pattern_positions:
        new_cube.del_pattern(pos[0], pos[1], pattern)
    orig_cube.rotate()
    new_cube.rotate()
    all_pos += pattern_positions
    pattern_positions = orig_cube.search_pattern(pattern)
    for pos in pattern_positions:
        new_cube.del_pattern(pos[0], pos[1], pattern)
    orig_cube.rotate()
    new_cube.rotate()
    all_pos += pattern_positions

    return all_pos


if __name__ == '__main__':
    cubes = []
    with open("input.txt", "r") as inFile:
        id = 0
        square = []
        for line in inFile:
            if line == '\n':
                cubes.append(Cube(id, square))
                square = []
                continue
            if line.startswith("Tile"):
                tmp = line.rstrip('\n').rstrip(':').split(' ')
                id = int(tmp[1])
                continue
            square.append(line.rstrip('\n'))
        if square:
            cubes.append(Cube(id, square))
        inFile.close()
        traverse([cubes[0]], cubes)

    newcubes = reorden(cubes)

    for cube in newcubes:
        cube.remove_border()

    length = int(math.sqrt(len(newcubes)))
    big_square = []
    for i in range(length):
        for l in range(len(newcubes[0].square)):
            square_line = ''
            for j in range(length):
                cube = newcubes[i*length + j]
                square_line += cube.square[l]
            big_square.append(square_line)

    big_cube = Cube(0, big_square)
    new_big_cube = copy.deepcopy(big_cube)
    pattern = Pattern()

    pattern_positions = search_rotations(big_cube, new_big_cube, pattern)
    big_cube.vflip()
    new_big_cube.vflip()
    pattern_positions += search_rotations(big_cube, new_big_cube, pattern)

    print(len(pattern_positions))
    new_big_cube.print()
    print(big_cube.count_waves())
    print(new_big_cube.count_waves())