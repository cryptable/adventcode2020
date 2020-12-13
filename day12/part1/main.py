class Direction:

    def __init__(self, dir):
        self.direction = dir[0]
        self.movement = int(dir[1:])


class Ferry:

    def __init__(self, dir):
        self.facing = dir
        self.positionEastWest = 0
        self.positionNorthSouth = 0

    def _go(self, dir, mov):
        if dir == 'E':
            self.positionEastWest += mov
        if dir == 'W':
            self.positionEastWest -= mov
        if dir == 'N':
            self.positionNorthSouth += mov
        if dir == 'S':
            self.positionNorthSouth -= mov

    def _rotate(self, degrees, dirs):
        if (degrees % 360) == 90:
            return dirs[1]
        if (degrees % 360) == 180:
            return dirs[2]
        if (degrees % 360) == 270:
            return dirs[3]
        if (degrees % 360) == 0:
            return dirs[0]
        raise Exception("Unknown direction")

    def navigate(self, dir):
        if dir.direction == 'F':
            self._go(self.facing, dir.movement)
            return
        if dir.direction == 'R':
            if self.facing == 'N':
                self.facing = self._rotate(dir.movement, ['N','E','S','W'])
            elif self.facing == 'E':
                self.facing = self._rotate(dir.movement, ['E','S','W','N'])
            elif self.facing == 'S':
                self.facing = self._rotate(dir.movement, ['S','W','N','E'])
            elif self.facing == 'W':
                self.facing = self._rotate(dir.movement, ['W','N','E','S'])
            else:
                raise Exception("R: Unkown facing")
            return
        if dir.direction == 'L':
            if self.facing == 'N':
                self.facing = self._rotate(dir.movement, ['N','W','S','E'])
            elif self.facing == 'W':
                self.facing = self._rotate(dir.movement, ['W','S','E','N'])
            elif self.facing == 'S':
                self.facing = self._rotate(dir.movement, ['S','E','N','W'])
            elif self.facing == 'E':
                self.facing = self._rotate(dir.movement, ['E','N','W','S'])
            else:
                raise Exception("L: Unkown facing")
            return
        self._go(dir.direction, dir.movement)


if __name__ == '__main__':
    directions = []
    with open("input.txt", "r") as inFile:
        for line in inFile:
            directions.append(Direction(line.rstrip('\n')))
        inFile.close()

    ferry = Ferry('E')
    for dir in directions:
        ferry.navigate(dir)

    print(abs(ferry.positionEastWest))
    print(abs(ferry.positionNorthSouth))
    print(abs(ferry.positionEastWest) + abs(ferry.positionNorthSouth))

