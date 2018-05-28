"""
	Christina Trotter
	5/27/19
	Python 3.6.2
"""

import numpy as np
COLS,LOSE,ROWS,TIE,WIN= 7,-100000,6,0,100000

def game_over(board,value):
    if check(board,value,4) > 0 or check(board,-value,4) > 0:
        return True

def check(board,value,length):
    return check_cols(board,value,length) + check_diags(board,value,length) + check_rows(board,value,length)

def check_cols(b,v,l):
    cols = [b[:,i].tolist() for i in range(COLS)]
    return sum([unit_check(c,v,l) for c in cols])

def check_diags(b,v,l):
    diags = [b[::-1,:].diagonal(i) for i in range(-b.shape[0]+1,b.shape[1])]
    diags.extend(b.diagonal(i) for i in range(b.shape[1]-1,-b.shape[0],-1))
    return sum([unit_check(d,v,l) for d in diags])

def check_rows(b,v,l):
    rows = [b[i,:].tolist() for i in range(ROWS)]
    return sum([unit_check(r,v,l) for r in rows])

def unit_check(unit,value,length):  
    lines,i = 0,0
    if value not in unit or len(unit) < length:
        return 0
    for u in unit:
        if u != value:
            if i == length:
                lines += 1
            i = 0
            continue
        i+=1
    if i == length:
        lines += 1
    elif length == 4 and i > 4:
        lines +=1
    return lines
