import copy

Z_ID = 0
Z_PLANE = 1


def _set_active(tmp_cube, z, y, x, activate):
    plane = tmp_cube[z][Z_PLANE]
    if activate:
#        print("{} {} {}: #".format(z, y, x))
        plane[y][x] = '#'
    else:
        plane[y][x] = '.'
#        print("{} {} {}: .".format(z, y, x))


class Cube:

    def __init__(self):
        self.cube = []
        self.cube.append((0, []))

    def init_row_on_plane(self, z, row):
        self.cube[z][Z_PLANE].append(row)

    def insert_planes(self):
        plane = []
        for y in range(len(self.cube[0][Z_PLANE])):
            plane.append(['.' for _ in range(len(self.cube[0][Z_PLANE][0]))])
        z_idx = self.cube[0][Z_ID]
        self.cube.insert(0, (z_idx - 1, plane))
        plane = copy.deepcopy(plane)
        z_idx = self.cube[len(self.cube) - 1][Z_ID]
        self.cube.append((z_idx + 1, plane))

    def insert_columns(self):
        for plane in self.cube:
            for row in plane[Z_PLANE]:
                row.insert(0, '.')
                row.append('.')

    def remove_column(self, last=False):
        for plane in self.cube:
            for row in plane[Z_PLANE]:
                if last:
                    del row[len(row)-1]
                else:
                    del row[0]

    def remove_columns(self):
        self.remove_column()
        self.remove_column(True)

    def insert_rows(self):
        for plane in self.cube:
            rows = plane[Z_PLANE]
            rows.insert(0, ['.' for _ in range(len(self.cube[0][Z_PLANE][0]))])
            rows.append(['.' for _ in range(len(self.cube[0][Z_PLANE][0]))])

    def remove_row(self, last=False):
        for plane in self.cube:
            rows = plane[Z_PLANE]
            if last:
                del rows[len(rows)-1]
            else:
                del rows[0]

    def remove_rows(self):
        self.remove_row()
        self.remove_row(True)

    def remove_plane(self, last=False):
        if last:
            del self.cube[len(self.cube)-1]
        else:
            del self.cube[0]

    def remove_planes(self, last=False):
        self.remove_plane()
        self.remove_plane(True)

    def _extend_cube(self):
        self.insert_rows()
        self.insert_columns()
        self.insert_planes()

    def _remove_cube(self):
        self.remove_rows()
        self.remove_columns()
        self.remove_planes()

    def _is_non_active_column(self, last=False):
        for plane in self.cube:
            for row in plane[Z_PLANE]:
                if last and row[len(row)-1] == '#':
                    return False
                if not last and row[0] == '#':
                    return False
        return True

    def remove_non_active_columns(self):
        while self._is_non_active_column():
            self.remove_column()
        while self._is_non_active_column(True):
            self.remove_column(True)

    def _is_non_active_row(self, last=False):
        for plane in self.cube:
            rows = plane[Z_PLANE]
            row = rows[len(rows)-1] if last else rows[0]
            for val in row:
                if val == '#':
                    return False
        return True

    def remove_non_active_rows(self):
        while self._is_non_active_row():
            self.remove_row()
        while self._is_non_active_row(True):
            self.remove_row(True)

    def _is_non_active_plane(self, last=False):
        plane = self.cube[len(self.cube) - 1][Z_PLANE] if last else self.cube[0][Z_PLANE]

        for row in plane:
            for val in row:
                if val == '#':
                    return False
        return True

    def remove_non_active_planes(self):
        while self._is_non_active_plane():
            self.remove_plane()
        while self._is_non_active_plane(True):
            self.remove_plane(True)

    def _active(self, z, y, x):
        plane = self.cube[z][Z_PLANE]
        if plane[y][x] == '#':
            return 1
        return 0

    def _count_active_around(self, z, y, x):
        result = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if z+i == z and y+j == y and x+k == x:
                        continue
                    result += self._active(z+i, y+j, x+k)
        return result

    def count_active(self):
        result = 0
        for i in range(len(self.cube)):
            for j in range(len(self.cube[0][Z_PLANE])):
                for k in range(len(self.cube[0][Z_PLANE][0])):
                    result += self._active(i, j, k)
        return result

    def _optimize(self):
        self.remove_non_active_rows()
        self.remove_non_active_columns()
        self.remove_non_active_planes()

    def cycle(self):
        self._extend_cube()
        self._extend_cube()
        tmp_cube = copy.deepcopy(self.cube)
        for z_idx in range(1, len(self.cube)-1):
            plane = self.cube[z_idx][Z_PLANE]
            for y_idx in range(1, len(plane)-1):
                row = plane[y_idx]
                for x_idx in range(1, len(row)-1):
                    count_active = self._count_active_around(z_idx, y_idx, x_idx)
                    if self._active(z_idx, y_idx, x_idx) == 1:
                        if not (count_active == 2 or count_active == 3):
                            _set_active(tmp_cube, z_idx, y_idx, x_idx, False)
                    if self._active(z_idx, y_idx, x_idx) == 0:
                        if count_active == 3:
                            _set_active(tmp_cube, z_idx, y_idx, x_idx, True)
        self.cube = tmp_cube
        self._remove_cube()
        self._optimize()

    def print(self):
        for z_plane in self.cube:
            print("z={}".format(z_plane[0]))
            for row in z_plane[1]:
                print("".join(row))
            print("\n")


if __name__ == '__main__':
    cube = Cube()
    with open("input.txt", "r") as inFile:
        for line in inFile:
            cube.init_row_on_plane(0, [x for x in line.rstrip('\n')])
        inFile.close()

        cube.cycle()
        cube.cycle()
        cube.cycle()
        cube.cycle()
        cube.cycle()
        cube.cycle()
        print(cube.count_active())
