import json
import os

class Vocable:
    
    _choices = ["verb", "noun", "adjective"]
 
    def __init__(self, filename):
        if filename is not None and os.path.exists(filename):
            with open(filename) as fl:
                self.data = json.load(fl)
        else:
            self.data = None
            
    def __repr__(self):
        return (self.data)
    
    def count(self) -> int:
        return len(self.data)
    
    def _find_word(self, index: int, getvalue: str, choice: str=None):
        if choice != None and (choice in self._choices):
            for i in range(len(self.data[index][getvalue])):
                if choice in self.data[index][getvalue][i]:
                    return self.data[index][getvalue][i][choice]
        #    return self.data[index][getvalue]
        # else:
        return self.data[index][getvalue]
    
    def get_vocable(self, index: int, choice: str=None) -> str:
        return self._find_word(index, 'VOCABLE', choice)
    
    def get_tip(self, index: int, choice: str=None):
        return self._find_word(index, 'SUPPORT_TEXT', choice)
    
    def get_sample(self, index: int, choice: str=None):
         return self._find_word(index, 'SAMPLE_SENTENCE', choice)

     
    def get_translation(self, index: int, choice: str=None):
        return self._find_word(index, 'TRANSLATION', choice)
  
    
    

# read file

voc = Vocable('modul1.json')

print(voc.count())
print(voc.get_vocable(0, 'verb'))
print(voc.get_tip(0, 'verb'))
print(voc.get_sample(0, 'verb'))
print(voc.get_translation(0, 'verb'))
