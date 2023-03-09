import click
from enum import Enum
from direction import Direction

class InteractionMessages(Enum):
    MOVE_BUT_DIRECTION_NOT_EXIST = "There is no room in that direction."

# # class KeyType(Enum):
# #     BRONZE = "BRONZE"
# #     SILVER = "SILVER"
# #     GOLD = "GOLD"

# # class Key:
# #     def __init__(self,key_type:KeyType):
# #         self.key_type = key_type

# # class DoorType(Enum):
# #     BRONZE = "BRONZE"
# #     SILVER = "SILVER"
# #     GOLD = "GOLD"

# # class Door:
# #     def __init__(self,name:DoorType,direction:Direction,is_open:bool=False,is_locked:bool=False,is_broken:bool=False,is_trapped:bool=False):
# #         self._name = name
# #         self._direction = direction
# #         self._is_open = is_open
# #         self._is_locked = is_locked
# #         self._is_broken = is_broken
# #         self._is_trapped = is_trapped
    
#     @property
#     def direction(self):
#         return self._direction.name
#     @direction.setter
#     def direction(self,door_direction:Direction):
#         self._direction = door_direction

#     @property
#     def name(self):
#         return self._name
#     @name.setter
#     def name(self,door_name:DoorType):
#         self._name = door_name
    
#     @property
#     def is_open(self):
#         return self._is_open
#     @is_open.setter
#     def is_open(self,door_state:bool):
#         self._is_open = door_state
#     @property
#     def is_locked(self):
#         return self._is_locked
#     @is_locked.setter
#     def is_locked(self,door_state:bool):
#         self._is_locked = door_state
#     @property
#     def is_broken(self):
#         return self._is_broken
#     @is_broken.setter
#     def is_broken(self,door_state:bool):
#         self._is_broken = door_state
#     @property
#     def is_trapped(self):
#         return self._is_trapped
#     @is_trapped.setter
#     def is_trapped(self,door_state:bool):
#         self._is_trapped = door_state

#     # open a door
#     def open(self):
#         if self._is_broken:
#             click.echo(InteractionMessages.OPEN_BUT_BROKEN.value)
#         elif self._is_locked:
#             click.echo(InteractionMessages.OPEN_BUT_LOCKED.value)
#         elif self._is_open:
#             click.echo(InteractionMessages.OPEN_BUT_OPENED.value)
#         elif self._is_trapped:
#             click.echo(InteractionMessages.OPEN_BUT_TRAPPED.value)
#         elif not self._is_open:
#             self._is_open = True
#             click.echo(InteractionMessages.OPEN_SUCCESS.value)
#         elif self._is_open:
#             self._is_open = False
#             click.echo(InteractionMessages.CLOSE_SUCCESS.value) 

#     # close a door
#     def close(self):
#         if self._is_broken:
#             click.echo(InteractionMessages.CLOSE_BUT_BROKEN.value)
#         elif self._is_trapped:
#             click.echo(InteractionMessages.CLOSE_BUT_TRAPPED.value)
#         elif self._is_open:
#             self._is_open = False
#             click.echo(InteractionMessages.CLOSE_SUCCESS.value)
#         elif not self._is_open:
#             click.echo(InteractionMessages.CLOSE_BUT_CLOSED.value)
        

    
#     # lock or unlock the door
#     def lock(self):
#         if not self._is_broken:
#             if self._is_locked:
#                 self._is_locked = False
#                 click.echo("You unlock the door.")
#             else:
#                 self._is_locked = True
#                 click.echo("You lock the door.")
#         else:
#             click.echo("How do you expect to lock a broken door?")
    
#     # break the door
#     def break_door(self):
#         if not self._is_broken:
#             self._is_broken = True
#             click.echo("You break the door.")
#         else:
#             click.echo("The door is already broken.")
    
    

# These are the nodes of the graph
class Room:
    def __init__(self,room_id,room_name,contents:dict={}):
        # self.surr = surr
        # self._desc = desc
        self.room_id = room_id
        self._room_name = room_name
        self._contents = contents
        self.is_exit = False
        self._shrimpified = False

    # @property
    # def desc(self):
    #     return self._desc
    # @desc.setter
    # def desc(self,desc):
    #     self._desc = desc
    
    @property
    def shrimpified(self):
        return self._shrimpified
    @shrimpified.setter
    def shrimpified(self,shrimpified:bool):
        self._shrimpified = shrimpified
        
    @property
    def contents(self):
        return self._contents
    @contents.setter
    def contents(self,contents:dict):
        self._contents = contents

    # @property
    # def neighbors(self):
    #     return self._neighbors
    # @neighbors.setter
    # def neighbors(self,neighbors):
    #     self._neighbors = neighbors
    @property
    def is_exit(self):
        return self._is_exit
    def is_exit(self,is_exit:bool):
        self._is_exit = is_exit
    @property
    def room_name(self):
        return self._room_name
    
    @room_name.setter
    def room_name(self,name):
        self._room_name = name
    
    # @property
    # def door(self):
    #     return self._door
    
    # @door.setter
    # def door(self,door:Door):
    #     self._door = door
    
    # @property
    # def contents(self):
    #     return self._contents
    
    # @contents.setter
    # def contents(self,contents):
    #     self._contents = contents
    

