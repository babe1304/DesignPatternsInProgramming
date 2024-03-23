from Renderer import Renderer
from point import Point
from typing import List

class SVGRendererImpl(Renderer):
    def __init__(self, filename="") -> None:
        super().__init__()
        self.filename = filename
        self.lines = []
        self.lines.append("<svg xmlns=\"http://www.w3.org/2000/svg\">\n")

    def close(self) -> None:
        self.lines.append("</svg>\n")
        with open(self.filename, "a") as f:
            for line in self.lines:
                f.write(line)

    def drawLine(self, s: Point, e: Point) -> None:
        self.lines.append(f"<line x1=\"{s.x}\" y1=\"{s.y}\" x2=\"{e.x}\" y2=\"{e.y}\" style=\"stroke:rgb(255,0,0);stroke-width:2\" />\n")

    def fillPolygon(self, points: List[Point]) -> None:
        line="<polygon points=\""
        for p in points:
            line+=f"{p.x},{p.y} "
        line+="\" style=\"fill:blue;stroke:red;stroke-width:2\" />\n"
        self.lines.append(line)