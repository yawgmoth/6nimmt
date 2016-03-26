import random


def get_value(card):
    if card % 55 == 0:
        return 7
    if card % 11 == 0:
        return 5
    if card % 10 == 0:
        return 3
    if card % 5 == 0:
        return 2
    return 1

class Player(object):
    def __init__(self):
        self.cards = []
        self.tricks = []
    def get_score(self):
        return sum(map(get_value, self.tricks))
    def choose_card(self, board):
        choice = None
        while choice not in self.cards:
            choice = self.make_choice(board)
        self.cards.remove(choice)
        return choice
   
    def make_choice(self, board):
        return random.choice(self.cards)
    def ask_which(self, board, card):
        return random.randint(0, len(board)-1)
        
class MinimizeTakenPointsMixin(object):
    def ask_which(self, board, card):
        min = -1 
        result = 0
        for i, row in enumerate(board):
            score = sum(map(get_value, row))
            if score < min or min < 0:
                min = score
                result = i
        return result
        

class GreedyPlayer(Player):
    def make_choice(self, board):
        min = -1
        minc = 0
        for c in self.cards:
            d = -1
            for row in board:
                if row[-1] < c and (c - row[-1] < d or d < 0):
                    d = c - row[-1]
            if d < min or min < 0:
                min = d
                minc = c
        return minc

class ShortestRowPlayer(Player):
    def make_choice(self, board):
        min = -1
        minc = 0
        for c in self.cards:
            d = -1
            l = 100000
            for row in board:
                if row[-1] < c and (c - row[-1] < d or d < 0):
                    d = c - row[-1]
                    l = len(row)
            if l < min or min < 0:
                min = l
                minc = c
        return minc
        
class HumanPlayer(Player):
    def make_choice(self, board):
        print "which card to you want to play?"
        print self.cards
        x = raw_input()
        return int(x)
    def ask_which(self, board, card):
        print "which row do you want to take for playing", card
        x = raw_input()
        return int(x)-1
        
def make_min_player(which):
    class MinPlayer(MinimizeTakenPointsMixin, which):
        pass
    return MinPlayer
    
PLAYER_TYPES = {"R": Player, "G": GreedyPlayer, "S": ShortestRowPlayer, "H": HumanPlayer}
