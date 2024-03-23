from tkinter import *
from typing import List
from models import GraphicalObject
from DocumentModel import DocumentModel
from Canvas import CanvasModel
from State import State, AddShapeState, SelectShapeState, EraserState
from point import Point
from SVGRendererImpl import SVGRendererImpl
from tkinter import filedialog
from CompositeShape import CompositeShape

class PaintEditor(Tk):
    def __init__(self, objects: List[GraphicalObject] = []):
        super().__init__()
        self.objects = objects
        self.title("Paint Editor")
        self.documentModel = DocumentModel()

        self.state = State()
        self.ctrlDown = False
        self.shiftDown = False
        self.create_toolbar()
        self.canvas = CanvasModel(self.documentModel, self.state)
        self.canvas.paintComponent()

        self.bind('<Escape>', lambda e: self.setState())
        self.bind('<KeyPress-Shift_L>', lambda *args: self.setShift(True))
        self.bind('<KeyRelease-Shift_L>', lambda *args: self.setShift(False))
        self.bind('<KeyPress-Control_L>', lambda *args: self.setControl(True))
        self.bind('<KeyRelease-Control_L>', lambda *args: self.setControl(False))
        self.canvas.bind('<Button-1>', lambda e: self.state.mouseDown(Point(e.x, e.y), self.shiftDown, self.ctrlDown))
        self.canvas.bind('<ButtonRelease-1>', lambda e: self.state.mouseUp(Point(e.x, e.y), self.shiftDown, self.ctrlDown))
        self.canvas.bind('<Motion>', lambda e: self.state.mouseDragged(Point(e.x, e.y)))
        self.bind('<Key>', lambda e: self.state.keyPressed(e))

        self.mainloop()

    def setControl(self, isDown):
        self.ctrlDown = isDown

    def setShift(self, isDown):
        self.shiftDown = isDown

    def setState(self, state: State = State()):
        self.state.onLeaving()
        self.state = state
        self.canvas.state = self.state

    def create_toolbar(self):
        toolbar = Frame(self)
        open_button = Button(toolbar, text="Učitaj", command=lambda: self.load())
        open_button.pack(side=LEFT)
        save_button = Button(toolbar, text="Pohrani", command=lambda: self.save())
        save_button.pack(side=LEFT)
        edit_button = Button(toolbar, text="SVG export", command=lambda: self.exportSVG())
        edit_button.pack(side=LEFT)
        button_dict = {}
        for i, o in enumerate(self.objects):
            shape_name = o.getShapeName()
            def create_lambda(i):
                return lambda: self.setState(AddShapeState(self.documentModel, self.objects[i], self.canvas))
            button_dict[shape_name] = Button(toolbar, text=shape_name, command=create_lambda(i))
            button_dict[shape_name].pack(side=LEFT)
        select_button = Button(toolbar, text="Selektiraj", command=lambda: self.setState(SelectShapeState(self.documentModel, self.canvas)))
        select_button.pack(side=LEFT)
        delete_button = Button(toolbar, text="Obriši", command=lambda: self.setState(EraserState(self.documentModel, self.canvas)))
        delete_button.pack(side=LEFT)
        toolbar.pack(side=TOP, fill=X, anchor=N, pady=5)

    def exportSVG(self):
        file_name = filedialog.asksaveasfilename(initialdir = ".",title = "Select file",filetypes = (("svg files","*.svg"),("all files","*.*")))
        if file_name:
            renderer = SVGRendererImpl(file_name)
            for o in self.documentModel.objects:
                o.render(renderer)
            renderer.close()

    def save(self):
        file_name = filedialog.asksaveasfilename(initialdir = ".",title = "Select file",filetypes = (("paint files","*.paint"),("all files","*.*")))
        if file_name:
            with open(file_name, "w") as f:
                for o in self.documentModel.objects:
                    f.write(o.save())

    def load(self):
        file_name = filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("paint files","*.paint"),("all files","*.*")))
        mapper = { o.getShapeID(): o for o in self.objects }
        self.documentModel.objects.clear()
        if file_name:
            with open(file_name, "r") as f:
                lines = f.readlines()
                objects = []
                for line in lines:
                    line_ = line.strip().split(" ")

                    if line_[0] not in mapper.keys():
                        CompositeShape().load(objects, line)
                    else:
                        mapper[line_[0]].load(objects, line)

                for o in objects:
                    self.documentModel.addGraphicalObject(o)