from room import Room

class Player:
    def __init__(self,max_hp:int,inventory:dict = {},position:Room = None):
        self.max_hp = max_hp
        self._inventory = inventory
        self._position = position
        self._score = 0

    @property
    def inventory(self):
        return self._inventory
    @inventory.setter
    def inventory(self,inventory):
        self._inventory = inventory

    def take_damage(self,damage):
        self.max_hp -= damage
    
    def heal_damage(self,heal):
        self.max_hp += heal
    
    @property
    def curr_score(self):
        return self._score
    
    @curr_score.setter
    def curr_score(self, value):
        self._score = value

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self,new_position):
        self._position = new_position
        

class Dragon:
    pass