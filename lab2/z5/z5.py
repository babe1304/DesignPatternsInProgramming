import sys
import time
import datetime
from abc import ABC, abstractmethod

class SlijedBrojeva:
    def __init__(self, izvor):
        self.kolekcija = []
        self.izvor = izvor
        self.listeners = []
    
    def dodajListenera(self, listener):
        self.listeners.append(listener)
    
    def odbaciListenera(self, listener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def obavijesti(self):
        for li in self.listeners:
                li.posao(self.kolekcija)

    def kreni(self):
        while True:
            sljBr = int(self.izvor())
            if sljBr == -1:
                break
            self.kolekcija.append(sljBr)
            self.obavijesti()
            time.sleep(1)
        return

class TipkovnickiIzvor:
    def __init__(self) -> None:
        self.input = sys.stdin.readlines()

    def __call__(self):
        i = self.input.pop()
        return i if type(i) == int else -1
    
class DatotecniIzvor:
    def __init__(self, izvor) -> None:
        with open(izvor) as izv:
            self.input = izv.readlines()
        
    def __call__(self):
        i = self.input.pop(0)
        return i
    
class Listener(ABC):
    @abstractmethod
    def posao(self):
        pass
    
class TekstDatotekaListener(Listener):
    def __init__(self, output):
        super().__init__()
        self.output = output

    def posao(self, kol):
        with open(self.output, "w") as out:
            out.write(str(datetime.datetime.now()) + "\n")
            for el in kol:
                out.write(str(el) + "\n")
    
class SumElementListener(Listener):
    def __init__(self) -> None:
        super().__init__()

    def posao(self, kol):
        print(f"Sum: {sum(kol)}")

class AvgElementListener(Listener):
    def __init__(self) -> None:
        super().__init__()

    def posao(self, kol):
        print(f"Avg: {sum(kol)/len(kol)}")

class MedElementListener(Listener):
    def __init__(self) -> None:
        super().__init__()

    def posao(self, kol):
        cp = kol.copy()
        cp.sort()
        mid = (len(kol) - 1) // 2
        if len(kol) % 2 == 0:
            mid = int(mid)
            print(f"Med: {(cp[mid]+cp[mid + 1])/2}")
        else:
            print(f"Med: {cp[mid]}")

if __name__=="__main__":
    inp = "in.txt"
    out = "out.txt"

    di = DatotecniIzvor(inp)
    avg = AvgElementListener()
    med = MedElementListener()
    sm = SumElementListener()
    tekst = TekstDatotekaListener(out)
    
    sb = SlijedBrojeva(di)
    sb.dodajListenera(avg)
    sb.dodajListenera(med)
    sb.dodajListenera(sm)
    sb.dodajListenera(tekst)

    sb.kreni()