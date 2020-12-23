import collections

class Player:

    def __init__(self, name):
        self.name = name
        self.deck = []

    def add(self, cards):
        self.deck += cards

    def nbr_of_cards(self):
        return len(self.deck)

    def pop_card(self):
        return self.deck.pop(0)

    def __str__(self):
        return "{}: {}".format(self.name, self.deck)


def check_winner(players, maxcards):
    for player in players:
        if player.nbr_of_cards() == max_cards:
            return player
    return None


if __name__ == '__main__':
    with open("input.txt", "r") as inFile:
        players = []
        idx = -1
        for line in inFile:
            if line.strip().isnumeric():
                players[idx].add([int(line.rstrip('\n'))])
            if line == '\n':
                continue
            if line.startswith('Player'):
                players.append(Player(line.rstrip('\n').rstrip(':')))
                idx += 1
        inFile.close()

    max_cards = 0
    for player in players:
        max_cards += player.nbr_of_cards()

    for player in players:
        print(player)

    turns = 0;
    winner = players[0]
    while winner.nbr_of_cards() != max_cards:
        game_list = {}
        for player in players:
            game_list[player.pop_card()] = player
        ordered_game_list = collections.OrderedDict(sorted(game_list.items(), reverse=True))

        winner = ordered_game_list[next(iter(ordered_game_list))]
        winner.add(ordered_game_list.keys())
        turns += 1

    print(turns)
    print(winner.deck)
    result = 0
    for i in range(len(winner.deck)):
        result += winner.deck[i] * (len(winner.deck) - i)
    print(result)