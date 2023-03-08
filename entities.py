from room import Room
from enum import Enum

class ActivityLevels(Enum):
    SLUMBER = 1
    CRANKY = 2
    DISGRUNTLED = 3
    FURIOUS = 4
    BLOODTHIRSTY = 5

class Player:
    def __init__(self,max_hp:int,inventory:dict = {},position:Room = None):
        self.max_hp = max_hp
        self._inventory = inventory
        self._position = position
        self._shrimp_count = 80

    @property
    def shrimp_count(self):
        return self._shrimp_count
    
    @shrimp_count.setter
    def shrimp_count(self,value):
        self._shrimp_count = value

    def shrimpify(self,room:Room):
        room.shrimpified = True

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
        self.activity_level = ActivityLevels.SLUMBER

    @property
    def position(self):
        return self._position
    @position.setter
    def position(self,new_position):
        self._position = new_position

    def update_activity_level(self,noise_scale:int):
        if noise_scale <= 5:
            self.activity_level = ActivityLevels.SLUMBER
        elif 6 <= noise_scale <= 10:
            self.activity_level = ActivityLevels.CRANKY
        elif 11 <= noise_scale <= 15:
            self.activity_level = ActivityLevels.DISGRUNTLED
        elif 16 <= noise_scale <= 20:
            self.activity_level = ActivityLevels.FURIOUS
        elif noise_scale >= 21:
            self.activity_level = ActivityLevels.BLOODTHIRSTY

    def eat_shrimp(self,room:Room):
        room.shrimpified = False