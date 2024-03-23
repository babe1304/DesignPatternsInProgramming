from point import Point

class Rectangle:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def __iter__(self):
        return iter([self.x1, self.y1, self.x2, self.y2])