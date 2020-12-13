import copy


def printSeatMap(seat_map):
    for row in seat_map:
        line=''
        for seat in row:
            line += seat
        print(line)


def countOccupiedSeats(seat_map):
    nbr = 0
    for row in seat_map:
        for seat in row:
            if seat == '#':
                nbr += 1
    return nbr


def sitDownRule(seatmap, row, seat):
    score = 1 if seeOccupiedSeat(seatmap, row, seat, -1, -1) else 0
    score += 1 if seeOccupiedSeat(seatmap, row, seat, -1, 0) else 0
    score += 1 if seeOccupiedSeat(seatmap, row, seat, -1, 1) else 0
    score += 1 if seeOccupiedSeat(seatmap, row, seat, 0, -1) else 0

    score += 1 if seeOccupiedSeat(seatmap, row, seat, 0, 1) else 0
    score += 1 if seeOccupiedSeat(seatmap, row, seat, 1, -1) else 0
    score += 1 if seeOccupiedSeat(seatmap, row, seat, 1, 0) else 0
    score += 1 if seeOccupiedSeat(seatmap, row, seat, 1, 1) else 0

    if score == 0:
        return '#'

    return 'L'


def seeOccupiedSeat(seatmap, row, seat, dir_row, dir_seat):
    r = row + dir_row
    s = seat + dir_seat
    while (0 <= r < len(seatmap)) and (0 <= s < len(seatmap[0])):
        if seatmap[r][s] == 'L':
            return False
        if seatmap[r][s] == '#':
            return True
        r += dir_row
        s += dir_seat
    return False


def leaveSeatRule(seatmap, row, seat):
    score = 1 if seeOccupiedSeat(seatmap, row, seat, -1, -1) else 0
    score += 1 if seeOccupiedSeat(seatmap, row, seat, -1, 0) else 0
    score += 1 if seeOccupiedSeat(seatmap, row, seat, -1, 1) else 0
    score += 1 if seeOccupiedSeat(seatmap, row, seat, 0, -1) else 0

    score += 1 if seeOccupiedSeat(seatmap, row, seat, 0, 1) else 0
    score += 1 if seeOccupiedSeat(seatmap, row, seat, 1, -1) else 0
    score += 1 if seeOccupiedSeat(seatmap, row, seat, 1, 0) else 0
    score += 1 if seeOccupiedSeat(seatmap, row, seat, 1, 1) else 0

    if score >= 5:
        return 'L'

    return '#'


def processSeatMap(seat_map):
    new_seat_map = copy.deepcopy(seat_map)
    for row in range(1, len(seat_map)-1):
        for seat in range(1, len(seat_map[row])-1):
            if seat_map[row][seat] == 'L':
                new_seat_map[row][seat] = sitDownRule(seat_map, row, seat)
            elif seat_map[row][seat] == '#':
                new_seat_map[row][seat] = leaveSeatRule(seat_map, row, seat)
            else:
                # '.'
                new_seat_map[row][seat] = seat_map[row][seat]
    return new_seat_map


def compareSeatMaps(seat_map1, seat_map2):
    for row in range(1, len(seat_map1)-1):
        for seat in range(1, len(seat_map1[row])-1):
            if seat_map1[row][seat] != seat_map2[row][seat]:
                return False
    return True


if __name__ == '__main__':
    seat_map = []
    with open("input.txt", "r") as infile:
        for line in infile:
            if seat_map == []:
                seat_map.append(['.']*(len(line.rstrip('\n')) + 2))
            seat_map.append(['.'] + list(line.rstrip('\n')) + ['.'])
    seat_map.append(['.'] * len(seat_map[0]))

    new_seat_map = processSeatMap(seat_map)

    while not compareSeatMaps(seat_map, new_seat_map):
        printSeatMap(seat_map)
        seat_map = new_seat_map
        new_seat_map = processSeatMap(seat_map)

    printSeatMap(seat_map)
    printSeatMap(new_seat_map)
    print(countOccupiedSeats(seat_map))
