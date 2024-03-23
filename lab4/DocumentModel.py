from models import GraphicalObject, GraphicalObjectListener, DocumentModelListener
from point import Point

class DocumentModel:
    STATIC_PROXIMITY = 7

    def __init__(self) -> None:
        self.objects = []
        self.listeners = []
        self.selectedObjects = []
        self.goListener = GraphicalObjectListener(self)

    def list(self) -> tuple:
        return self.roObjects
    
    def clear(self) -> None:
        for o in self.objects:
            o.removeGraphicalObjectListener(self.goListeners)
        self.objects.clear()

    def addGraphicalObject(self, obj: GraphicalObject) -> None:
        obj.addGraphicalObjectListener(self.goListener)
        self.objects.append(obj)
        self.notifyListeners(obj)

    def removeGraphicalObject(self, obj: GraphicalObject) -> None:
        obj.removeGraphicalObjectListener(self.goListener)
        if obj in self.selectedObjects:
            self.selectedObjects.remove(obj)
        self.objects.remove(obj)
        self.notifyListeners(obj)

    def addDocumentModelListener(self, l: DocumentModelListener) -> None:
        self.listeners.append(l)

    def removeDocumentModelListener(self, l: DocumentModelListener) -> None:
        self.listeners.remove(l)

    def notifyListeners(self, go: GraphicalObject) -> None:
        for l in self.listeners:
            l.documentChanged(go)
    
    def increaseZ(self, go: GraphicalObject) -> None:
        if go in self.objects:
            index = self.objects.index(go)
            if index < len(self.objects) - 1:
                self.objects[index], self.objects[index + 1] = self.objects[index + 1], self.objects[index]
                self.notifyListeners(go)

    def decreaseZ(self, go: GraphicalObject) -> None:
        if go in self.objects:
            index = self.objects.index(go)
            if index > 0:
                self.objects[index], self.objects[index - 1] = self.objects[index - 1], self.objects[index]
                self.notifyListeners(go)

    def findSelectedGraphicalObject(self, point: Point) -> GraphicalObject:
        for o in self.objects:
            if o.selectionDistance(point) <= DocumentModel.STATIC_PROXIMITY:
                return o
        return None
    
    def findSelectedHotPoint(self, o: GraphicalObject, point: Point) -> int:
        for i in range(o.getNumberOfHotPoints()):
            if o.getHotPointDistance(i, point) <= DocumentModel.STATIC_PROXIMITY:
                return i
        return -1
    
    def graphicalObjectChanged(self, o: GraphicalObject):
        self.notifyListeners(o)