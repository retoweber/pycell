import numpy as np
import dill as pickle
from functools import reduce
import importlib
import csv

with open('setup.py', 'r') as f:
    boilerplate = '\n'.join(f.readlines())+'\n'

boilerplate += """import dill as pickle
import numpy as np
from main import Cell, SpreadSheet


def this_exec(function: str, C: Cell, S: SpreadSheet):
    exec(f"global res; res = {function}")
    return res


"""


class SpreadSheet(object):
    def __init__(self, width=1024, height=1024):
        self.width = width
        self.height = height
        self.cells = np.array([[Cell(self, w, h) for w in range(width)] for h in range(height)])

    def __str__(self):
        def concat_cells(it1, it2):
            return it1 + ", " + it2

        def concat_rows(it1, it2):
            return it1 + ",\n" + it2

        return "[" + reduce(concat_rows,
                            map(lambda row: "[" + reduce(concat_cells, map(lambda cell: cell.__str__(), row)) + "]",
                                self.cells)) + "]"

    def __call__(self, *args, **kwargs):
        if len(args) >= 2:
            # assume x and y value
            y, x = args[:2]
            if len(args) == 2:  # get or execute
                return self.cells[y, x]()
            else:
                self.cells[y, x].descriptor = args[2]
                self.cells[y, x].__call__()

    def __getitem__(self, key):
        ret = self.cells[key]
        if isinstance(ret, Cell):
            return ret.value
        else:
            len_shape = len(ret.shape)
            if len_shape == 1:
                return np.array(list(map(lambda ele: ele.value, ret)))
            if len_shape == 2:
                return np.array(list([list(map(lambda ele: ele.value, row)) for row in self.cells[key]]))


class Cell:
    def __init__(self, this_spreadsheet: SpreadSheet, x: int, y: int, descriptor: str = ""):
        self.descriptor = descriptor
        self.value = ""
        self.x = x
        self.y = y
        self.location = (x, y)
        self.spreadsheet = this_spreadsheet
        self.__call__()

    def __call__(self):
        if self.descriptor.startswith('='):
            write_to_temp(self, self.descriptor[1:])
            self.value = load_from_temp(self, self.spreadsheet)
            return self.value
        else:
            self.value = self.descriptor
            return self.value

    def __str__(self):
        if isinstance(self.value, str):
            return "'" + self.value + "'"
        else:
            return str(self.value)

    def __getitem__(self, key):
        if isinstance(key, tuple):
            y, x = key
            dy = self.y
            dx = self.x
            if isinstance(y, slice):
                y = slice(y.start + dy, y.stop + dy, y.step)
            else:
                y += dy
            if isinstance(x, slice):
                x = slice(x.start + dx, x.stop + dx, x.step)
            else:
                x += dx
        else:
            raise ValueError('If you want to select a row or column use: (e.g. cell[1,:])')
        return self.spreadsheet[y, x]


def cell_to_function_name(cell: Cell):
    return f"fun_{cell.y}_{cell.x}"


def load_from_temp(cell: Cell, sh: SpreadSheet):
    import temp.tmp
    importlib.reload(temp.tmp)
    return temp.tmp.this_exec(f"{cell_to_function_name(cell)}(C, S)", cell, sh)


def write_to_temp(cell: Cell, fun: str):
    fun = fun.split('\\n')
    if fun[-1].find('return') == -1:
        whitespaces = len(fun[-1]) - len(fun[-1].lstrip())
        fun[-1] = fun[-1][:whitespaces] + 'return ' + fun[-1][whitespaces:]
    fun = list(map(lambda x:'    ' + x, fun))
    fun = '\n'.join(fun)
    with open('temp/tmp.py', 'a') as f:
        f.write(f"""def {cell_to_function_name(cell)}(C: Cell, S: SpreadSheet):
{fun}


""")


def init_temp():
    with open('temp/tmp.py', 'w') as f:
        f.write(f"""{boilerplate}""")


def load_from_csv(csv_file):
    with open(csv_file, 'r') as f:
        csv_reader = list(csv.reader(f, delimiter=';'))
    rows = len(csv_reader)
    cols = max([len(row) for row in csv_reader])
    spreadsheet = SpreadSheet(cols, rows)
    for row in range(rows):
        csv_reader[row] += [''] * (cols - len(csv_reader[row]))
    for row in range(rows):
        for col in range(cols):
            spreadsheet(row, col, csv_reader[row][col])
    return spreadsheet


def compute_spreadsheet(csv_file: str, spreadsheet: SpreadSheet):
    csv_file = csv_file[:-4] + '_out.csv'
    spreadsheet = list(map(lambda row: list(map(lambda cell: str(cell), row)), spreadsheet.cells))
    with open(csv_file, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(spreadsheet)


if __name__ == '__main__':
    init_temp()
    spreadsheet = load_from_csv('pycell.csv')
    compute_spreadsheet('pycell.csv', spreadsheet)
    print(spreadsheet)
