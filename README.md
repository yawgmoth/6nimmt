# 6 nimmt!

6 nimmt! is a card game where players simultaneously choose cards and then play them in ascending order according to simple rules. Whoever plays the sixth card in a row has to take that row, which scores against them. While playing the game two questions came up:
 - Is playing randomly a viable/competitive strategy?
 - What happens when the parameters of the game (number of rows, starting cards in hand, which cards are in the game) are changed?
 
To answer these questions, I wrote this simple python implementation of the game. As it turns out, it is very easy to write an AI that beats a random player, and it does that across several different parameter settings. 

# Requirements

 - Python 2.7

# Usage

usage: main.py [-h] [-c--starting-cards STARTING_CARDS]
               [-m--max-card MAX_CARD] [-r--rows ROWS] [-t--takes TAKES]
               [-q--quiet] [-n--iterations ITERATIONS] [-p--players PLAYERS]

An (parameterized) implementation of 6 nimmt.

optional arguments:
  -h, --help              show this help message and exit
  -c, --starting-cards STARTING_CARDS
                          defines how many cards players start with (default: 10)
  -m, --max-card MAX_CARD
                          defines what the highest card in the game is (default: 104)
  -r, --rows ROWS         defines how many rows there are in the game (default: 4)
  -t, --takes TAKES       defines which card takes a row (default: 6)
  -q, --quiet             turn off output except for the summary
  -n, --iterations ITERATIONS
                          how many times the game should run
  -p, --players PLAYERS   define how may and which player types should play.
                          Currently available types are: 
                          R: Random player 
                          G: Greedy player (plays card with minimum distance to board rows) 
                          S: Shortest row player (plays card that fit in the shortest row on the board) 
                          H: Human player (asks user for input) 
                        
                          For any AI player, an "M" can be appended to make that player minimize the scores of
                          rows they have to take when they play the lowest card.
                          The players should be separated by comma. (default: "R,R,R,R,R", i.e. 5 random players)