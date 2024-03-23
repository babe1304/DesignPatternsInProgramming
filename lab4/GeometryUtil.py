from point import Point
import math

class GeomatryUtil:
    @staticmethod
    def distanceFromPoint(p1: Point, p2: Point) -> float:
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
    
    @staticmethod
    def distanceFromLineSegment(s: Point, e: Point, p: Point):
        if s.x == e.x and s.y == e.y:
            return GeomatryUtil.distanceFromPoint(s, p)
        else:
            return abs((e.x - s.x)*(s.y - p.y) - (s.x - p.x)*(e.y - s.y)) / GeomatryUtil.distanceFromPoint(s, e)