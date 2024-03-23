from point import Point
from models import GraphicalObject
from CompositeShape import CompositeShape

class State:
    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        pass

    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        pass

    def mouseDragged(self, mousePoint: Point) -> None:
        pass

    def keyPressed(self, keyEvent) -> None:
        pass

    def afterDraw(self) -> None:
        pass

    def onLeaving(self) -> None:
        pass

class AddShapeState(State):
    def __init__(self, model, prototype=None, canvas=None) -> None:
        self.model = model
        self.prototype = prototype
        self.canvas = canvas
        self.current: GraphicalObject = None

    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        self.current = self.prototype.duplicate()
        self.current.translate(mousePoint)
        self.current.render(self.canvas)

    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        self.model.addGraphicalObject(self.current)
        self.current = None

    def mouseDragged(self, mousePoint: Point) -> None:
        if self.current == None: return
        self.current.setHotPoint(1, mousePoint)
        self.canvas.documentChanged(self)
        self.current.render(self.canvas)

class SelectShapeState(State):
    def __init__(self, model, canvas=None) -> None:
        self.model = model
        self.canvas = canvas
        self.current = None

    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        if not ctrlDown: 
            if len(self.model.selectedObjects) != 0:
                for o in self.model.selectedObjects:
                    o.setSelected(False)
                self.model.selectedObjects.clear()
        ob = self.model.findSelectedGraphicalObject(mousePoint)
        if ob != None:
            ob.setSelected(True)
            if len(self.model.selectedObjects) == 0:
                self.current = ob
                ob.setHotPointSelected(ob.findSelectedHotPoint(mousePoint))
            self.model.selectedObjects.append(ob)
        else:
            self.current = None
        self.canvas.documentChanged(ob)
        print(self.current)

    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        self.current = None

    def mouseDragged(self, mousePoint: Point) -> None:
        if self.current == None: return
        hp = self.current.getSelectedHotPoint()
        if hp != None:
            self.current.setHotPoint(self.current.hot_points.index(hp), mousePoint)
            self.canvas.documentChanged(self.current)
            self.current.render(self.canvas)
        else:
            self.current.translate(mousePoint.difference(self.current.getCenter()))
            self.canvas.documentChanged(self.model.selectedObjects)
            self.current.render(self.canvas)

    def keyPressed(self, keyEvent) -> None:
        if len(self.model.selectedObjects) == 0 and self.current == None: return
        
        if keyEvent.keycode == 42:
            if len(self.model.selectedObjects) == 1: return
            new_obj = CompositeShape([o for o in self.model.selectedObjects])
            new_obj.setSelected(True)
            for o in self.model.selectedObjects.copy():
                self.model.removeGraphicalObject(o)
            self.model.addGraphicalObject(new_obj)
            self.model.selectedObjects.append(new_obj)
            self.canvas.documentChanged(new_obj)
            new_obj.render(self.canvas)
            self.current = new_obj
            return
        elif keyEvent.keycode == 30:
            if len(self.model.selectedObjects) != 1 and type(self.current) != CompositeShape and self.current == None: return
            self.current = self.model.selectedObjects[0]
            self.model.removeGraphicalObject(self.current)
            self.current.setSelected(False)
            self.model.selectedObjects.clear()
            for o in self.current.objects:
                o.setSelected(True)
                self.model.addGraphicalObject(o)
                self.model.selectedObjects.append(o)
                self.canvas.documentChanged(self.model.selectedObjects)
                o.render(self.canvas)
            self.current = None
            return
        for o in self.model.selectedObjects:
            if keyEvent.keycode == 111:
                o.translate(Point(0, -4))
            elif keyEvent.keycode == 113:
                o.translate(Point(-4, 0))
            elif keyEvent.keycode == 114:
                o.translate(Point(4, 0))
            elif keyEvent.keycode == 116:
                o.translate(Point(0, 4))
            elif keyEvent.keycode == 21:
                self.model.increaseZ(o)
            elif keyEvent.keycode == 61:
                self.model.decreaseZ(o)
            self.canvas.documentChanged(self.model.selectedObjects)
            o.render(self.canvas)

    def afterDraw(self) -> None:
        for go in self.model.selectedObjects:
            bb = go.getBoundingBox()
            self.canvas.create_rectangle(bb.x1, bb.y1, bb.x2, bb.y2)
        if len(self.model.selectedObjects) == 1:
            go = self.model.selectedObjects[0]
            for hp in go.hot_points:
                if go.isHotPointSelected(go.hot_points.index(hp)):
                    self.canvas.create_rectangle(hp.x - 4, hp.y - 4, hp.x + 4, hp.y + 4, fill="green")
                else:          
                    self.canvas.create_rectangle(hp.x - 4, hp.y - 4, hp.x + 4, hp.y + 4)

    def onLeaving(self) -> None:
        for o in self.model.selectedObjects:
            o.setSelected(False)
        self.model.selectedObjects.clear()
        self.canvas.documentChanged(None)

class EraserState(State):
    def __init__(self, model, canvas=None) -> None:
        self.model = model
        self.canvas = canvas
        self.prev = None
        self.current = None
        self.objects = []

    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        self.current = mousePoint
        self.prev = mousePoint

    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        self.current = None
        if len(self.objects) == 0: 
            self.canvas.documentChanged(None)
            return
        for o in self.objects.copy():
            self.model.removeGraphicalObject(o)
        self.objects.clear()

    def mouseDragged(self, mousePoint: Point) -> None:
        if self.current == None: return
        obj = self.model.findSelectedGraphicalObject(mousePoint)
        if obj != None:
            if obj not in self.objects:
                self.objects.append(obj)
        self.canvas.create_line(self.prev.x, self.prev.y, mousePoint.x, mousePoint.y, fill="orange", width=3)
        self.prev = self.current
        self.current = mousePoint