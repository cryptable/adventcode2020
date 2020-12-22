import copy

class Cube:

    def __init__(self, id, square):
        self.id = id
        self.square = square
        self.state = 0

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


def compare_left(a, b):
    return cube1.left() == cube2.right()
def compare_right(a, b):
    return cube1.right() == cube2.left()
def compare_top(a, b):
    return cube1.top() == cube2.bottom()
def compare_bottom(a, b):
    return cube1.bottom() == cube2.top()


def check(cube1, cube2, comare_fn):
    nbr_sides_cube2 = 0
    if comare_fn(cube1, cube2):
        nbr_sides_cube2 += 1
    cube2.rotate()
    if comare_fn(cube1, cube2):
        nbr_sides_cube2 += 1
    cube2.rotate()
    if comare_fn(cube1, cube2):
        nbr_sides_cube2 += 1
    cube2.rotate()
    if comare_fn(cube1, cube2):
        nbr_sides_cube2 += 1
    cube2.rotate()
    cube2.vflip()
    if comare_fn(cube1, cube2):
        nbr_sides_cube2 += 1
    cube2.rotate()
    if comare_fn(cube1, cube2):
        nbr_sides_cube2 += 1
    cube2.rotate()
    if comare_fn(cube1, cube2):
        nbr_sides_cube2 += 1
    cube2.rotate()
    if comare_fn(cube1, cube2):
        nbr_sides_cube2 += 1
    cube2.rotate()
    return nbr_sides_cube2


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

        result = 1
        for cube1 in cubes:
            nbr_sides = 0
            for cube2 in cubes:
                if cube1 == cube2:
                    continue
                nbr_sides += check(cube1, cube2, comare_fn=compare_left)
                nbr_sides += check(cube1, cube2, comare_fn=compare_right)
                nbr_sides += check(cube1, cube2, comare_fn=compare_top)
                nbr_sides += check(cube1, cube2, comare_fn=compare_bottom)
            if nbr_sides == 2:
                result *= cube1.id
                print(cube1.id)
        print(result)