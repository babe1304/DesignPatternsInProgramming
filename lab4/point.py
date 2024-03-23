class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        return iter([self.x, self.y])

    def translate(self, pd: "Point") -> "Point":
        return Point(self.x + pd.x, self.y + pd.y)

    def difference(self, pd: "Point") -> "Point":
        return Point(self.x - pd.x, self.y - pd.y)