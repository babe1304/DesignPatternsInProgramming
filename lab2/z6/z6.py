import re
import ast
from abc import ABC, abstractmethod

class CellListener(ABC):
    @abstractmethod
    def cellChanged(self):
        pass

class Cell(CellListener):
    def __init__(self, sheet, exp) -> None:
        self.sheet = sheet
        self.exp = exp
        self.listeners = []
        self.reference = []
        self.value = self.exp if type(self.exp) == int else self.eval_expression(self.exp, self.sheet)

    def __call__(self):
        return f" [{str(self.exp)}] = {self.value}"
    
    def __eq__(self, __value: object) -> bool:
        return type(self) == type(__value) and self.exp == __value.exp
    
    def eval_expression(self, exp, variables):
        def _eval(node):
            if isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.Name):
                cell =  variables.cell(node.id)
                if not self in cell.listeners:
                    cell.addCellListener(self)
                if not cell in self.reference:
                    self.reference.append(cell)
                return cell.value
            elif isinstance(node, ast.BinOp):
                return _eval(node.left) + _eval(node.right)
            else:
                raise Exception('Unsupported type {}'.format(node))
        node = ast.parse(exp, mode='eval')
        return _eval(node.body)

    def cellChanged(self):
        self.value = self.exp if type(self.exp) == int else self.eval_expression(self.exp, self.sheet)
        return 
    
    def addCellListener(self, c: CellListener):
        self.listeners.append(c)

    def removeCellListener(self, c: CellListener):
        if c in self.listeners:
            self.listeners.remove(c)
    
    def notify(self):
        for cell in self.listeners:
            cell.cellChanged()
 
class Sheet:
    def __init__(self, rows, cols) -> None:
        self.RE = "[A-H][1-8]"
        self.rows = rows
        self.cols = cols
        self.cells = [[0] * cols for _ in range(rows)]

    def print(self):
        for row in self.cells:
            line = ""
            for cell in row:
                if cell == 0:
                    line += " [Empty]"
                else:
                    line += cell()
            print(line)

    def check(self, c):
        st = c.reference
        checked = []
        while st:
            el = st.pop()
            if el == c:
                raise RuntimeError("Kružna ovisnost.")
            checked.insert(0, el)
            for s in el.reference:
                st.append(s)
        return
    
    def cell(self, ref):
        x, y = ord(ref[0]) - ord('A'), int(ref[1]) - 1
        return self.cells[x][y]

    def set(self, ref, content):
        if not re.match(self.RE, ref):
            raise ValueError
        x, y = ord(ref[0]) - ord('A'), int(ref[1]) - 1
        present = self.cells[x][y] != 0
        if not present:
            cell = Cell(self, content)
            self.cells[x][y] = cell
        else:
            self.cells[x][y].exp = content
            self.cells[x][y].cellChanged()
            self.check(self.cells[x][y])
            self.cells[x][y].notify()
        return
    
    def getrefs(self, cell):
        c = self.cell(cell)
        print(list(map(lambda x: x.exp, c.reference)), sep=" - ")
        return
    
    def evaluate(self, cell):
        cell.evaluate()
        return

if __name__=="__main__":
    s=Sheet(5,5)

    s.set('A1',2)
    s.set('A2',5)
    s.set('A3','A1+A2')
    s.print()
    print()

    s.set('A1',4)
    s.set('A4','A1+A3')
    s.print()
    print()

    s.getrefs("A3")
    try:
        s.set('A1','A3')
    except RuntimeError as e:
        print("Caught exception:",e)
    s.print()
    print()