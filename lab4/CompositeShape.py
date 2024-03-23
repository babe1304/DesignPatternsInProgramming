from typing import List
from Rectangle import Rectangle
from Renderer import Renderer
from point import Point
from models import GraphicalObject

class CompositeShape(GraphicalObject):
    def __init__(self, objs: List[GraphicalObject]=[]) -> None:
        super().__init__()
        self.objects = objs

    def getCenter(self) -> Point:
        xs = [o.getBoundingBox().x1 for o in self.objects]
        ys = [o.getBoundingBox().y1 for o in self.objects]
        return Point(sum(xs)/len(xs), sum(ys)/len(ys))

    def getBoundingBox(self) -> Rectangle:
        x1 = [o.getBoundingBox().x1 for o in self.objects]
        y1 = [o.getBoundingBox().y1 for o in self.objects]
        x2 = [o.getBoundingBox().x2 for o in self.objects]
        y2 = [o.getBoundingBox().y2 for o in self.objects]
        return Rectangle(min(x1 + x2), min(y1 + y2), max(x1 + x2), max(y1 + y2))
    
    def translate(self, delta: Point) -> None:
        for o in self.objects:
            o.translate(delta)

    def duplicate(self) -> GraphicalObject:
        return CompositeShape([o.duplicate() for o in self.objects])

    def render(self, renderer: Renderer) -> None:
        for o in self.objects:
            o.render(renderer)

    def getShapeName(self) -> str:
        return "Kompozit"
    
    def selectionDistance(self, point: Point) -> float:
        return min([o.selectionDistance(point) for o in self.objects])
    
    def getShapeID(self) -> str:
        return "@COMP"
    
    def save(self) -> str:
        line = ""
        for o in self.objects:
            line += o.save()
        return line + f"{self.getShapeID()} {len(self.objects)}\n"
    
    def load(self, stack: list, line: str) -> None:
        args = line.split()
        num = int(args[1])
        objs = []
        for _ in range(num):
            objs.append(stack.pop())
        stack.append(CompositeShape(objs))
