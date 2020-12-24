import collections
import copy

class Player:

    def __init__(self, name, cards=[]):
        self.name = name
        self.deck = cards

    def add(self, cards):
        self.deck += cards

    def nbr_of_cards(self):
        return len(self.deck)

    def pop_card(self):
        return self.deck.pop(0)

    def __str__(self):
        return "{}: {}".format(self.name, self.deck)


players_history = []


def store_in_previous_games(history, player1, player2, level):
    history.append((copy.deepcopy(player1), copy.deepcopy(player2), level))


def check_same_previous_decks(history, player1, player2, level):
    for chk_player in history:
        if chk_player[2] == level and chk_player[0].deck == player1.deck and chk_player[1].deck == player2.deck:
            print("Found previoud history")
            return True
    return False


def play_game(player1, player2, level):
    max_cards = player1.nbr_of_cards()
    max_cards += player2.nbr_of_cards()
    players_history = []

    turns = 0;
    winner = player1
    while winner.nbr_of_cards() != max_cards:
#        print("Game: {}".format(turns))
#        print("------------")
        if check_same_previous_decks(players_history, player1, player2, level):
            print("Found duplicate {}:{}".format(level, turns))
            return player1
        store_in_previous_games(players_history, player1, player2, level)
#        print("Player 1 cards: {}".format(player1.deck))
#        print("Player 2 cards: {}".format(player2.deck))
        card_player1 = player1.pop_card()
        card_player2 = player2.pop_card()
#        print("Player 1 takes: {}".format(card_player1))
#        print("Player 2 tabes: {}".format(card_player2))
        if card_player1 <= player1.nbr_of_cards() and card_player2 <= player2.nbr_of_cards():
            new_player1 = Player(player1.name, player1.deck[:card_player1])
            new_player2 = Player(player2.name, player2.deck[:card_player2])
#            print("Start Sub Game in game {}".format(turns))
            winner = play_game(new_player1, new_player2, level+1)
            if winner.name == player1.name:
#                print("Player 1 wins sub-game!")
                player1.add([card_player1, card_player2])
                winner = player1
            else:
#                print("Player 2 wins sub-game!")
                player2.add([card_player2, card_player1])
                winner = player2
        else:
            if card_player1 > card_player2:
#                print("Player 1 wins!")
                player1.add([card_player1, card_player2])
                winner = player1
            else:
 #               print("Player 2 wins!")
                player2.add([card_player2, card_player1])
                winner = player2
        turns += 1
#    print(turns)

    return winner


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
                players.append(Player(line.rstrip('\n').rstrip(':'), []))
                idx += 1
        inFile.close()

    winner = play_game(players[0], players[1], 0)

    print(winner.deck)
    result = 0
    for i in range(len(winner.deck)):
        result += winner.deck[i] * (len(winner.deck) - i)
    print(result)