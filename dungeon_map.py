from __future__ import annotations
from room import Room
import random
import click
from direction import Direction
import faker
class DungeonMap:
    def __init__(self):
        self.rooms = {}
        self.player_location = None

    def add_room(self, room:Room):
        if room not in self.rooms:
            self.rooms[room] = {}

    def add_connection(self, room1:Room, room2:Room, direction:Direction.value):
        if room1 not in self.rooms:
            self.add_room(room1)
        if room2 not in self.rooms:
            self.add_room(room2)
        self.rooms[room1][direction] = room2
        self.rooms[room2][opposite_direction(direction)] = room1

    def set_player_location(self, room:Room):
        self.player_location = room

    def move_player(self, direction:Direction.value):
        if direction not in self.rooms[self.player_location]:
            click.echo("You can't go that way!")
            return False
        self.player_location = self.rooms[self.player_location][direction]
        return True


def opposite_direction(direction:Direction.value):
    if direction == Direction.NORTH.value:
        return Direction.SOUTH.value
    elif direction == Direction.NORTHEAST.value:
        return Direction.SOUTHWEST.value
    elif direction == Direction.EAST.value:
        return Direction.WEST.value
    elif direction == Direction.SOUTHEAST.value:
        return Direction.NORTHWEST.value
    elif direction == Direction.SOUTH.value:
        return Direction.NORTH.value
    elif direction == Direction.SOUTHWEST.value:
        return Direction.NORTHEAST.value
    elif direction == Direction.WEST.value:
        return Direction.EAST.value
    elif direction == Direction.NORTHWEST.value:
        return Direction.SOUTHEAST.value
    else:
        raise ValueError("Invalid direction: {}".format(direction))
    
def generate_dungeon(num_rooms):
    fake = faker.Generator().add_provider(faker.providers.lorem)

    # First room is always room 1
    dungeon = DungeonMap()
    first_room = Room(1)
    dungeon.add_room(first_room)
    dungeon.set_player_location(first_room)
    num_created = 1
    while num_created < num_rooms:
        random_room = random.choice(list(dungeon.rooms.keys()))
        direction = random.choice(list(Direction))
        if direction.value not in dungeon.rooms[random_room]:
            if random.random() < 0.8:
                num_created += 1
                new_room_id = num_created
                new_room = Room(new_room_id)
                dungeon.add_room(new_room)
                dungeon.add_connection(random_room,new_room,direction.value)
    return dungeon

# class DungeonMap:
#     def __init__(self):
#         self.rooms = {}
#         self.player_location = None

#     def add_room(self, room_id):
#         if room_id not in self.rooms:
#             self.rooms[room_id] = {}

#     def add_connection(self, room1_id, room2_id, direction:Direction):
#         if room1_id not in self.rooms:
#             self.add_room(room1_id)
#         if room2_id not in self.rooms:
#             self.add_room(room2_id)
#         self.rooms[room1_id][direction] = room2_id
#         self.rooms[room2_id][opposite_direction(direction)] = room1_id

#     def set_player_location(self, room_id):
#         self.player_location = room_id

#     def move_player(self, direction:Direction):
#         if direction not in self.rooms[self.player_location]:
#             click.echo("You can't go that way!")
#             return False
#         self.player_location = self.rooms[self.player_location][direction]
#         return True


# def opposite_direction(direction:Direction):
#     if direction == Direction.NORTH:
#         return Direction.SOUTH
#     elif direction == Direction.NORTHEAST:
#         return Direction.SOUTHWEST
#     elif direction == Direction.EAST:
#         return Direction.WEST
#     elif direction == Direction.SOUTHEAST:
#         return Direction.NORTHWEST
#     elif direction == Direction.SOUTH:
#         return Direction.NORTH
#     elif direction == Direction.SOUTHWEST:
#         return Direction.NORTHEAST
#     elif direction == Direction.WEST:
#         return Direction.EAST
#     elif direction == Direction.NORTHWEST:
#         return Direction.SOUTHEAST
#     else:
#         raise ValueError("Invalid direction: {}".format(direction))
    
# def generate_dungeon(num_rooms):
#     dungeon = DungeonMap()
#     dungeon.add_room(1,Room())
#     dungeon.set_player_location(1)
#     num_created = 1
#     while num_created < num_rooms:
#         room_id = random.randint(1,num_created)
#         direction = random.choice(list(Direction))
#         if direction not in dungeon.rooms[room_id]:
#             if random.random() < 0.8:
#                 num_created += 1
#                 new_room_id = num_created
#                 dungeon.add_room(new_room_id,Room())
#                 dungeon.add_connection(room_id,new_room_id,direction)
#     return dungeon

# # This class exists to represent the dungeon map as a graph
# class DungeonMap:
#     def __init__(self,min_rooms:int,max_rooms:int):
#         self.graph = {}
#         self.rooms = []
#         self.min_rooms = min_rooms
#         self.max_rooms = max_rooms
#         self.current_room = None # This is the current room
#         self.connected_room_count = 0 # This is the number of rooms in the dungeon

#     @property
#     def room_count(self):
#         return self.room_count
#     @property
#     def current_room(self):
#         print(self.current_room)
#         return self.current_room
    
#     @current_room.setter
#     def current_room(self,value):
#         self.current_room = value
    
#     def get_dungeon_graph(self):
#         return self.graph
    
#     def generate_rooms(self):
#         number_of_rooms = Random.randint(self.min_rooms,self.max_rooms)
#         # Create rooms of random types and add them to the room list
#         for i in range(number_of_rooms):
#             self.rooms.append(Room("brick-walled room"),[])

#     # Check if current room already has a direction
#     def has_direction(self,direction:Direction) -> bool:
#         if direction in self.current_room:
#             return True
#         else:
#             return False
        

    
#     @property
#     def connected_room_count(self):
#         return self.room_count
    
#     @room_count.setter
#     def connected_room_count(self,value):
#         self.room_count = value

#     # For ordinary hallways
#     def add_undirected_edge(self,u:Room,v:Room,direction:Direction):
#         if u not in self.graph:
#             self.graph[u] = []
#         if v not in self.graph:
#             self.graph[v] = []
#         self.graph[u].append({direction:v})
#         self.graph[v].append({direction:u})
#         if self.room_count == 0:
#             self.current_room = self.graph[u]
#         self.room_count += 1
    
#     def get_connections(self,rooms:dict):
#         # This function will return a dict of rooms that are connected to the current room
#         return self.graph[self.current_room]
    
#     # Move in a valid direction
#     def travel(self,direction:Direction):
#         if direction in self.graph[self.current_room]:
#             self.current_room = self.graph[self.current_room]
#         else:
#             print("You can't go that way!")
#             return False
#         return True

