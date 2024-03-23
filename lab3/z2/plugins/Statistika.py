class Statistika:
    def __init__(self, model) -> None:
        self.model = model
        
    def getName(self):
        return "Statistika"
    
    def getDescription(self):
        return "Plugin koji broji koliko ima redaka, riječi i slova u dokumentu i to prikazuje korisniku u dijalogu."
    
    def execute(self, undoManager=None, clipboardStack=None):
        stats = {"lines":0, "words":0, "chars":0}
        for line in self.model.lines:
            stats["lines"] += 1
            words = line.split(" ")
            for word in words:
                stats["words"] += 1
                for letter in word:
                    stats["chars"] += 1
        return stats