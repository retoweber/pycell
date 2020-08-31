import dill as pickle
import numpy as np
from main import Cell, SpreadSheet


def this_exec(function: str, cell: Cell, sh: SpreadSheet):
    exec(f"global res; res = {function}")
    return res


def fun_1_0(cell: Cell, sh: SpreadSheet):    
    return 1


def fun_1_1(cell: Cell, sh: SpreadSheet):    
    return 2


def fun_1_2(cell: Cell, sh: SpreadSheet):    
    return 3


def fun_1_3(cell: Cell, sh: SpreadSheet):    
    return 4


def fun_1_4(cell: Cell, sh: SpreadSheet):    
    return 5


def fun_2_0(cell: Cell, sh: SpreadSheet):    
    return sum(sh[1,0:5])


def fun_3_0(cell: Cell, sh: SpreadSheet):    
    return lambda l:list(map(lambda x:x*x, l))


def fun_3_1(cell: Cell, sh: SpreadSheet):    
    return sh[3,0](sh[1,:])


def fun_4_0(cell: Cell, sh: SpreadSheet):    
    return sum(cell[-3,1:4])


