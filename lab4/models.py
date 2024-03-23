from typing import List
from point import Point
from Rectangle import Rectangle
from Renderer import Renderer
from GeometryUtil import GeomatryUtil

class GraphicalObjectListener:
    def __init__(self, documentModel) -> None:
        super().__init__()
        self.documentModel = documentModel

    def graphicalObjectChanged(self, o: "GraphicalObject") -> None:
        self.documentModel.notifyListeners(o)

class GraphicalObject:
    """Abstract class for graphical objects."""
    def __init__(self, points: List[Point] = []) -> None:
        super().__init__()
        self.hot_points = points
        self.selected = False
        self.selected_hot_point = -1
        self.listeners: List[GraphicalObjectListener] = []

    def isSelected(self) -> bool:
        return self.selected

    def setSelected(self, selected: bool) -> None:
        self.selected = selected

    def getNumberOfHotPoints(self) -> int:
        return len(self.hot_points)

    def getHotPoint(self, index: int) -> Point:
        return self.hot_points[index]

    def setHotPoint(self, index: int, point: Point) -> None:
        self.hot_points[index] = point

    def setHotPointSelected(self, index: int) -> None:
        self.selected_hot_point = index

    def isHotPointSelected(self, index: int) -> bool:
        return self.selected_hot_point == index

    def findSelectedHotPoint(self, point: Point) -> int:
        for i, p in enumerate(self.hot_points):
            if GeomatryUtil.distanceFromPoint(p, point) <= 7:
                return i
        return -1

    def getSelectedHotPoint(self) -> Point:
        return self.hot_points[self.selected_hot_point] if self.selected_hot_point != -1 else None  

    def getCenter(self) -> Point:
        return

    def translate(self, delta: Point) -> None:
        for i, p in enumerate(self.hot_points):
            self.hot_points[i] = p.translate(delta)

    def getBoundingBox(self) -> Rectangle:
        return Rectangle(0, 0, 0, 0)

    def selectionDistance(self, point: Point) -> float:
        return 0

    def render(self, renderer: Renderer) -> None:
        return

    def addGraphicalObjectListener(self, listener: GraphicalObjectListener) -> None:
        return

    def removeGraphicalObjectListener(self, listener: GraphicalObjectListener) -> None:
        return

    def getShapeName(self) -> str:
        return ""
    
    def duplicate(self) -> "GraphicalObject":
        return GraphicalObject([])

    def getShapeID(self) -> str:
        return 0

    def load(self, stack: list, line: str) -> None:
        return

    def save(self) -> str:
        return

    def notifyListeners(self) -> None:
        for listener in self.listeners:
            listener.graphicalObjectChanged(self)

class DocumentModelListener:
    def __init__(self) -> None:
        super().__init__()

    def documentChanged(self, o: GraphicalObject) -> None:
        pass