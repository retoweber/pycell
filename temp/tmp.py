import dill as pickle
import numpy as np
from main import Cell, SpreadSheet


def this_exec(function: str, C: Cell, S: SpreadSheet):
    exec(f"global res; res = {function}")
    return res


def fun_0_0(C: Cell, S: SpreadSheet):
    a = 5
    return a


def fun_1_0(C: Cell, S: SpreadSheet):
    return 1


def fun_1_1(C: Cell, S: SpreadSheet):
    return 2


def fun_1_2(C: Cell, S: SpreadSheet):
    return 3


def fun_1_3(C: Cell, S: SpreadSheet):
    return 4


def fun_1_4(C: Cell, S: SpreadSheet):
    return 5


def fun_2_0(C: Cell, S: SpreadSheet):
    return sum(S[1, 0:5])


def fun_3_0(C: Cell, S: SpreadSheet):
    return lambda l: list(map(lambda x:x*x, l))


def fun_3_1(C: Cell, S: SpreadSheet):
    return S[3, 0](S[1, :])


def fun_4_0(C: Cell, S: SpreadSheet):
    return sum(C[-3, 1:4])


def fun_4_1(C: Cell, S: SpreadSheet):
    global a
    a = 6
    return 'asdf'


def fun_4_2(C: Cell, S: SpreadSheet):
    return a


