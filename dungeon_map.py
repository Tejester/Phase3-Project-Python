from __future__ import annotations
from room import Room,InteractionMessages
import random
import click
from direction import Direction
from entities import Player
from treasure import generate_treasures
import string

adjectives = ["abandoned","aberrant","abhorrent","abiding","abject","ablaze","able","abnormal","aboard","aboriginal","abortive","abounding","abrasive","abrupt","absent","absorbed","absorbing","abstracted","absurd","abundant","abusive","acceptable","accessible","accidental","accurate","acid","acidic","acoustic","acrid","actually","ad hoc","adamant","adaptable","addicted","adhesive","adjoining","adorable","adventurous","afraid","aggressive","agonizing","agreeable","ahead","ajar","alcoholic","alert","alike","alive","alleged","alluring","aloof","amazing","ambiguous","ambitious","amuck","amused","amusing","ancient","angry","animated","annoyed","annoying","anxious","apathetic","aquatic","aromatic","arrogant","ashamed","aspiring","assorted","astonishing","attractive","auspicious","automatic","available","average","awake","aware","awesome","awful","axiomatic","bad","barbarous","bashful","bawdy","beautiful","befitting","belligerent","beneficial","bent","berserk","best","better","bewildered","big","billowy","bite-sized","bitter","bizarre","black","black-and-white","bloody","blue","blue-eyed","blushing","boiling","boorish","bored","boring","bouncy","boundless","brainy","brash","brave","brawny","breakable","breezy","brief","bright","bright","broad","broken","brown","bumpy","burly","bustling","busy","cagey","calculating","callous","calm","capable","capricious","careful","careless","caring","cautious","ceaseless","certain","changeable","charming","cheap","cheerful","chemical","chief","childlike","chilly","chivalrous","chubby","chunky","clammy","classy","clean","clear","clever","cloistered","cloudy","closed","clumsy","cluttered","coherent","cold","colorful","colossal","combative","comfortable","common","complete","complex","concerned","condemned","confused","conscious","cooing","cool","cooperative","coordinated","courageous","cowardly","crabby","craven","crazy","creepy","crooked","crowded","cruel","cuddly","cultured","cumbersome","curious","curly","curved","curvy","cut","cute","cute","cynical","daffy","daily","damaged","damaging","damp","dangerous","dapper","dark","dashing","dazzling","dead","deadpan","deafening","dear","debonair","decisive","decorous","deep","deeply","defeated","defective","defiant","delicate","delicious","delightful","delirious","demonic","delirious","dependent","depressed","deranged","descriptive","deserted","detailed","determined","devilish","didactic","different","difficult","diligent","direful","dirty","disagreeable","disastrous","discreet","disgusted","disgusting","disillusioned","dispensable","distinct","disturbed","divergent","dizzy","domineering","doubtful","drab","draconian","dramatic","dreary","drunk","dry","dull","dusty","dusty","dynamic","dysfunctional","eager","early","earsplitting","earthy","easy","eatable","economic","educated","efficacious","efficient","eight","elastic","elated","elderly","electric","elegant","elfin","elite","embarrassed","eminent","empty","enchanted","enchanting","encouraging","endurable","energetic","enormous","entertaining","enthusiastic","envious","equable","equal","erect","erratic","ethereal","evanescent","evasive","even","excellent","excited","exciting","exclusive","exotic","expensive","extra-large","extra-small","exuberant","exultant","fabulous","faded","faint","fair","faithful","fallacious","false","familiar","famous","fanatical","fancy","fantastic","far","far-flung","fascinated","fast","fat","faulty"]
places = ["art gallery","bakery","bank","bar","beach","bookstore","bowling alley","bus station","cafe","campground","casino","cemetery","church","city hall","clothing store","coffee shop","concert hall","convenience store","courthouse","dentist's office","department store","doctor's office","drugstore","embassy","factory","farm","fire station","gas station","golf course","grocery store","gym","hair salon","hospital","hotel","house","jail","library","mall","museum","nightclub","office building","park","parking lot","pharmacy","police station","post office","restaurant","school","shopping mall","spa","stadium","store","subway station","supermarket","theater","university","zoo"]
# Give me a LOOOOONG list of fantasy-themed adjectives and places, please!
adjectives = ["brick-walled","cobwebbed","dark","dusty","filthy","flooded","gloomy","grubby","grimy","musty","moldy","muddy","murky","mysterious","narrow","nasty","obscure","old","overgrown","rotten","rusty","shadowy","shady","smelly","spooky","stale","stained"]
places = ["art gallery","castle","cave","crypt","dungeon","graveyard","house","inn","keep","labyrinth","maze","mine","ruin","temple","tower","tomb","tunnel","vault","well","windmill"]
class DungeonMap:
    def __init__(self):
        self.rooms = {}
        self._player = None
        self.dragon_location = None

    @property
    def player(self):
        return self._player
    @player.setter
    def player(self,player:Player):
        self._player = player

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
        self._player.position = room

    def move_player(self, direction:Direction.value):
        if direction not in self.rooms[self._player.position]:
            click.echo(InteractionMessages.MOVE_BUT_DIRECTION_NOT_EXIST.value)
            return False
        self._player.position = self.rooms[self.player.position][direction]
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
    
# def create_random_door(direction:Direction.value):
#     random.random()
#     broken_chance = 0.1
#     open_chance = 0.5
#     trap_chance = 0.2
#     locked_chance = 0.2
#     # new_door = Door(random.choice(list(DoorType)),direction)
#     if random.random() <= broken_chance:
#         new_door.is_broken = True
#         return new_door
#     elif random.random() <= open_chance:
#         new_door.is_open = True
#     if random.random() <= trap_chance:
#         new_door.is_trapped = True
#     if random.random() <= locked_chance:
#         new_door.is_locked = True
#     return new_door

    

    
def generate_dungeon(num_rooms,num_exits,max_treasures_per_room):
    # First room is always room 1
    first_name = random.choice(adjectives)
    second_name = random.choice(places)
    dungeon = DungeonMap()
    dungeon.player = Player(10,{})
    # first_door = Door(DoorType.BRONZE.value,True,False,False,False)
    first_room = Room(1,first_name.title() + " " + second_name.title(),contents={})
    first_room.is_exit = True
    dungeon.add_room(first_room)
    dungeon.set_player_location(first_room)
    num_created = 1
    while num_created < num_rooms:
        first_name = random.choice(adjectives)
        second_name = random.choice(places)
        random_room = random.choice(list(dungeon.rooms.keys()))
        direction = random.choice(list(Direction))
        # new_door = create_random_door(direction)
        new_content = []
        new_content = generate_treasures(20)
        # new_content.append(new_door)
        if direction.value not in dungeon.rooms[random_room]:
            if random.random() < 0.8:
                letter_count = 0
                letter_list = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(range(100))
                letter_list.reverse()
                num_created += 1
                new_room_id = num_created
                new_room = Room(new_room_id,first_name.title() + " " + second_name.title(),{})
                # Take a random number of treasures from the list
                num_treasures = random.randint(0,max_treasures_per_room) 
                # If the number of treasures is greater than the number of treasures left, take all the treasures
                if num_treasures > len(new_content):
                    num_treasures = len(num_treasures)
                for i in range(num_treasures):
                    new_room.contents[str(letter_list.pop())] = new_content.pop()
                dungeon.add_room(new_room)
                dungeon.add_connection(random_room,new_room,direction.value)
    exit_lefts = num_exits
    while exit_lefts > 0:
        random_room = random.choice(list(dungeon.rooms.keys()))
        if random_room.is_exit == False:
            random_room.is_exit = True
            exit_lefts -= 1
    
    # while len(new_content) > 0:
    #     random_room = random.choice(list(dungeon.rooms.keys()))
    #     random_room.contents[str(letter_list.pop())] = new_content.pop()
    #     letter_count += 1
        

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

