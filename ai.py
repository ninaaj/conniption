"""
	Christina Trotter
	5/27/19
	Python 3.6.2
"""

from player import Player 
import check as ch
from ab import AlphaBeta
import time

COLS,FLIP,MAX_DEPTH,MAX_FLIPS,ROWS = 7,'F',3,4,6

class AI(Player):
    def __init__(self, name, value):
        Player.__init__(self, name, value)     
        self.brain = AlphaBeta()
        self.depth = 1

    def make_move(self,board):
        self.discs += 1
        if self.discs == 1 and self.first:
            board.drop(self.value,COLS//2)
            print('{0} dropped a disc in column {1}'.format(self.name,(COLS//2)+1))
            return
        
        t = time.time()
        move = self.brain.best_move(self.depth,board,self.value,self.flips['me'],self.flips['op'])
        while move[1] < ch.WIN and self.depth < MAX_DEPTH:
            self.depth += 1
            move = self.brain.best_move(self.depth,board,self.value,self.flips['me'],self.flips['op'])
        t = time.time() - t
        
        print('\n{0} took {1} seconds to make a move'.format(self.name,int(t)))
        
        if type(move[0]) is int:
            board.drop(self.value,move[0])
            print('{0} dropped a disc in column {1}'.format(self.name,move[0]+1))
            return
        
        move = move[0].split(',')
        for m in move:
            if m == FLIP:
                board.flip()
                print('{0} flipped the board'.format(self.name))
                self.flips['me'] -= 1
            else:
                board.drop(self.value,int(m[0]))
                print('{0} dropped a disc in column {1}'.format(self.name,int(m[0])+1))
    