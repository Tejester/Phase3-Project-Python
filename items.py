class Items:
    cloth = 0
    
    def __init__(self):
        self._bandage = False

    @property
    def bandaged(self):
        return self._bandage
    
    @bandaged.setter
    def bandaged(self, value):
        self._bandage = value
