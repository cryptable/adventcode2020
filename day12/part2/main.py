class Direction:

    def __init__(self, dir):
        self.direction = dir[0]
        self.movement = int(dir[1:])


class WayPoint:

    def __init__(self, initialEastWest, initialNortSouth):
        self.positionEastWest = initialEastWest
        self.positionNorthSouth = initialNortSouth

    def _rotateRight(self, degrees):
        if (degrees % 360) == 90:
            tmp = self.positionEastWest
            self.positionEastWest = self.positionNorthSouth
            self.positionNorthSouth = -tmp
            return
        if (degrees % 360) == 180:
            self.positionEastWest = -self.positionEastWest
            self.positionNorthSouth = -self.positionNorthSouth
            return
        if (degrees % 360) == 270:
            tmp = self.positionEastWest
            self.positionEastWest = -self.positionNorthSouth
            self.positionNorthSouth = tmp
            return
        if (degrees % 360) == 0:
            return
        raise Exception("Unknown direction")

    def _rotateLeft(self, degrees):
        if (degrees % 360) == 90:
            tmp = self.positionEastWest
            self.positionEastWest = -self.positionNorthSouth
            self.positionNorthSouth = tmp
            return
        if (degrees % 360) == 180:
            self.positionEastWest = -self.positionEastWest
            self.positionNorthSouth = -self.positionNorthSouth
            return
        if (degrees % 360) == 270:
            tmp = self.positionEastWest
            self.positionEastWest = self.positionNorthSouth
            self.positionNorthSouth = -tmp
            return
        if (degrees % 360) == 0:
            return
        raise Exception("Unknown direction")

    def _go(self, dir, mov):
        if dir == 'E':
            self.positionEastWest += mov
        if dir == 'W':
            self.positionEastWest -= mov
        if dir == 'N':
            self.positionNorthSouth += mov
        if dir == 'S':
            self.positionNorthSouth -= mov

    def move(self, dir):
        if dir.direction == 'R':
            self._rotateRight(dir.movement)
            return
        if dir.direction == 'L':
            self._rotateLeft(dir.movement)
            return

        self._go(dir.direction, dir.movement)


class Ferry:

    def __init__(self):
        self.positionEastWest = 0
        self.positionNorthSouth = 0

    def navigate(self, waypoint):
        self.positionEastWest += waypoint.positionEastWest
        self.positionNorthSouth += waypoint.positionNorthSouth


if __name__ == '__main__':
    directions = []
    with open("input.txt", "r") as inFile:
        for line in inFile:
            directions.append(Direction(line.rstrip('\n')))
        inFile.close()

    ferry = Ferry()
    waypoint = WayPoint(10, 1)
    for dir in directions:
        if dir.direction == 'F':
            for _ in range(0, dir.movement):
                ferry.navigate(waypoint)
        else:
            waypoint.move(dir)
            print("EW: {}, NS: {}".format(waypoint.positionEastWest, waypoint.positionNorthSouth))

    print(abs(ferry.positionEastWest))
    print(abs(ferry.positionNorthSouth))
    print(abs(ferry.positionEastWest) + abs(ferry.positionNorthSouth))

