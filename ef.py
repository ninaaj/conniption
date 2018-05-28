"""
	Christina Trotter
	5/27/19
	Python 3.6.2
"""

import copy as cp, check as ch, numpy as np
COLS,EMPTY,LOSE,ROWS,TIE,WIN = 7,0,-100000,6,0,100000
class EvaluationFunction(object):
    def __init__(self):
        self.id_board = None
        self.solutions = []
        self.solution_map = None
        self.populate()
        self.get_solutions()
    
    def populate(self):
        self.id_board = np.zeros((ROWS*COLS,), dtype=int).reshape(ROWS,COLS)
        
        for i in range(ROWS):
            for j in range(COLS):
                self.id_board[i,j] = str(i) + str(j)

        self.solution_map = np.array([[3,4,5,7,5,4,3],[4,6,8,10,8,6,4],[5,8,11,13,11,8,5],[5,8,11,13,11,8,5],[4,6,8,10,8,6,4],[3,4,5,7,5,4,3]], np.int32)
        
    def get_solutions(self):
        units = [self.id_board[:,i].tolist() for i in range(COLS)]
        units.extend([self.id_board[::-1,:].diagonal(i) for i in range(-self.id_board.shape[0]+1,self.id_board.shape[1])])
        units.extend(self.id_board.diagonal(i) for i in range(self.id_board.shape[1]-1,-self.id_board.shape[0],-1))
        units.extend([self.id_board[i,:].tolist() for i in range(ROWS)])

        for u in units:
            if len(u) < 4:
                continue
            if len(u) == 4:
                self.solutions.append(list(u))
                continue
            i = len(u) - 4
            self.solutions.append(list(u[:-i]))
            self.solutions.append(list(u[i:]))
            if i > 1:
                self.solutions.append(list(u[1:-(i-1)]))
            if i > 2:
                self.solutions.append(list(u[(i-1):-1]))
    
    def get_heuristic_value(self,board,value):
        me, mev = self.heuristic_helper(board,value)
        op, opv = self.heuristic_helper(board,-value)
        if me[4] > 0 and op[4] > 0:
            return TIE
        if me[4] > 0:
            return WIN + mev 
        if op[4] > 0:
            return - (WIN + opv) 
        return (mev + ((100 * me[3]) + (10 * me[2]) + (me[1]))) -  (opv + ((100 * op[3]) + (10 * op[2]) + (op[1])))
    
    def heuristic_helper(self,board,value):
        sum_lines = {4:0,3:0,2:0,1:0}
        sum_values = 0
        visited = []
        for i in range(ROWS):
            for j in range(COLS):
                if board[i,j] == value:
                    l,r,visited = self.evaluate_disc(board,[i,j],board[i,j],visited)
                    sum_values += r
                    for k,v in l.items():
                        sum_lines[k] += v
        return sum_lines, sum_values

    def evaluate_disc(self,board,index,value,visited):
        remaining_sols, max_sols, count = 0, self.solution_map[index[0],index[1]], 0
        lines = {4:0,3:0,2:0,1:0}
        for s in self.solutions:
            if count == max_sols:
                break
            if int(str(index[0]) + str(index[1])) in s:
                count += 1
                if s in visited:
                    continue
                visited.append(s)
                n,r = self.check_solution(board, s, value)
                remaining_sols += r
                if n:
                    lines[n] += 1 
        return lines, remaining_sols, visited

    def check_solution(self, board, solution, value):
        num = 0
        for s in solution:
            index = [int(i) for i in str(s)]
            if len(index) == 1:
                index.insert(0,0)
            if board[index[0],index[1]] == -value:
                return 0,0
            if board[index[0],index[1]] == value:
                num += 1
            if num > 3:
                return num, 10 * num
        return num, 1 * num

    def game_over(self,board,row,col,value,flipped):
        if not flipped:
            return self.helper(board,row,col,value)[0]
        results = [False,[]]
        for i in range(row+1):
            results = self.helper(board,i,col,value,results[1])
            if results[0]:
                return True 
        return False

    def helper(self,board,row,col,value,visited=[]):
        count,max_sols = 0, self.solution_map[row,col]
        for s in self.solutions:
            if count == max_sols:
                break
            if int(str(row) + str(col)) in s:
                count += 1
                if s in visited:
                    continue
                if self.helper_helper(board, s, value):
                    return [True, None]
                visited.append(s)
        return [False, visited]
    
    def helper_helper(self,board,solution,value):
        for s in solution:
            index = [int(i) for i in str(s)]
            if len(index) == 1:
                index.insert(0,0)
            if board[index[0],index[1]] == -value or board[index[0],index[1]] == EMPTY:
                return False
        return True