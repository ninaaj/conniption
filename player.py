"""
	Christina Trotter
	5/27/19
	Python 3.6.2
"""

CHS,MAX_FLIPS = [1,2,3,4],4

class Player():
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.flips = {'me':MAX_FLIPS,'op':MAX_FLIPS}
        self.stats = {'wins':0,'ties':0,'loses':0}
        self.first = False
        self.discs = 0
        
    def reset(self):
        self.flips = {'me':MAX_FLIPS,'op':MAX_FLIPS}
        self.first = False
        self.discs = 0
               
    def make_move(self,board):
        if self.flips['me'] == 0:
            self.drop(board)
            return
        ch = -1
        while int(ch) not in CHS:
            ch = input('make a move\n[1] DROP\n[2] DROP -> FLIP\n[3] FLIP -> DROP\n[4] FLIP -> DROP -> FLIP\nCHOICE: ')
        
        while int(ch) not in CHS or ((int(ch) == CHS[2] or int(ch) == CHS[3]) and board.last_flipped):
            ch = input('the board cannot be flipped back to back\nmake a move\n[1] DROP\n[2] DROP -> FLIP\nCHOICE: ')

        while int(ch) not in CHS or (int(ch) == CHS[3] and self.flips['me'] == 1):
            ch = input('you do not have enough flips left\nmake a move\n[1] DROP\n[2] DROP -> FLIP\n[3] FLIP -> DROP\nCHOICE: ')
        
        if int(ch) == CHS[0]:
            self.drop(board)
        elif int(ch) == CHS[1]:
            self.drop(board)
            self.flip(board)
        elif int(ch) == CHS[2]:
            self.flip(board)
            self.drop(board)
        else:
            self.flip(board)
            self.drop(board)
            self.flip(board)

    def drop(self,board):
        col = -1
        while not board.drop(self.value,int(col)-1)[0]:
            col = input('pick a column\nenter [1 - 7]: ')
        print('{0} dropped a disc in column {1}'.format(self.name,col))

    def flip(self,board):
        board.flip()
        print('{0} flipped the board'.format(self.name))
        self.flips['me'] -= 1
    
          
