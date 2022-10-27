import os
import random
import argparse

from utils import Vocable
from utils import History


def vokabel_test(filename):
    """ Vokabel Test durchführen.

        Alle Vokabeln werden in zufälliger Reihenfolge abgefragt.
        Zu jeder Vokabel wird ein Punktestand festgehalten.
        Die Maximal Punkte erhält man, wenn die Lösung direkt mit der Vokabeldarstellung gelöst wird.
        Ein Punkt abzug erhält man, wenn mehr Hilfeleistung angezeigt wird.
        0 Punkte wenn die Übersetzung angezeigt werden muss.
    
        Parameters:
        -----------

        filename: str
            Qualifizierter Dateiname der Vokabeldatei.

        Returns
        -------
        :None:

    """
     # Laufvariablen
    alle_vokabeln: bool = False # Wurden alle Vokabeln abgearbeitet
    neue_zufalls_zahl: bool = True # FLag 
    punkte: int = 0 # erreichte Punkte je durchlauf neu

    # Todo: Auswahl des Vokabel Datei festlegen.
    vokabel = Vocable(filename)
    history = History() # für jede Vokabel wird der erreicht Punkte stand festgehalten zur
                        # Späteren analyse
    
    max_punkte = 5 * vokabel.count() # Maximal zu erreichende Punkte.
    
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
    """ Vokabel Training
        Alle Vokabeln werden nacheinander ausgegeben. 
        Es werden alle Informationen zur Vokabel ausgeben.
        Anschließend die Übersetzung.
        
    """
    vokabel = Vocable(filename)

    for i in range(vokabel.count()):
        print("\n\n")
        print("==> %15s : %s\n" % (vokabel.get_vocable(i), vokabel.get_tip(i)))
        for x in vokabel.get_sample(i):
            print("    %15s   %s" % (" ", x))
        print("\n")
        antwort = input("Weiter mit Return: ")
        print("\n")
        print("%s\n\n" % vokabel.get_translation(i))



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Vokabel Training")
    parser.add_argument("-t", "--test", action="store_false", help="Vokabel Test durchführen.")
    parser.add_argument("-p", "--praxis", action="store_false", help="Vokabel Praxis durchlaufen.")
    parser.add_argument("-m", "--modul", default="vocabular.json", help="Modulname")
    parser.add_argument("-l", "--language", default='en', help="Sprachauswahl")

    args = parser.parse_args(['-t'])

    print(args)
    
    if args.test:
        vokabel_training(os.path.join('sprachen/en/unit_a', args.modul))

    if args.praxis:
        vokabel_test(os.path.join('sprachen/en/unit_a', args.modul))


    
