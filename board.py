"""
	Christina Trotter
	5/27/19
	Python 3.6.2
"""

import copy as cp, check as ch, numpy as np

AI,COLS,EMPTY,PL,ROWS = 1,7,0,-1,6
class Board():
    def __init__(self): 
        self.current = self.get_new_board() 
        self.last_flipped = False

    def get_new_board(self):
        return np.zeros((ROWS*COLS,), dtype=int).reshape(ROWS,COLS)

    def flip(self):
        temp = self.get_new_board()
        for i in range(ROWS):
            for j in range(COLS):
                if self.current[i,j] != EMPTY:
                    temp = self.flip_helper(temp,self.current[i,j],j)
        self.current = np.copy(temp)
        self.last_flipped = True
        return

    def flip_helper(self, board, value, col):
        a = 1
        while board[ROWS - a,col] != EMPTY:
            a += 1
        board[ROWS - a,col] = value
        return board

    def drop(self, value, col):
        if col not in range(COLS) or not self.can_drop(col):
            return [False,-1] 
        a = 1
        while self.current[ROWS - a,col] != EMPTY:
            a += 1
        self.current[ROWS - a,col] = value
        self.last_flipped = False
        return [True,ROWS - a]
    
    def can_drop(self, col):
        return self.current[0,col] == EMPTY

    def more_moves(self):
        for i in range(COLS):
            if self.can_drop(i):
                return True
        return False

    def print_board(self):
        A, E, P = 'B',' ','W'
        print("\n")
        for i in range(ROWS):
            for j in range(COLS):
                if self.current[i,j] == EMPTY:
                    print('[{0}]'.format(E), end="", flush=True)
                elif self.current[i,j] == AI:
                    print('[{0}]'.format(A), end="", flush=True)
                elif self.current[i,j] == PL:
                    print('[{0}]'.format(P), end="", flush=True)
            print()
        for i in range(COLS):
            print(" {0} ".format(i+1), end="", flush=True)
        print("\n")
        return
    
    def get_copy(self):
        return {'current':np.copy(self.current),'last_flipped':cp.copy(self.last_flipped)}

    def reset_board(self):
        self.current = self.get_new_board()
        self.last_flipped = False

    