
opposites = {'e':'w', 'ne':'sw', 'se':'nw', 'w':'e', 'nw':'se', 'sw':'ne'}


def opposite(direction):
    return opposites[direction]


class Tile:

    def __init__(self, id):
        self.id = id
        self.color = 'white'
        self.tiles = {}
        self.tiles_adj = {}
        self.tiles['e'] = None
        self.tiles['se'] = None
        self.tiles['sw'] = None
        self.tiles['w'] = None
        self.tiles['nw'] = None
        self.tiles['ne'] = None
        # tuple adjecent direction, direction new tile to add link
        self.tiles_adj['e'] = [('se', 'sw'), ('ne', 'nw')]
        self.tiles_adj['se'] = [('e', 'ne'), ('sw', 'w')]
        self.tiles_adj['sw'] = [('se', 'e'), ('w', 'nw')]
        self.tiles_adj['w'] = [('sw', 'se'), ('nw', 'ne')]
        self.tiles_adj['nw'] = [('w', 'sw'), ('ne', 'e')]
        self.tiles_adj['ne'] = [('nw', 'w'), ('e', 'se')]

    def flip(self):
        if self.color == 'white':
            self.color = 'black'
        else:
            self.color = 'white'

    def add_tile(self, direction, new_tile):
        if not self.tiles[direction]:
            self.tiles[direction] = new_tile
            new_tile.tiles[opposite(direction)] = self
            for adj in self.tiles_adj[direction]:
                if self.tiles[adj[0]]:
                    new_tile.add_tile(adj[1], self.tiles[adj[0]])

        return new_tile

    def get_tile(self, direction):
        return self.tiles[direction]

    def print(self):
        print("Tile id {}".format(self.id))
        for (key, val) in self.tiles.items():
            if val:
                print("Connection {} {}".format(key, val.id))


def processTile(curr_tile, direction, id, tiles):
    tile = None

    if curr_tile.get_tile(direction):
        tile = curr_tile.get_tile(direction)
    else:
        id += 1
        tile = curr_tile.add_tile(direction, Tile(id))
        tiles.append(tile)

    return (id, tiles, tile)


def processLine(line, tiles, id):
    pos = 0
    curr_tile = tiles[0]

    while pos < len(line):
        if line[pos:].startswith('se'):
            (id, tiles, curr_tile) = processTile(curr_tile, 'se', id, tiles)
            pos += 2
        if line[pos:].startswith('sw'):
            (id, tiles, curr_tile) = processTile(curr_tile, 'sw', id, tiles)
            pos += 2
        if line[pos:].startswith('ne'):
            (id, tiles, curr_tile) = processTile(curr_tile, 'ne', id, tiles)
            pos += 2
        if line[pos:].startswith('nw'):
            (id, tiles, curr_tile) = processTile(curr_tile, 'nw', id, tiles)
            pos += 2
        if line[pos:].startswith('e'):
            (id, tiles, curr_tile) = processTile(curr_tile, 'e', id, tiles)
            pos += 1
        if line[pos:].startswith('w'):
            (id, tiles, curr_tile) = processTile(curr_tile, 'w', id, tiles)
            pos += 1
        print("--- Added tile : {}".format(curr_tile.id))
        curr_tile.print()

    curr_tile.flip()


    return (id, tiles)


if __name__ == '__main__':
    id = 0
    tiles = [Tile(id)]

    with open("input_test2.txt", "r") as inFile:
        for line in inFile:
            (id, tiles) = processLine(line, tiles, id)

    count_black_tiles = 0
    for tile in tiles:
        if tile.color == 'black':
            count_black_tiles += 1


    print("{} of {} tiles".format(count_black_tiles, len(tiles)))
    for tile in tiles:
        tile.print()