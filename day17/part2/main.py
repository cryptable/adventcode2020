import copy

Z_ID = 0
Z_PLANE = 1
W_ID = 0
W_CUBE = 1


def cube_set_active(tmp_cube, z, y, x, activate):
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

    def clear(self):
        for i in range(len(self.cube)):
            for j in range(len(self.cube[0][Z_PLANE])):
                for k in range(len(self.cube[0][Z_PLANE][0])):
                    cube_set_active(self.cube, i, j, k, False)

    def insert_planes(self):
        plane = []
        for y in range(len(self.cube[0][Z_PLANE])):
            plane.append(['.' for _ in range(len(self.cube[0][Z_PLANE][0]))])
        z_idx = self.cube[0][Z_ID]
        self.cube.insert(0, (z_idx - 1, plane))
        plane = copy.deepcopy(plane)
        z_idx = self.cube[len(self.cube) - 1][Z_ID]
        self.cube.append((z_idx + 1, plane))

    def remove_plane(self, last=False):
        if last:
            del self.cube[len(self.cube)-1]
        else:
            del self.cube[0]

    def remove_planes(self, last=False):
        self.remove_plane()
        self.remove_plane(True)

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

    def _extend_cube(self):
        self.insert_rows()
        self.insert_columns()
        self.insert_planes()

    def _remove_cube(self):
        self.remove_rows()
        self.remove_columns()
        self.remove_planes()

    def is_non_active_column(self, last=False):
        for plane in self.cube:
            for row in plane[Z_PLANE]:
                if last and row[len(row)-1] == '#':
                    return False
                if not last and row[0] == '#':
                    return False
        return True

    def remove_non_active_columns(self):
        while self.is_non_active_column():
            self.remove_column()
        while self.is_non_active_column(True):
            self.remove_column(True)

    def is_non_active_row(self, last=False):
        for plane in self.cube:
            rows = plane[Z_PLANE]
            row = rows[len(rows)-1] if last else rows[0]
            for val in row:
                if val == '#':
                    return False
        return True

    def remove_non_active_rows(self):
        while self.is_non_active_row():
            self.remove_row()
        while self.is_non_active_row(True):
            self.remove_row(True)

    def is_non_active_plane(self, last=False):
        plane = self.cube[len(self.cube) - 1][Z_PLANE] if last else self.cube[0][Z_PLANE]

        for row in plane:
            for val in row:
                if val == '#':
                    return False
        return True

    def remove_non_active_planes(self):
        while self.is_non_active_plane():
            self.remove_plane()
        while self.is_non_active_plane(True):
            self.remove_plane(True)

    def active(self, z, y, x):
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
                    result += self.active(z+i, y+j, x+k)
        return result

    def count_active(self):
        result = 0
        for i in range(len(self.cube)):
            for j in range(len(self.cube[0][Z_PLANE])):
                for k in range(len(self.cube[0][Z_PLANE][0])):
                    result += self.active(i, j, k)
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
                    if self.active(z_idx, y_idx, x_idx) == 1:
                        if not (count_active == 2 or count_active == 3):
                            cube_set_active(tmp_cube, z_idx, y_idx, x_idx, False)
                    if self.active(z_idx, y_idx, x_idx) == 0:
                        if count_active == 3:
                            cube_set_active(tmp_cube, z_idx, y_idx, x_idx, True)
        self.cube = tmp_cube
        self._remove_cube()
        self._optimize()

    def print(self, w_idx):
        for z_plane in self.cube:
            print("z={}, w={}".format(z_plane[0], w_idx))
            for row in z_plane[1]:
                print("".join(row))
            print("\n")


def hypercube_set_active(tmp_hypercube, w, z, y, x, activate):
    cube = tmp_hypercube[w][W_CUBE].cube
    cube_set_active(cube, z, y, x, activate)


class HyperCube:

    def __init__(self):
        self.hypercube = []
        self.hypercube.append((0, Cube()))

    def init_row_on_cube(self, w, z, row):
        cube = self.hypercube[w][W_CUBE]
        cube.init_row_on_plane(z, row)

    def active(self, w, z, y, x):
        cube = self.hypercube[w][W_CUBE]
        return cube.active(z, y, x)

    def insert_cubes(self):
        cube = copy.deepcopy(self.hypercube[0][W_CUBE])
        cube.clear()
        w_idx = self.hypercube[0][W_ID] - 1
        self.hypercube.insert(0, (w_idx, cube))
        cube = copy.deepcopy(self.hypercube[0][W_CUBE])
        cube.clear()
        w_idx = self.hypercube[len(self.hypercube)-1][W_ID] + 1
        self.hypercube.append((w_idx, cube))

    def remove_cube(self, last=False):
        if last:
            del self.hypercube[len(self.hypercube)-1]
        else:
            del self.hypercube[0]

    def remove_cubes(self):
        self.remove_cube()
        self.remove_cube(True)

    def is_non_active_cube(self, last=False):
        cube = self.hypercube[len(self.hypercube) - 1][W_CUBE] if last else self.hypercube[0][W_CUBE]

        if cube.count_active() > 0:
            return False

        return True

    def remove_non_active_cubes(self):
        while self.is_non_active_cube():
            self.remove_cube()
        while self.is_non_active_cube(True):
            self.remove_cube(True)

    def insert_planes(self):
        for w in self.hypercube:
            w[W_CUBE].insert_planes()

    def remove_plane(self, last=False):
        for cube in self.hypercube:
            cube[W_CUBE].remove_plane(last)

    def remove_planes(self):
        self.remove_plane()
        self.remove_plane(True)

    def is_non_active_plane(self, last=False):
        for cube in self.hypercube:
            if not cube[W_CUBE].is_non_active_plane():
                return False
        return True

    def remove_non_active_planes(self):
        while self.is_non_active_plane():
            self.remove_plane()
        while self.is_non_active_plane(True):
            self.remove_plane(True)

    def insert_rows(self):
        for w in self.hypercube:
            w[W_CUBE].insert_rows()

    def remove_row(self, last=False):
        for cube in self.hypercube:
            cube[W_CUBE].remove_row(last)

    def remove_rows(self):
        self.remove_row()
        self.remove_row(True)

    def is_non_active_row(self, last=False):
        for cube in self.hypercube:
            if not cube[W_CUBE].is_non_active_row():
                return False
        return True

    def remove_non_active_rows(self):
        while self.is_non_active_row():
            self.remove_row()
        while self.is_non_active_row(True):
            self.remove_row(True)

    def insert_columns(self):
        for w in self.hypercube:
            w[W_CUBE].insert_columns()

    def remove_column(self, last=False):
        for cube in self.hypercube:
            cube[W_CUBE].remove_column(last)

    def remove_columns(self):
        self.remove_column()
        self.remove_column(True)

    def is_non_active_column(self, last=False):
        for cube in self.hypercube:
            if not cube[W_CUBE].is_non_active_column():
                return False
        return True

    def remove_non_active_columns(self):
        while self.is_non_active_column():
            self.remove_column()
        while self.is_non_active_column(True):
            self.remove_column(True)

    def extend_hypercube(self):
        self.insert_cubes()
        self.insert_rows()
        self.insert_columns()
        self.insert_planes()

    def _remove_hypercube(self):
        self.remove_cubes()
        self.remove_rows()
        self.remove_columns()
        self.remove_planes()

    def _optimize(self):
        self.remove_non_active_cubes()
        self.remove_non_active_rows()
        self.remove_non_active_columns()
        self.remove_non_active_planes()

    def _count_active_around(self, w, z, y, x):
        result = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if w + i == w and z + j == z and y + k == y and x + l == x:
                            continue
                        result += self.active(w + i, z + j, y + k, x + l)
        return result

    def count_active(self):
        result = 0
        for cube in self.hypercube:
            result += cube[W_CUBE].count_active()
        return result

    def cycle(self):
        self.extend_hypercube()
        self.extend_hypercube()
        tmp_hypercube = copy.deepcopy(self.hypercube)
        for w_idx in range(1, len(self.hypercube)-1):
            cube = self.hypercube[w_idx][W_CUBE].cube
            for z_idx in range(1, len(cube)-1):
                plane = cube[z_idx][Z_PLANE]
                for y_idx in range(1, len(plane)-1):
                    row = plane[y_idx]
                    for x_idx in range(1, len(row)-1):
                        count_active = self._count_active_around(w_idx, z_idx, y_idx, x_idx)
                        if self.active(w_idx, z_idx, y_idx, x_idx) == 1:
                            if not (count_active == 2 or count_active == 3):
                                hypercube_set_active(tmp_hypercube, w_idx, z_idx, y_idx, x_idx, False)
                        if self.active(w_idx, z_idx, y_idx, x_idx) == 0:
                            if count_active == 3:
                                hypercube_set_active(tmp_hypercube, w_idx, z_idx, y_idx, x_idx, True)
        self.hypercube = tmp_hypercube
        self._remove_hypercube()
        self._optimize()

    def print(self):
        for w_cube in self.hypercube:
            w_cube[W_CUBE].print(w_cube[W_ID])


if __name__ == '__main__':
    hypercube = HyperCube()
    with open("input.txt", "r") as inFile:
        for line in inFile:
            hypercube.init_row_on_cube(0, 0, [x for x in line.rstrip('\n')])
        inFile.close()

        hypercube.cycle()
        hypercube.cycle()
        hypercube.cycle()
        hypercube.cycle()
        hypercube.cycle()
        hypercube.cycle()
        print(hypercube.count_active())
