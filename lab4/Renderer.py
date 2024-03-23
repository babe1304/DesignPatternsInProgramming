import abc
from point import Point
from typing import List

class Renderer(abc.ABC):
    @abc.abstractmethod
    def drawLine(self, s: Point, e: Point) -> None:
        pass

    @abc.abstractmethod
    def fillPolygon(self, points: List[Point]) -> None:
        pass