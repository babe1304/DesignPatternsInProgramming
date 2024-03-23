from tkinter import *
from Renderer import Renderer
from point import Point
from typing import List
from State import State
from models import DocumentModelListener, GraphicalObject

class CanvasModel(Canvas, Renderer, DocumentModelListener):
    def __init__(self, documentModel=None, state: State =None):
        super().__init__(width=600, height=600, bg="white", cursor="crosshair", relief=SUNKEN, borderwidth=2, highlightthickness=0)
        self.documentModel = documentModel
        self.documentModel.addDocumentModelListener(self)
        self.state = state
        self.pack()

    def drawLine(self, s: Point, e: Point) -> None:
        self.create_line(s.x, s.y, e.x, e.y, fill="red", width=2)

    def fillPolygon(self, points: List[Point]) -> None:
        self.create_polygon([(p.x, p.y) for p in points], fill="blue")

    def paintComponent(self):
        for o in self.documentModel.objects:
            o.render(self)
        self.state.afterDraw()

    def documentChanged(self, o: GraphicalObject) -> None:
        self.delete(ALL)
        self.paintComponent()
        