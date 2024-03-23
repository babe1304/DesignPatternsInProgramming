from tkinter import *
from textEditor import TextEditor, TextEditorModel

if __name__=="__main__":
    app = TextEditor(master=Tk(), model=TextEditorModel())