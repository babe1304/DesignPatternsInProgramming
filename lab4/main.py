from tkinter import *
from PaintEditor import PaintEditor
from LineSegment import LineSegment
from Oval import Oval

if __name__=="__main__":
    objects = [Oval(), LineSegment()]
    app = PaintEditor(objects=objects)