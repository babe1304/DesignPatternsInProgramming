from Renderer import Renderer
from models import GraphicalObject
from point import Point
from Rectangle import Rectangle
from GeometryUtil import GeomatryUtil

class LineSegment(GraphicalObject):
    def __init__(self, p1=Point(0, 0), p2=Point(10, 0)) -> None:
        super().__init__([p1, p2])
        self.update()
       
    def update(self) -> None:
        self.p1 = self.hot_points[0]
        self.p2 = self.hot_points[1]

    def selectionDistance(self, point: Point) -> float:
        return GeomatryUtil.distanceFromLineSegment(self.p1, self.p2, point)

    def getBoundingBox(self) -> Rectangle:
        return Rectangle(self.p1.x, self.p1.y, self.p2.x, self.p2.y)
    
    def duplicate(self) -> GraphicalObject:
        return LineSegment(self.p1, self.p2)
    
    def getShapeName(self) -> str:
        return "Linija"
    
    def render(self, renderer: Renderer) -> None:
        self.update()
        renderer.drawLine(self.p1, self.p2)
         
    def getCenter(self) -> Point:
        return Point((self.p1.x + self.p2.x)/2, (self.p1.y + self.p2.y)/2)
    
    def getShapeID(self) -> str:
        return "@LINE"
    
    def save(self) -> str:
        return f'{self.getShapeID()} {self.p1.x} {self.p1.y} {self.p2.x} {self.p2.y}\n'
    
    def load(self, stack: list, line: str) -> None:
        args = line.split(" ")
        stack.append(LineSegment(Point(*map(float, args[1:3])), Point(*map(float, args[3:5]))))