"""
	Christina Trotter
	5/27/19
	Python 3.6.2
"""

from player import Player 
from random import choice
CHS,COLS,MAX_FLIPS,ROWS = [1,2,3,4],7,4,6

class RandomPlayer(Player):
    def __init__(self, name, value):
        Player.__init__(self, name, value)     

    def make_move(self,board):
        if self.flips['me'] == 0: 
            self.drop(board)
            return
        
        ch = choice(CHS)
        while ch == CHS[2] or ch == CHS[3] and board.last_flipped:
            ch = choice(CHS)

        while ch == CHS[3] and self.flips['me'] == 1:
            ch = choice(CHS)
        
        if ch == CHS[0]:
            self.drop(board)
        elif ch == CHS[1]:
            self.drop(board)
            self.flip(board)
        elif ch == CHS[2]:
            self.flip(board)
            self.drop(board)
        else:
            self.flip(board)
            self.drop(board)
            self.flip(board)

    def drop(self,board):
        col = -1
        while not board.drop(self.value,col)[0]:
            col = choice(range(COLS))
        print('{0} dropped a disc in column {1}'.format(self.name,col+1))

