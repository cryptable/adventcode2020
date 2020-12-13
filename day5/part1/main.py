NBR_ROWS = 128
NBR_SEATS = 8


def processSeat(qeats, ticket):
    r1 = NBR_ROWS
    r2 = NBR_SEATS
    row = 0
    seat = 0
    for i in range(0,7):
        r1 = r1/2
        if ticket[i] == 'B':
            row += r1
    for i in range(7,10):
        r2 = r2/2
        if ticket[i] == 'R':
            seat += r2
    print("Row: {}, Seat {}, ID {}".format(row, seat, (row*8 + seat)))
    seats[int(row)][int(seat)] = 'X'

    return int(row*8 + seat)


def findEmptySeat(qeats):
    nbr_found = 0;
    ids_found = ['.', '.', '.']
    for r in range(0, NBR_ROWS):
        for s in range(0, NBR_SEATS):
            ids_found[0] = ids_found[1]
            ids_found[1] = ids_found[2]
            ids_found[2] = seats[r][s]
            if ''.join(ids_found) == 'X.X':
                print("Row: {}, Seat {}, ID {}".format(int((r*8 + s - 1)/8), int((r*8 + s - 1)%8), (r*8 + s - 1)))


if __name__ == '__main__':
    seats = []
    row = []
    for i in range(0, NBR_ROWS):
        row = []
        for j in range(0, NBR_SEATS):
            row.append('.')
        seats.append(row)

    highest = 0
    with open("./input.txt", "r") as infile:
        value = infile.readline()
        while value != '':
            seatnr = processSeat(seats, value)
            if seatnr > highest:
                highest = seatnr
            value = infile.readline()

        infile.close()

    print("Highest nr: {}".format(highest))

    findEmptySeat(seats)

