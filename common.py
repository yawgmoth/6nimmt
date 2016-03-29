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
    def __init__(self, max_card=104, starting_cards=10, rows=4, takes=6):
        self.max_card = max_card
        self.starting_cards = starting_cards
        self.rows = rows
        self.takes = takes
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
    
def make_opportunistic_player(which):
    class OpportunisticPlayer(Player):
        def __init__(self, max_card=6, starting_cards=104, rows=4, takes=6):
            self.inner = which(max_card=max_card, starting_cards=starting_cards, rows=rows, takes=takes)
            super(OpportunisticPlayer, self).__init__(max_card=max_card, starting_cards=starting_cards, rows=rows, takes=takes)
        def make_choice(self, board):
            for b in board:
                if sum(map(get_value, b)) <= 1:
                    c = min(self.cards)
                    bmin = min(map(lambda r: r[-1], board))
                    if c < bmin:
                        return c
            self.inner.cards = self.cards
            self.inner.tricks = self.tricks
            return self.inner.make_choice(board)
        def ask_which(self, board, card):
            self.inner.cards = self.cards
            self.inner.tricks = self.tricks
            return self.inner.ask_which(board, card)
    return OpportunisticPlayer
    
PLAYER_TYPES = {"R": Player, "G": GreedyPlayer, "S": ShortestRowPlayer, "H": HumanPlayer}
MIXINS = {"M": make_min_player, "O": make_opportunistic_player}