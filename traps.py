import random

class Trap:
    traps = {
        "crossbow":{"damage" : 10 },
        "hole":{"damage": 5},
        "beartrap":{"damage": 8}
    }

    def __init__(self):
        self._found = False
        self.type = random.choice(list(self.traps.keys()))
        self._bleed = False

    @property
    def found(self):
        return self._found
    
    @found.setter
    def found(self,value):
        self._found = value

    @property
    def bleed(self):
        return self._bleed
    
    @bleed.setter
    def bleed(self, value):
        self._bleed = value


   

    
