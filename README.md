# PyCell
An alternative to Excel or other spreadsheet programs.
You can edit the `pycell.csv`.

## Syntax
- Write anything in the csv and it will be interpreted as a string.
- Start it with `=` and everything afterwards will be interpreted as python code.

More specifically: Assume the cell at location x=1 and y=2 `=1+2` becomes
```
def fun_2_1(C: Cell, S: SpreadSheet):
    return 1+2
```

You can also add multiline python statements. Decode a new line as usual `\n`.
So `=class Person:\n    def __init__(self, name):\n        self.name = name\n    Person('Hans')`
in cell x=273 and y=1024 becomes: 
```
def fun_1024_273(C: Cell, S: SpreadSheet):
    class Person:
        def __init__(self, name):
            self.name = name
    return Person('Hans')
```
The logic is: That if the last line in your statement does not contain a `return`
it will be automatically added. So you can add a return in the end but you don't
have to.

All the created functions are in the same file. So do whatever you think is funny 
using this fact. You can use globals an alike to escape your function.

If you need some special libraries add them to `setup.py`. This will be added at the
beginning of the python file containing all functions. Ensure that the package is
installed on the system you are running it afterwards.

###Access Values
You can now access these values. Assuming the above example you can
now use these values by the following code: `=S[1024,273]`

By executing the python program the spreadsheet gets evaluated.
A new spreadsheet in `pycell_out.csv` gets created with the evaluated cells.

The cells can be accessed by two functions:
- `=S[y,x]` accesses the cell at row `y` and column `x`
- `=C[dy,dx]` accessed the cell at the relative `dy,dx` position from 
the current cell

The cells are stored internally as a numpy array.
Therefore also sub parts can be chosen:
- `=S[1:3,2]` accesses the cells at row `1` and `2` and at column `2`.

Please check the `pycell.csv` for interesting examples.

- Please don't take this code too seriously.
It has obvious security issues as it just executes whatever code is in the 
spreadsheet.
It could be improved by a simple GUI which just lets you execute each cell 
individually and look at the formula and the  computed value 
simultaneously.
- But also don't take it not serious at all: A spreadsheet program is nothing 
complicated. This can do the job and because you can import every python
library you have installed on your computer it has much more possibilities
than Microsoft Excel or LibreOffice.

(Of course the usability is crap)