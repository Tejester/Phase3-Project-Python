import click
from enum import Enum

class KeyType(Enum):
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"

class Key:
    def __init__(self,key_type:KeyType):
        self.key_type = key_type

class DoorType(Enum):
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"

class Door:
    def __init__(self,is_open:bool=False,is_locked:bool=False,is_broken:bool=False,is_trapped:bool=False):
        self._is_open = is_open
        self._is_locked = is_locked
        self._is_broken = is_broken
        self._is_trapped = is_trapped
    
    @property
    def is_open(self):
        return self._is_open
    @is_open.setter
    def is_open(self,door_state:bool):
        self._is_open = door_state
    @property
    def is_locked(self):
        return self._is_locked
    @is_locked.setter
    def is_locked(self,door_state:bool):
        self._is_locked = door_state
    @property
    def is_broken(self):
        return self._is_broken
    @is_broken.setter
    def is_broken(self,door_state:bool):
        self._is_broken = door_state
    @property
    def is_trapped(self):
        return self._is_trapped
    @is_trapped.setter
    def is_trapped(self,door_state:bool):
        self._is_trapped = door_state

    # open or close the door
    def interact(self):
        if not self._is_broken:
            if self._is_locked:
                click.echo("The door is locked.")
            elif self._is_open:
                self._is_open = False
                click.echo("You close the door.")
            elif self._is_open and self._is_trapped:
                click.echo("You open the door, but it's trapped!")
            elif not self._is_open:
                self._is_open = True
                click.echo("You open the door.")
            
        else:
            click.echo("Don't be an idiot, the door is clearly broken.")
    
    # lock or unlock the door
    def lock(self):
        if not self._is_broken:
            if self._is_locked:
                self._is_locked = False
                click.echo("You unlock the door.")
            else:
                self._is_locked = True
                click.echo("You lock the door.")
        else:
            click.echo("How do you expect to lock a broken door?")
    
    # break the door
    def break_door(self):
        if not self._is_broken:
            self._is_broken = True
            click.echo("You break the door.")
        else:
            click.echo("The door is already broken.")
    
    

# These are the nodes of the graph
class Room:
    def __init__(self,room_id,name,door:Door=None,contents=[]):
        # self.surr = surr
        # self.desc = desc
        self.room_id = room_id
        self.name = name
        self._door = door
        self.contents = contents
    
    @property
    def room_name(self):
        return self.name
    
    @property
    def door(self):
        return self._door
    
    @door.setter
    def door(self,door:Door):
        self._door = door

