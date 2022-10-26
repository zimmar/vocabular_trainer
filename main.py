from encodings.utf_8 import encode
import json
import os
import random

class Vocable:
    
    def __init__(self, filename):
        if filename is not None and os.path.exists(filename):
            with open(filename) as fl:
                self.data = json.load(fl)
        else:
            self.data = None
            
    def __repr__(self):
        return(json.dumps(self.data, indent=4))
    
    def count(self) -> int:
        return len(self.data)
    
    def _find_word(self, index: int, getvalue: str):
        return self.data[index][getvalue]
        
    def get_vocable(self, index: int) -> str:
        return  self.data[index]['VOCABLE']
    
    def get_tip(self, index: int) -> str:
        return self.data[index]['SUPPORT_TEXT']
    
    def get_sample(self, index: int) -> str:
         return self.data[index]['SAMPLE_SENTENCE']

    def get_translation(self, index: int) -> str:
        return self._find_word(index, 'TRANSLATION')

    def check(self, antwort: str, index: int) -> bool:
        rc = False
        ck = self._find_word(index, 'TRANSLATION')

        if antwort in ck:
            rc = True
        return rc

class History:
    """ Klasse die den Verlauf des Vokabeltest festhält. 
    """
    _queue = []    

    def __init__(self):
        self._queue = []

    def save(self, index: int, points: int):
        p = {}
        p[index] = points
        self._queue.append(p)

    def get_entry(self, index):
        return (self._queue[index])

    def info(self):
        return self._queue

    def is_ready(self, index):
        for i in range(len(self._queue)):
            if index in self._queue[i]:
                return True
        return False

    def count(self):
        return (len(self._queue))

    def __repr__(self):
        return self._queue


def vokabel_test(filename):
     # Laufvariablen
    alle_vokabeln: bool = False # Wurden alle Vokabeln abgearbeitet
    neue_zufalls_zahl: bool = True
    punkte: int = 0

    # Todo: Auswahl des Vokabel Datei festlegen.
    vokabel = Vocable(filename)
    history = History() # für jede Vokabel wird der erreicht Punkte stand festgehalten zur
                        # Späteren analyse
    
    max_punkte = 5 * vokabel.count()
    
    # Durchlaufe alle Vokabeln
    while alle_vokabeln == False:
        # Neue Zufallszahl erstellen. (Reihenfolge der Abfrage wilkürlich.)
        punkte = 5 # Neue Vokabel neue Punkte    
        x = random.randrange(vokabel.count())
        
        while history.is_ready(x):
            x = random.randrange(vokabel.count())
            
        # 1. Vokabel anzeigen
        print(" ===> %s <=== \n" % vokabel.get_vocable(x))
        antwort = input("Lösen oder weiter mit Return: ")
        print("\n")
        
       
        if vokabel.check(antwort, x):
            print(" *** Perfect ***")
            
        else:
            # 2. Hinweistext
            punkte -= 1
            print(" %s \n" % vokabel.get_tip(x))
            antwort = input("Lösen oder weiter mit Return: ")
            print("\n")
            if vokabel.check(antwort, x):
                print("** Good **\n")
            else:
                # 3. Beispietext
                punkte -= 1
                sample = vokabel.get_sample(x)
                for satz in sample:
                    print(" %s " % satz)   
                print("\n")
                antwort = input("Lösen oder weiter mit Return: ")
                print("\n")
                
                if vokabel.check(antwort, x):
                    print(" * OK * \n")
                else:
                    # 4. Übersetzung
                    punkte = 0
                    loesung = vokabel.get_translation(x)
                    for lsg in loesung:
                        print(" %s " % lsg)
                    print("\n")
                    
       
        history.save(x, punkte)
        gesamt_punkte: int = 0        
        if history.count() == vokabel.count(): # Alle Vokabeln durchlaufen.
            print("Das waren alle Vokabeln\n")
            alle_vokabeln = True
            for i in range(history.count()):    # Alle Ergebnisse auflisten.
                v = history.get_entry(i)
                for key, value in v.items():
                    print("%15s : %s --> %s" % ( vokabel.get_vocable(key),
                                           vokabel.get_translation(key),
                                           value))
                    gesamt_punkte += value
            print("Sie habe %s Punkte von %s Punkten erreicht." % (gesamt_punkte, max_punkte))

def vokabel_training(filename):
    vokabel = Vocable(filename)

    for i in range(vokabel.count()):

        print("==> %15s : %s\n" % (vokabel.get_vocable(i), vokabel.get_tip(i)))
        for x in vokabel.get_sample(i):
            print("%s" % x)
        print("\n")
        antwort = input("Weiter mit Return: ")
        print("\n")
        print("%s\n\n" % vokabel.get_translation(i))



def main():
   vokabel_training("modul_a.json")


if __name__ == '__main__':
    main()



    