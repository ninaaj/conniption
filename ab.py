"""
	Christina Trotter
	5/27/19
	Python 3.6.2
"""
import check as ch, copy as cp
from operator import itemgetter 
from board import Board
from ef import EvaluationFunction
from random import choice
COLS,ROWS, = 7,6

class AlphaBeta():
    def __init__(self):
        self.ef = EvaluationFunction()
        self.nodes = 0
            
    def best_move(self, depth, board, player_value, player_flips, opp_flips):
        self.nodes = 0
        alpha, beta, legal_moves = float('-inf'), float('inf'), {}
        
        for col in range(COLS):
            if board.can_drop(col):
                drop = self.make_move(board, player_value, col)
                legal_moves[col] = self.min(alpha, beta, depth-1, drop['board'],drop['row'],col, -player_value, opp_flips, player_flips, flipped=False)
                if player_flips > 0:
                    drop_flip = self.make_move(board, player_value, col, after=True, before=False)
                    legal_moves[str(col) + ',F'] = self.min(alpha, beta, depth-1, drop_flip['board'],drop_flip['row'],col, -player_value, opp_flips, player_flips-1,flipped=True)
                    if not board.last_flipped:
                        flip_drop = self.make_move(board, player_value, col, after=False, before=True)
                        legal_moves['F,' + str(col)] = self.min(alpha, beta, depth-1, flip_drop['board'],flip_drop['row'],col, -player_value, opp_flips, player_flips-1, flipped=True)
                        if player_flips > 1:
                            flip_drop_flip = self.make_move(board, player_value, col, after=True, before=True)
                            legal_moves['F,' + str(col) + ',F'] = self.min(alpha, beta, depth-1, flip_drop_flip['board'],flip_drop_flip['row'],col, -player_value, opp_flips, player_flips-2, flipped=True)
        moves = sorted(legal_moves.items(),key = itemgetter(1),reverse = True)
        
        basic_moves, best_moves = [],[]
    
        for m in moves:
            if m[1] != moves[0][1]:
                break
            best_moves.append(m)

        if len(best_moves) == 1:
            return best_moves[0]

        for m in best_moves:
            if type(m[0]) is int:
                basic_moves.append(m)
            
        if len(basic_moves) > 0:
            picks = basic_moves
        else:
            temp = []
            for m in best_moves:
                if len(m[0].split(',')) > 2:
                    temp.append(m)
                    best_moves.remove(m)
            if len(best_moves) > 0:
                picks = best_moves
            else:
                picks = temp
        
        return choice(picks)
        
    def max(self, alpha, beta, depth, board, row, col, player_value, player_flips, opp_flips, flipped):
        legal_moves = self.get_moves(board,player_value, player_flips)
        
        if depth <= 0 or len(legal_moves) == 0 or self.game_over(board,row, col, player_value, flipped):
            return self.get_function(board, player_value)
        
        
        value = float('-inf')
        for move in legal_moves:
              value = max(value, self.min(alpha, beta, depth-1, move[0]['board'], move[0]['row'], move[0]['col'], -player_value, opp_flips, move[1], move[2]))
              if value >= beta:
                  return value
              alpha = max(alpha, value)
        return value

    def min(self, alpha, beta, depth, board, row, col, player_value, player_flips, opp_flips, flipped):
        legal_moves = self.get_moves(board,player_value, player_flips)
        
        if depth <= 0 or len(legal_moves) == 0 or self.game_over(board, row, col, player_value, flipped):
            return -self.get_function(board, player_value)
        
        value = float('inf')
        for move in legal_moves:
              value = min(value, self.max(alpha, beta, depth-1, move[0]['board'], move[0]['row'], move[0]['col'], -player_value, opp_flips, move[1], move[2]))  
              if value <= alpha:
                  return value
              beta = min(beta, value)
        return value

    def game_over(self, board, row, col, value, flipped):
        if self.ef.game_over(board.current, row, col, value, flipped) or not board.more_moves():
            return True
        return False
        
    
    def make_move(self, board, player_value, col, after=False, before=False):
        temp = self.get_copy(board)
        if before:
            temp.flip()
        result = temp.drop(player_value,col)
        if after:
            temp.flip()
        return {'board':temp, 'row':result[1], 'col': col}
        
    def get_copy(self,board):
        temp = Board()
        vemp = board.get_copy()
        temp.current = vemp['current']
        temp.last_flipped = vemp['last_flipped']
        return temp

    def get_function(self, board, player_value):
        return self.ef.get_heuristic_value(board.current,player_value)

    def get_moves(self, board, player_value, player_flips):
        legal_moves = []
        for i in range(COLS):
            if board.can_drop(i):
                drop = [self.make_move(board, player_value, i), player_flips, False]
                legal_moves.append(drop)
                if player_flips > 0:
                    drop_flip = [self.make_move(board, player_value, i, after=True, before=False), player_flips-1, True]
                    legal_moves.append(drop_flip)
                    if not board.last_flipped:
                        flip_drop = [self.make_move(board, player_value, i, after=False, before=True), player_flips-1, True]    
                        legal_moves.append(flip_drop)
                        if player_flips > 1:
                            flip_drop_flip = [self.make_move(board, player_value, i, after=True, before=True), player_flips-2, True]
                            legal_moves.append(flip_drop_flip)
        return legal_moves
 

