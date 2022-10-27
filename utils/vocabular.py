# coding:utf-8
import json
import os


class Vocable:
    """ Hilsklasse zum Arbeiten mit Vokabeln """
    
    def __init__(self, filename):
        """ Einlesen der Vokabeldatei """
        if filename is not None and os.path.exists(filename):
            with open(filename) as fl:
                self.data = json.load(fl)
        else:
            self.data = None
            
    def __repr__(self):
        """ Ausgabe aller Vokabeln """
        return(json.dumps(self.data, indent=4))
    
    def count(self) -> int:
        """ Anzahl der Vokabeln """
        return len(self.data)
    
    def _find_word(self, index: int, getvalue: str) -> str:
        """ Suchen einer Vokabel """
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
        """ Prüft ob die Antwort mit der Übersetzung der 
        übereinstimmt."""
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
        """ Vokabel ist schon in der Queue eingetragen. """
        for i in range(len(self._queue)):
            if index in self._queue[i]:
                return True
        return False

    def count(self):
        """ Anzahl der Einträge in der Queue """
        return (len(self._queue))

    def __repr__(self):
        return self._queue
