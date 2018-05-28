"""
	Christina Trotter
	5/27/19
	Python 3.6.2
    Notes: run this file to play game
"""

import sys, traceback, check as ch
from ai import AI
from player import Player
from rand import RandomPlayer
from ab import AlphaBeta
from board import Board

VALUE,MAX_GAMES = 1,10

class Game():
    def __init__(self):
        self.board = Board()
        self.brain = AlphaBeta()
        self.players = []
        self.players.append(AI("Arya",VALUE))
        self.players.append(Player("You",-VALUE))

    def play(self,current):
        self.board.print_board()
        while True:
            self.players[current].make_move(self.board)
            self.board.print_board()
            if ch.game_over(self.board.current,self.players[current].value):
                self.get_final(current)
                break
            print("flips left ({0}) = {1}\n".format(self.players[current].name,self.players[current].flips['me']))
            current = abs(current - 1)
            self.players[0].flips['op'] = self.players[1].flips['me']
            self.players[1].flips['op'] = self.players[0].flips['me']
        self.board.reset_board()
        for p in self.players:
            p.reset()

    def get_final(self,current):
        result = self.brain.get_function(self.board,self.players[current].value)
        if result >= ch.WIN or result == ch.TIE:
            print("{0} won!".format(self.players[current].name))
            self.players[current].stats['wins'] += 1
            self.players[abs(current - 1)].stats['loses'] += 1
        elif result <= ch.LOSE:
            print("{0} won!".format(self.players[abs(current - 1)].name))
            self.players[abs(current - 1)].stats['wins'] += 1
            self.players[current].stats['loses'] += 1
        else:
            print("it's a tie!")
            self.players[abs(current - 1)].stats['ties'] += 1
            self.players[current].stats['ties']  += 1

 
if __name__ == '__main__':
    try:
        answer, current = '',0
        game = Game()
        while answer not in ['Y','y','N','n']:
            answer = input('Do you want to go first?\n[Y]/[N]\nanswer: ')
        if answer in ['Y','y']:
            current = 1
        for i in range(MAX_GAMES):
            print('game: {0}'.format(i+1))
            game.players[current].first = True
            game.play(current)
            current = abs(current - 1)
        print('\nstats:\n\ngames played: {4}\n\nplayer 1: {0}\n\n{2}\n\nplayer 2: {1}\n\n{3}\n\n'.format(game.players[0].name,game.players[1].name,game.players[0].stats,game.players[1].stats,MAX_GAMES))
    except Exception as e:
        print(str(e))
        _, _, tb = sys.exc_info()
        print(traceback.format_list(traceback.extract_tb(tb)[-1:])[-1])