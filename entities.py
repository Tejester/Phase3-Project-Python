from room import Room
from enum import Enum

class ActivityLevels(Enum):
    SLUMBER = 1
    CRANKY = 2
    DISGRUNTLED = 3
    FURIOUS = 4
    SUICIDAL = 5

class Player:
    def __init__(self,max_hp:int,inventory:dict = {},position:Room = None):
        self.max_hp = max_hp
        self._inventory = inventory
        self._position = position
        self.noise_scale = 0

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
    def position(self):
        return self._position
    
    @position.setter
    def position(self,new_position):
        self._position = new_position
        

class Chameleos:
    def __init__(self,position:Room = None):
        self._position = position

    @property
    def position(self):
        return self._position
    @position.setter
    def position(self,new_position):
        self._position = new_position

    # def adjacent_message(self):
    #     if(self.)