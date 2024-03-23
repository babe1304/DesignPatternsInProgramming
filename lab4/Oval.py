from Renderer import Renderer
from point import Point
from models import GraphicalObject
from Rectangle import Rectangle
from GeometryUtil import GeomatryUtil
import math

class Oval(GraphicalObject):
    def __init__(self, right=Point(10, 0), down=Point(0, 10)) -> None:
        super().__init__([right, down])
        self.update()

    def update(self) -> None:
        self.right = self.hot_points[0]
        self.down = self.hot_points[1]
        self.center = Point(self.down.x, self.right.y)
        self.width = 2 * (self.right.x - self.center.x)
        self.height = 2 * (self.down.y - self.center.y)

    def selectionDistance(self, point: Point) -> float:
        d = math.sqrt((point.x - self.center.x)**2 + (point.y - self.center.y)**2)
        angle = math.atan2(point.y - self.center.y, point.x - self.center.x)
        return d - math.sqrt((self.width/2)**2 * math.cos(angle)**2 + (self.height/2)**2 * math.sin(angle)**2)
    
    def getBoundingBox(self) -> Rectangle:
        return Rectangle(self.center.x - self.width / 2, self.center.y - self.height / 2, self.center.x + self.width / 2, self.center.y + self.height / 2)
    
    def duplicate(self) -> GraphicalObject:
        return Oval(self.right, self.down)
    
    def getShapeName(self) -> str:
        return "Oval"
    
    def render(self, renderer: Renderer) -> None:
        self.update()
        points = []
        cx, cy = self.center    
        a = self.width / 2
        b = self.height / 2
        x0, y0 = cx + a, cy
        for i in range(180):
            points.append(Point(x0, y0))
            angle = 2 * math.pi * i / 180
            x1 = (cx + a * math.cos(angle) + 0.5)
            y1 = (cy + b * math.sin(angle) + 0.5)
            renderer.drawLine(Point(x0, y0), Point(x1, y1))
            x0, y0 = x1, y1
        renderer.fillPolygon(points)

    def getCenter(self) -> Point:
        return self.center
    
    def getHotPointDistance(self, index: int, point: Point) -> float:
        hp = self.getHotPoint(index)
        return GeomatryUtil.distanceFromPoint(hp, point)
    
    def getShapeID(self) -> str:
        return "@OVAL"
    
    def save(self) -> str:
        return f'{self.getShapeID()} {self.right.x} {self.right.y} {self.down.x} {self.down.y}\n'
    
    def load(self, stack: list, line: str) -> None:
        args = line.split(" ")
        stack.append(Oval(Point(*map(float, args[1:3])), Point(*map(float, args[3:5]))))