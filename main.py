import random
from common import *
import argparse
    

class Game(object):
    def __init__(self, players, max_card=104, starting_cards=10, rows=4, takes=6, output=True):
        self.players = players
        self.max_card = max_card
        self.starting_cards = starting_cards
        self.rows = rows
        self.takes = takes
        self.output = output
    def deal(self):
        cards = range(1, self.max_card+1)
        random.shuffle(cards) # TODO: random.shuffle can't generate all possible permutations
        for p in self.players:
            p.cards = cards[:self.starting_cards]
            del cards[:self.starting_cards]
        self.board = []
        for r in xrange(self.rows):
            self.board.append([cards[0]])
            del cards[0]
    
    def print_board(self):
        print "\n\nBoard:"
        for row in self.board:
            for c in row:
                print "%5d"%c,
            print
            
    def turn(self):
        if self.output:
            self.print_board()
    
        cards = [(i,p.choose_card(self.board)) for i,p in enumerate(self.players)]
        
        cards.sort(key=lambda (i,c): c)
        if self.output:
            print "chosen cards: ", " ".join(map(lambda (i,c): "%d (Player %d)"%(c,i), cards))
        for (i,c) in cards:
            self.place_card(i,c)
            
    def place_card(self, player, card):
        if self.output:
            print "player", player, "plays", card
        where = -1
        distance = self.max_card
        for i,row in enumerate(self.board):
            if card > row[-1] and (card - row[-1]) < distance:
                where = i
                distance = card - row[-1]
        if where < 0:
            which = self.players[player].ask_which(self.board, card)
            if self.output:
                print " ", card, "is lower than anything on the board. Player takes row", which+1, "(", self.board[which], ")"
            self.players[player].tricks.extend(self.board[which])
            self.board[which] = [card]
        elif len(self.board[where]) < self.takes-1:
            if self.output:
                print " ", card, "is added to row", where+1, "(", self.board[where], ")"
            self.board[where].append(card)
        else:
            if self.output:
                print " ", card, "TAKES row", where+1, "(", self.board[where], ") for", sum(map(get_value, self.board[where])), "points"
            self.players[player].tricks.extend(self.board[where])
            self.board[where] = [card]
    def run(self):
        self.deal()
        for i in xrange(self.starting_cards):
            self.turn()
        return [p.get_score() for p in self.players]
        
def main(playerdef="R,R,G,S,SM", max_card=104, starting_cards=10, rows=4, takes=6, output=True, iterations=1):
    if iterations > 1:
        results = {}
        ptypes = []
        presults = []
        for p in playerdef.split(","):
            p = p.strip()
            results[p] = (0,0)
            presults.append((0,0))
            ptypes.append(p)

    for i in xrange(iterations):
    
        players = []
        for p in ptypes:
            pclass = PLAYER_TYPES[p[0]]
            if len(p) > 1 and p[1] == "M":
                pclass = make_min_player(pclass)
            players.append(pclass())
        
        g = Game(players, max_card=max_card, starting_cards=starting_cards, rows=rows, takes=takes, output=output)
        
        result = g.run()
        print result
        if iterations > 1:
            for i,s in enumerate(result):
                (olds,n) = presults[i]
                presults[i] = (olds+s,n+1)
                (olds,n) = results[ptypes[i]]
                results[ptypes[i]] = (olds+s, n+1)
    if iterations > 1:
        print "Summary"
        for t in results:
            print t, "scored an average of", results[t][0]*1.0/results[t][1]
        print "by player"
        for i,p in enumerate(presults):
            print "Player", i, "scored an average of", p[0]*1.0/p[1]
                


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='An (parameterized) implementation of 6 nimmt.')
    parser.add_argument('-c', '--starting-cards', dest='starting_cards', action='store', type=int, default=10,
                       help='defines how many cards players start with (default: 10)')
    parser.add_argument('-m', '--max-card', dest='max_card', action='store', type=int, default=104,
                       help='defines what the highest card in the game is (default: 104)')
    parser.add_argument('-r', '--rows', dest='rows', action='store', type=int, default=4,
                       help='defines how many rows there are in the game (default: 4)')
    parser.add_argument('-t', '--takes', dest='takes', action='store', type=int, default=6,
                       help='defines which card takes a row (default: 6)')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_false', default=True,
                       help='turn off output except for the summary (default: True)')
    parser.add_argument('-n', '--iterations', dest='iterations', action='store', type=int, default=1,
                       help='how many times the game should run (default: 1)')
    parser.add_argument('-p', '--players', dest='players', action='store', default="R,R,R,R,R",
                       help="""define how may and which player types should play. Currently available types are:
    R: Random player
    G: Greedy player (plays card with minimum distance to board rows)
    S: Shortest row player (plays card that fit in the shortest row on the board)
    H: Human player (asks user for input)
    
For any AI player, an "M" can be appended to make that player minimize the scores of rows they have to take when they play the lowest card. The players should be separated by comma. (default: "R,R,R,R,R", i.e. 5 random players)""")

    args = parser.parse_args()
    
    main(args.players, args.max_card, args.starting_cards, args.rows, args.takes, args.quiet, args.iterations)
