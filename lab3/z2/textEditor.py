from tkinter import *
from tkinter.font import Font
from tkinter.simpledialog import askstring
from importlib import import_module
import os

class CursorObserver:
    def __init__(self):
        pass

    def updateCursorLocation(self, loc):
        return
    
class TextObserver:
    def __init__(self):
        pass

    def updateText(self):
        return
    
class ClipboardObserver:
    def __init__(self):
        pass

    def updateClipboard(self):
        return
    
class ClipboardStack():
    def __init__(self, textEditor=None):
        self.textEditor = textEditor
        self.texts = []
        self.clipboardObservers = []

    def stack(self, el):
        self.texts.append(el)
        self.notifyClipboardObservers()

    def pop(self):
        el = self.texts.pop()
        self.notifyClipboardObservers()
        return el
    
    def peek(self):
        return self.texts[-1]

    def isEmpty(self):
        return len(self.texts) == 0
    
    def clear(self):
        self.texts.clear()
        self.notifyClipboardObservers()
    
    def addClipboardObserver(self, obs):
        self.clipboardObservers.append(obs)

    def notifyClipboardObservers(self):
        for obs in self.clipboardObservers: obs.updateClipboard()


class Location:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __iter__(self):
        return iter((self.row, self.col))

class LocationRange:
    def __init__(self, start: Location, end: Location):
        self.start = start
        self.end = end

class TextEditorModel:
    def __init__(self, text=""):
        self.lines = text.split('\n')
        self.cursorLocation = Location(len(self.lines) - 1, len(self.lines[-1]))
        self.selectionRange = None
        self.cursorObservers = []
        self.textObservers = []

    def allLines(self):
        return iter(self.lines)
    
    def linesRange(self, index1: int, index2: int):
        return iter(self.lines[index1 - 1: index2])
    
    def addCursorObserver(self, obs):
        self.cursorObservers.append(obs)

    def notifyCursorObservers(self):
        for obs in self.cursorObservers: obs.updateCursorLocation()

    def addTextObserver(self, obs):
        self.textObservers.append(obs)

    def notifyTextObservers(self):
        for obs in self.textObservers: obs.updateText()

    def getSelectionRange(self):
        return self.selectionRange
    
    def setSelectionRange(self, sr: LocationRange):
        self.selectionRange = sr

    def insert(self, input_: str):
        r = self.cursorLocation.row 
        c = self.cursorLocation.col

        for ch in input_[::-1]:
            if ord(ch) != 13:
                line = list(self.lines[r])
                line.insert(c, ch)
                self.lines[r] = "".join(line)
                self.cursorLocation.col += 1
            else:
                if c == len(self.lines[r]):
                    self.lines.insert(r + 1,"")
                else:
                    self.lines.insert(r + 1, self.lines[r][c:])
                    self.lines[r] = self.lines[r][:c]
                self.cursorLocation.row = r + 1
                self.cursorLocation.col = 0
        self.notifyTextObservers()
        self.notifyCursorObservers()

    def deleteBefore(self):
        r = self.cursorLocation.row 
        c = self.cursorLocation.col
        if self.selectionRange != None:
            self.deleteRange(self.selectionRange)
        else:
            if r != 0 or c != 0:
                if c != 0:
                    line = self.lines[r]
                    new_line = line[:c - 1] + line[c:]
                    self.lines[r] = new_line
                    self.cursorLocation.col -= 1
                else:
                    upper_line = self.lines[r - 1]
                    new_line = upper_line + self.lines[r]
                    self.lines[r - 1] = new_line
                    self.lines.pop(r)
                    self.cursorLocation.row -= 1
                    self.cursorLocation.col = len(upper_line)
                self.notifyTextObservers()
                self.notifyCursorObservers()

    def deleteAfter(self):
        r = self.cursorLocation.row 
        c = self.cursorLocation.col
        if self.selectionRange != None:
            self.deleteRange(self.selectionRange)
        else:
            if r != len(self.lines) - 1 or c != len(self.lines[-1]):
                if c != len(self.lines[r][-1]):
                    line = self.lines[r]
                    new_line = line[:c] + line[c + 1:]
                    self.lines[r] = new_line
                else:
                    curr_line = self.lines[r]
                    new_line = curr_line + self.lines[r + 1]
                    self.lines[r] = new_line
                    self.lines.pop(r + 1)
                    self.cursorLocation.col = len(curr_line)
                self.notifyTextObservers()
                self.notifyCursorObservers()

    def deleteRange(self, lr: LocationRange):
        if lr.start.row == lr.end.row:
            first_part = self.lines[lr.start.row][:lr.start.col]
            second_part = self.lines[lr.start.row][lr.end.col + 1:]
            self.lines[lr.start.row] = first_part + second_part
        else:
            for i in range(lr.start.row, lr.end.row + 1):
                if i == lr.start.row:
                    self.lines[lr.start.row] = self.lines[lr.start.row][:lr.start.col]
                if i == lr.end.row:
                    self.lines[lr.end.row] = self.lines[lr.end.row][lr.end.col:]
            for i in range(lr.start.row + 1, lr.end.row):
                self.lines.pop(i)
        self.cursorLocation.col = self.selectionRange.start.col
        self.cursorLocation.row = self.selectionRange.start.row
        self.selectionRange = None
        self.notifyCursorObservers()
        self.notifyTextObservers()

    def moveCursorLeft(self):
        if self.cursorLocation.col > 0:
            self.cursorLocation.col -= 1
        elif self.cursorLocation.row > 0:
            self.cursorLocation.row -= 1
            self.cursorLocation.col = len(self.lines[self.cursorLocation.row])
        if self.selectionRange != None:
            if self.selectionRange.start.row == self.selectionRange.end.row and self.selectionRange.start.col == self.selectionRange.end.col:
                self.setSelectionRange(LocationRange(Location(self.cursorLocation.row, self.cursorLocation.col), self.selectionRange.start))
            elif self.selectionRange.start.row == self.selectionRange.end.row and self.cursorLocation.col in list(range(self.selectionRange.start.col, self.selectionRange.end.col + 1)):
                self.setSelectionRange(LocationRange(self.selectionRange.start, Location(self.cursorLocation.row, self.cursorLocation.col)))
            else:
                self.setSelectionRange(LocationRange(Location(self.cursorLocation.row, self.cursorLocation.col), self.selectionRange.end))
        self.notifyCursorObservers()
    
    def moveCursorRight(self):
        if self.cursorLocation.col < len(self.lines[self.cursorLocation.row]):
            self.cursorLocation.col += 1
        elif self.cursorLocation.row < len(self.lines) - 1:
            self.cursorLocation.col = 0
            self.cursorLocation.row += 1
        if self.selectionRange != None:
            if self.selectionRange.start.row == self.selectionRange.end.row and self.selectionRange.start.col == self.selectionRange.end.col:
                self.setSelectionRange(LocationRange(self.selectionRange.start, Location(self.cursorLocation.row, self.cursorLocation.col)))
            elif self.selectionRange.start.row == self.selectionRange.end.row and self.cursorLocation.col in list(range(self.selectionRange.start.col, self.selectionRange.end.col + 1)):
                self.setSelectionRange(LocationRange(Location(self.cursorLocation.row, self.cursorLocation.col), self.selectionRange.end))
            else:
                self.setSelectionRange(LocationRange(self.selectionRange.start, Location(self.cursorLocation.row, self.cursorLocation.col)))
        self.notifyCursorObservers()

    def moveCursorUp(self):
        if self.cursorLocation.row > 0:
            self.cursorLocation.row -= 1

            if self.cursorLocation.col >= len(self.lines[self.cursorLocation.row]): self.cursorLocation.col = len(self.lines[self.cursorLocation.row])
            if self.selectionRange != None:
                if self.selectionRange.start.row >= self.selectionRange.end.row:
                    self.setSelectionRange(LocationRange(Location(self.cursorLocation.row, self.cursorLocation.col), self.selectionRange.start))
                else:    
                    self.setSelectionRange(LocationRange(self.selectionRange.start, Location(self.cursorLocation.row, self.cursorLocation.col)))
            self.notifyCursorObservers()

    def moveCursorDown(self):
        if self.cursorLocation.row < len(self.lines) - 1:
            self.cursorLocation.row += 1

            if self.cursorLocation.col >= len(self.lines[self.cursorLocation.row]): self.cursorLocation.col = len(self.lines[self.cursorLocation.row]) - 1
            if self.selectionRange != None:
                if self.selectionRange.start.row >= self.selectionRange.end.row:
                    self.setSelectionRange(LocationRange(self.selectionRange.start, Location(self.cursorLocation.row, self.cursorLocation.col)))
                else:    
                    self.setSelectionRange(LocationRange(Location(self.cursorLocation.row, self.cursorLocation.col), self.selectionRange.start))
            
            self.notifyCursorObservers()

class EditAction:
    def __init__(self, ) -> None:
        pass

    def execute_do(self):
        return

    def execute_undo(self):
        return

class UndoManager:
    def __init__(self) -> None:
        self.undoStack = []
        self.redoStack = []

    def undo(self):
        return
        
    def redo(self):
        return

class TextEditor(Frame):
    def __init__(self, master=None, model:TextEditorModel=None):
        super().__init__(master)
        self.master = master
        self.model = model
        self.font = Font(master, name="Monospace", size=16)
        self.asc = self.font.metrics("ascent")
        self.des = self.font.metrics("descent")
        self.modules = []
        self.undoManager = UndoManager()

        for mymodule in os.listdir('plugins'):
            moduleName, moduleExt = os.path.splitext(mymodule)
            if moduleExt=='.py':
                module=self.get_module(moduleName)
            self.modules.append(module)

        self.clipboard = ClipboardStack(self)
        self.clipboard.addClipboardObserver(self)

        self.model.addCursorObserver(self)
        self.model.addTextObserver(self)
        
        self.master.bind('<Left>', lambda *args: self.model.moveCursorLeft())
        self.master.bind('<Right>', lambda *args: self.model.moveCursorRight())
        self.master.bind('<Up>', lambda *args: self.model.moveCursorUp())
        self.master.bind('<Down>', lambda *args: self.model.moveCursorDown())
        self.master.bind('<BackSpace>', lambda *args: self.model.deleteBefore())
        self.master.bind('<Delete>', lambda *args: self.model.deleteAfter())
        self.master.bind('<Shift_L>', lambda *args: self.setSelection())
        self.master.bind('<Control-c>', lambda *args: self.copy())
        self.master.bind('<Control-x>', lambda *args: self.cut())
        self.master.bind('<Control-v>', lambda *args: self.paste())
        self.master.bind('<Control-z>', lambda *args: self.undo())
        self.master.bind('<Control-y>', lambda *args: self.redo())
        self.master.bind('<Control-Shift-v>', lambda *args: self.insert())
        self.master.bind('<KeyPress>', self.add_text)

        self.menu_bar = Menu(self.master)

        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_f)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.quit)

        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo")
        self.edit_menu.add_command(label="Redo")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Delete", command=self.delete)

        self.move_menu = Menu(self.menu_bar, tearoff=0)
        self.move_menu.add_command(label="Cursor to document start", command=self.move_start)
        self.move_menu.add_command(label="Cursor to document end", command=self.move_end)

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.menu_bar.add_cascade(label="Move", menu=self.move_menu)
        self.master.config(menu=self.menu_bar)

        self.text_area = Canvas(self, width=600, height=400, bg='white')
        self.draw()
        self.text_area.pack()

        self.status_bar_1 = Label(self.master, text=f'Cursor at:{self.model.cursorLocation.row}:{self.model.cursorLocation.col}', bd=1, relief=SUNKEN, anchor=E)
        self.status_bar_1.pack(side=BOTTOM, fill=X)
        self.status_bar_2 = Label(self.master, text=f'Number of lines:{len(self.model.lines)}', bd=1, relief=SUNKEN, anchor=E)
        self.status_bar_2.pack(side=BOTTOM, fill=X)

        self.pack()
        self.master.mainloop()

    def get_module(self, moduleName):
        return getattr(import_module(f'.{moduleName}', 'plugins'), moduleName)
    
    def move_start(self):
        self.model.cursorLocation = Location(0, 0)
        self.draw()
    
    def move_end(self):
        self.model.cursorLocation = Location(len(self.model.lines) - 1, len(self.model.lines[-1]))
        self.draw()

    def open_f(self):
        input_ = askstring(title="Open", prompt="Open file:", initialvalue="./", parent=self.master)
        self.model = TextEditorModel(open(input_).read())
        self.model.addCursorObserver(self)
        self.model.addTextObserver(self)
        self.draw()

    def save(self):
        output_ = askstring(title="Save", prompt="Save file:", initialvalue="./", parent=self.master)

        with open(output_, "w") as output:
            for line in self.model.lines:
                output.write(f'{line}\n')
    
    def insert(self):
        text = self.clipboard.pop()
        self.model.insert(text)

    def copy(self):
        selection = self.model.getSelectionRange()
        lines = self.model.lines[selection.start.row: selection.end.row + 1]
        if len(lines) == 1:
            text = lines[0][selection.start.col:selection.end.col + 1]
        else:
            text = lines[0][selection.start.col:]
            for line in lines[1:-1]:
                text += line
            text += lines[-1][:selection.end.col]
        self.model.setSelectionRange(None)
        self.clipboard.stack(text)

    def cut(self):
        selection = self.model.getSelectionRange()
        lines = self.model.lines[selection.start.row: selection.end.row + 1]
        if len(lines) == 1:
            text = lines[0][selection.start.col:selection.end.col + 1]
        else:
            text = lines[0][selection.start.col:]
            for line in lines[1:-1]:
                text += line
            text += lines[-1][:selection.end.col]
        self.model.deleteRange(selection)
        self.model.setSelectionRange(None)
        self.clipboard.stack(text)

    def paste(self):
        text = self.clipboard.peek()
        self.model.insert(text)

    def delete(self):
        selection = self.model.getSelectionRange()
        lines = self.model.lines[selection.start.row: selection.end.row + 1]
        if len(lines) == 1:
            text = lines[0][selection.start.col:selection.end.col + 1]
        else:
            text = lines[0][selection.start.col:]
            for line in lines[1:-1]:
                text += line
            text += lines[-1][:selection.end.col]
        self.model.deleteRange(selection)
        self.model.setSelectionRange(None)

    def add_text(self, event: Event):
        if event.keysym in ['Control_L', 'Control_L-c', 'Control_L-x', 'Control_L-v']:
            return
        if self.model.getSelectionRange() != None:
            self.model.deleteRange(self.model.getSelectionRange())
        self.model.insert(event.char)

    def setSelection(self):
        if self.model.getSelectionRange() == None:
            cursor_row, cursor_col = self.model.cursorLocation
            self.model.setSelectionRange(LocationRange(Location(cursor_row, cursor_col), Location(cursor_row, cursor_col)))
        else:
            self.model.setSelectionRange(None)
        self.draw()

    def draw(self):
        self.text_area.delete('all')
        x = y = 4
        cursor_row, cursor_col = self.model.cursorLocation
        selection = self.model.getSelectionRange()
        for i, line in enumerate(self.model.allLines()):
            self.text_area.create_text(x, y + i * self.asc + (i + 1) * self.des, text=line, font=self.font, anchor='nw', tags=f"text_{i}")        
            
            if i == cursor_row:
                cursor_x = x + self.font.measure(line[:cursor_col])
                cursor_y1 = y + i * self.asc + (i + 1) * self.des
                cursor_y2 = cursor_y1 + self.asc
                self.text_area.create_line(cursor_x, cursor_y1, cursor_x, cursor_y2, tags="cursor")

            if selection != None:
                s_x = x + self.font.measure(line[:selection.start.col])
                s_y1 = y + i * self.asc + (i + 1) * self.des
                s_y2 = s_y1 + self.asc
                if i == selection.start.row:
                    if selection.start.row == selection.end.row:
                        self.text_area.create_rectangle(s_x, s_y1, s_x + self.font.measure(line[selection.start.col:selection.end.col + 1]), s_y2)
                    else:
                        self.text_area.create_rectangle(s_x, s_y1, s_x + self.font.measure(line[selection.start.col:]), s_y2)
                elif i in list(range(selection.start.row + 1, selection.end.row)):
                    self.text_area.create_rectangle(x, s_y1, self.font.measure(line), s_y2)
                elif i == selection.end.row:
                    self.text_area.create_rectangle(x, s_y1, self.font.measure(line[:selection.end.col]), s_y2)
        if self.clipboard.isEmpty():
            self.edit_menu.entryconfig("Paste", state="disabled")
        else:
            self.edit_menu.entryconfig("Paste", state="normal")
        if self.model.getSelectionRange() == None:
            self.edit_menu.entryconfig("Cut", state="disabled")
            self.edit_menu.entryconfig("Copy", state="disabled")
            self.edit_menu.entryconfig("Delete", state="disabled")
        else:
            self.edit_menu.entryconfig("Cut", state="normal")
            self.edit_menu.entryconfig("Copy", state="normal")
            self.edit_menu.entryconfig("Delete", state="normal")

        #for plugin in self.modules:
            #output = plugin.execute(self.model)
            #print(output)

    def update_status(self):
        self.status_bar_1.config(text=f'Cursor at:{self.model.cursorLocation.row}:{self.model.cursorLocation.col}')
        self.status_bar_2.config(text=f'Number of lines:{len(self.model.lines)}')

    def updateCursorLocation(self):
        self.draw()
        self.update_status()

    def updateText(self):
        self.draw()

    def updateClipboard(self):
        pass

    def undo(self):
        return
    
    def redo(self):
        return