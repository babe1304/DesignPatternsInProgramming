class VelikoSlovo:
    def __init__(self) -> None:
        pass
    def getName(self):
        return "VelikoSlovo"
    
    def getDescription(self):
        return "Plugin koji prolazi kroz dokument i svako prvo slovo riječi mijenja u veliko ('ovo je tekst' ==> 'Ovo Je Tekst')"
    
    def execute(self, model, undoManager=None, clipboardStack=None):
        new_lines = []
        for line in model.lines:
            words = line.split(" ")
            upper = []
            for word in words:
                upper.append(word.title())
            new_lines.append("".join(upper))
        model.lines = new_lines
        model.notifyTextObservers()
        return {}