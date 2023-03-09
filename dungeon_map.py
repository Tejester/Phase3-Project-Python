from __future__ import annotations
from room import Room,InteractionMessages
import random
import click
from click import style
from direction import Direction
from entities import Player, Chameleos, ActivityLevels
from treasure import generate_treasures
import string
from queue import Queue
from dungeon_colors import MessageColors
import tracery
from tracery.modifiers import base_english

adjectives = ["abandoned","aberrant","abhorrent","abiding","abject","ablaze","able","abnormal","aboard","aboriginal","abortive","abounding","abrasive","abrupt","absent","absorbed","absorbing","abstracted","absurd","abundant","abusive","acceptable","accessible","accidental","accurate","acid","acidic","acoustic","acrid","actually","ad hoc","adamant","adaptable","addicted","adhesive","adjoining","adorable","adventurous","afraid","aggressive","agonizing","agreeable","ahead","ajar","alcoholic","alert","alike","alive","alleged","alluring","aloof","amazing","ambiguous","ambitious","amuck","amused","amusing","ancient","angry","animated","annoyed","annoying","anxious","apathetic","aquatic","aromatic","arrogant","ashamed","aspiring","assorted","astonishing","attractive","auspicious","automatic","available","average","awake","aware","awesome","awful","axiomatic","bad","barbarous","bashful","bawdy","beautiful","befitting","belligerent","beneficial","bent","berserk","best","better","bewildered","big","billowy","bite-sized","bitter","bizarre","black","black-and-white","bloody","blue","blue-eyed","blushing","boiling","boorish","bored","boring","bouncy","boundless","brainy","brash","brave","brawny","breakable","breezy","brief","bright","bright","broad","broken","brown","bumpy","burly","bustling","busy","cagey","calculating","callous","calm","capable","capricious","careful","careless","caring","cautious","ceaseless","certain","changeable","charming","cheap","cheerful","chemical","chief","childlike","chilly","chivalrous","chubby","chunky","clammy","classy","clean","clear","clever","cloistered","cloudy","closed","clumsy","cluttered","coherent","cold","colorful","colossal","combative","comfortable","common","complete","complex","concerned","condemned","confused","conscious","cooing","cool","cooperative","coordinated","courageous","cowardly","crabby","craven","crazy","creepy","crooked","crowded","cruel","cuddly","cultured","cumbersome","curious","curly","curved","curvy","cut","cute","cute","cynical","daffy","daily","damaged","damaging","damp","dangerous","dapper","dark","dashing","dazzling","dead","deadpan","deafening","dear","debonair","decisive","decorous","deep","deeply","defeated","defective","defiant","delicate","delicious","delightful","delirious","demonic","delirious","dependent","depressed","deranged","descriptive","deserted","detailed","determined","devilish","didactic","different","difficult","diligent","direful","dirty","disagreeable","disastrous","discreet","disgusted","disgusting","disillusioned","dispensable","distinct","disturbed","divergent","dizzy","domineering","doubtful","drab","draconian","dramatic","dreary","drunk","dry","dull","dusty","dusty","dynamic","dysfunctional","eager","early","earsplitting","earthy","easy","eatable","economic","educated","efficacious","efficient","eight","elastic","elated","elderly","electric","elegant","elfin","elite","embarrassed","eminent","empty","enchanted","enchanting","encouraging","endurable","energetic","enormous","entertaining","enthusiastic","envious","equable","equal","erect","erratic","ethereal","evanescent","evasive","even","excellent","excited","exciting","exclusive","exotic","expensive","extra-large","extra-small","exuberant","exultant","fabulous","faded","faint","fair","faithful","fallacious","false","familiar","famous","fanatical","fancy","fantastic","far","far-flung","fascinated","fast","fat","faulty"]
places = ["art gallery","bakery","bank","bar","beach","bookstore","bowling alley","bus station","cafe","campground","casino","cemetery","church","city hall","clothing store","coffee shop","concert hall","convenience store","courthouse","dentist's office","department store","doctor's office","drugstore","embassy","factory","farm","fire station","gas station","golf course","grocery store","gym","hair salon","hospital","hotel","house","jail","library","mall","museum","nightclub","office building","park","parking lot","pharmacy","police station","post office","restaurant","school","shopping mall","spa","stadium","store","subway station","supermarket","theater","university","zoo"]
# Give me a LOOOOONG list of fantasy-themed adjectives and places, please!
adjectives = ["brick-walled","cobwebbed","dark","dusty","filthy","flooded","gloomy","grubby","grimy","musty","moldy","muddy","murky","mysterious","narrow","nasty","obscure","old","overgrown","rotten","rusty","shadowy","shady","smelly","spooky","stale","stained"]
places = ["art gallery","castle","cave","crypt","dungeon","graveyard","house","inn","keep","labyrinth","maze","mine","ruin","temple","tower","tomb","tunnel","vault","well","windmill"]
class DungeonMap:
    def __init__(self):
        self.rooms = {}
        self._player = None
        self._chameleos = None
        self._noise_scale = 0

    
    @property
    def dungeon_treasures(self):
        return self._dungeon_treasures
    @dungeon_treasures.setter
    def dungeon_treasures(self,dungeon_treasures:list):
        self._dungeon_treasures = dungeon_treasures

    @property
    def noise_scale(self):
        return self._noise_scale
    @noise_scale.setter
    def noise_scale(self,noise_scale:int):
        self._noise_scale = noise_scale

    @property
    def chameleos(self):
        return self._chameleos
    @chameleos.setter
    def chameleos(self,chameleos:Chameleos):
        self._chameleos = chameleos
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

    def is_neighbor(self, room1:Room, room2:Room) -> Direction:
        for direction,room in self.rooms[room1].items():
            if room == room2:
                return direction
        return False
    
    def in_same_room(self) -> bool:
        return self._player.position == self._chameleos.position
    

    def set_player_location(self, room:Room):
        self._player.position = room
    
    def set_chameleos_location(self, room:Room):
        self._chameleos.position = room

    def move_player(self, direction:Direction.value):
        if direction not in self.rooms[self._player.position]:
            click.echo(InteractionMessages.MOVE_BUT_DIRECTION_NOT_EXIST.value)
            return False
        self._player.position = self.rooms[self.player.position][direction]
        click.echo(style("You move through the corridor making as little noise as possible.",MessageColors.PLAYER.value))
        self._noise_scale += 1
        self.chameleos.update_activity_level(self._noise_scale)
        return True
    
    def move_chameleos_towards_player(self):
        if self._chameleos.position == self._player.position:
            return
        elif self.chameleos.position.shrimpified:
            self.chameleos.eat_shrimp(self.chameleos.position)
            click.echo(style("You hear an eating sound.",MessageColors.CHAMELEOS.value))
            self._noise_scale = 0
            self.chameleos.update_activity_level(self._noise_scale)
        else:
            click.echo(style("You hear a rustling in the distance.",MessageColors.CHAMELEOS.value))
            path = find_distance(self.rooms,self._chameleos.position,self._player.position,True)
            click.echo(path)
            if(len(path)) >= 1:
                self._chameleos.position = path[1]
            elif(len(path) == 1):
                self._chameleos.position = path[0]
            else:
                return
            return True

    def scream(self):
        click.echo(style("You scream as loud as you can!",MessageColors.PLAYER.value))
        self._noise_scale += 10
        self.chameleos.update_activity_level(self._noise_scale)
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
    
# Using BFS to find the shortest path
def find_distance(rooms:dict,start_room:Room,end_room:Room,return_visited:bool=False):
    visited = list()
    queue = Queue()
    queue.put((start_room,0))

    while not queue.empty():
        room, distance = queue.get()
        if room == end_room:
            visited.append(end_room)
            if(return_visited == False):
                return distance
            else:
                return visited
        else:
            visited.append(room)
        for direction,new_room in rooms[room].items():
            # print(direction,new_room)
            # print("Visited: ",visited)
            # print("Queue: ",queue.queue)
            if new_room not in visited:
                queue.put((new_room,distance+1))
    if return_visited == False:
        return -1 # If end is not reachable from start
    else:
        return visited

    
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

    
    
def generate_dungeon(num_rooms,num_exits,treasure_generated,max_treasures_per_room,chameleos_min_distance:int):
    # # Random sentence engine for room descriptions
    # grammar = tracery.Grammar({
    #     # subject for room description. It's a room, so it's always "the room"
    #     "subject": ["the room"],
    #     # adjectives for room description
    #     "adjective": ["funny","smelly","cool","dark","bright","shiny","dusty","dirty","mysterious","magical","enchanted","rancid","bloodthirsty",
    #                   "ugly","shabby","beautful","fancy","frightening","scary","creepy","spooky","haunted","spooky","spooky","spooky","spooky"],
    #     # verbs for room description
    #     "verb" : ["scream","sing","laugh","cry","echo","whisper","moan","howl","yell","squeal","squeak","drip","splash"],
    #     # verbs conjugated to present tense
    #     "verb.present" : ["screams","sings","laughs","cries","echoes","whispers","moans","howls","yells","squeals","squeaks","drips","splashes"],
    #     # verbs conjugated to past tense
    #     "verb.past" : ["screamed","sang","laughed","cried","echoed","whispered","moaned","howled","yelled","squealed","squeaked","dripped","splashed"],

    #     # nouns for room description
    #     "noun" : ["quietus","silence","noise","sound","flashing lights","darkness","light","shadows","ghosts","spirits","rocks","stones","dirt","dust","cobwebs","mud","water","blood"],
    #     # adverbs for room description
    #     "adverb" : ["loudly","softly","quietly","eerie","ominously","creepily","frighteningly","scarily","creepily","creepily","amazingly","magically","darkly","gradually","carelessly"],
    #     # prepositions for room description
    #     "preposition" : ["in","on","under","behind","beside","near","above","below","around","through","across","over","underneath","inside",
    #                      "outside","beneath","beyond","throughout","among","amongst","amid","amidst","within","without","alongside","along","opposite","towards",
    #                      "toward","from","of","by","with","at","into","onto","through","till","until","since","for","in","on","upon","after",
    #                      "before","since","until","till","during","while","whilst","except","excepting","excluding","including","barring","despite",
    #                      "minus","notwithstanding","out","outside","over","past","per","plus","pro","regarding",
    #                      "round","save","sub","than","throughout","to","toward","towards","under","underneath","unlike","until","unto","up","upon","versus",
    #                      "via","with","within","without"],
    #     # conjunctions for room description
    #     "conjunction" : ["and","or","but","nor","for","yet","so"],
    #     # articles for room description
    #     "article" : ["a","the","an"],
    #     # colors for room description
    #     "color" : ["red","orange","yellow","green","blue","indigo","violet","purple","black","white","grey","gray","brown","pink","magenta","cyan","teal","maroon","olive","lime","navy","aqua"],
    #     # smells for room description
    #     "smell" : ["rotten","stale","foul","putrid","decaying","decaying","funny","stinky","amazing","otherworldly","magical","enchanted","rancid","bloodthirsty"],
    #     # actions for room description
    #     "action": ["seems to be alive","has something lurking inside","has been abandoned for years","clearly hasn't gotten a through cleaning in a while",
    #                "dust covers everything","is covered in cobwebs","is covered in dust","is covered in dirt","is covered in grime","is covered in filth",
    #                "is covered in mud","is covered in slime","is covered in blood","is covered in guts","is covered in gore","is covered in vomit","is covered in feces",
    #                "is covered in urine","is covered in snot","is covered in mucus","is covered in pus","is covered in oil","is covered in grease","is covered in tar","is covered in wax",
    #                "is covered in paint","is covered in ink","is covered in mud","is covered in sand","is covered in ash","is covered in soot","is covered in rust",
    #                "is covered in mold","is covered in mildew","is covered in fungus","is covered in moss","is covered in lichen","is covered in algae","is covered in slime",
    #                "is covered in ooze","is covered in pus","is covered in blood","is covered in guts","is covered in gore","is covered in vomit","is covered in feces",
    #                "is covered in urine","is covered in snot","is covered in mucus","is covered in pus","is covered in oil","is covered in grease","is covered in tar",
    #                "is covered in wax","is covered in paint","is covered in ink","is covered in mud","is covered in sand","is covered in ash","is covered in soot","is covered in rust",
    #                "is covered in mold","is covered in mildew","is covered in fungus","is covered in moss","is covered in lichen","is covered in algae","is covered in slime","is covered in ooze",
    #                "is covered in pus","is covered in blood","is covered in guts","is covered in gore","is covered in vomit","is covered in feces","is covered in urine",
    #                "is covered in snot","is covered in mucus","is covered in pus","is covered in oil","is covered in grease","is covered in tar","is covered in wax",
    #                "is covered in paint","is covered in ink","is covered in mud","is covered in sand","is covered in ash","is covered in soot","is covered in rust",
    #                "is covered in mold","is covered in mildew","is covered in fungus","is covered in moss","is covered in lichen","is covered in algae","is covered in slime",
    #                "is covered in ooze","is covered in pus"],
    #     # Random origins for room description:
    #     "origin": ["#subject.capitalize# #verb.past# #preposition# #article# #adjective# #noun#."]
    # })

    # grammar.add_modifiers(base_english)
    # sentence = grammar.flatten("#origin#")
    # First room is always room 1
    first_name = random.choice(adjectives)
    second_name = random.choice(places)
    dungeon = DungeonMap()
    dungeon.player = Player(5,{})
    dungeon.chameleos = Chameleos()
    # first_door = Door(DoorType.BRONZE.value,True,False,False,False)
    first_room = Room(1,first_name.title() + " " + second_name.title(),contents={})
    first_room.is_exit = True
    dungeon.add_room(first_room)
    dungeon.set_player_location(first_room)
    num_created = 1
    letter_list = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(range(100))
    letter_list.reverse()
    while num_created < num_rooms:
        first_name = random.choice(adjectives)
        second_name = random.choice(places)
        random_room = random.choice(list(dungeon.rooms.keys()))
        direction = random.choice(list(Direction))
        # new_door = create_random_door(direction)
        new_content = []
        new_content = generate_treasures(treasure_generated)
        dungeon.dungeon_treasures = new_content
        # new_content.append(new_door) 
        if direction.value not in dungeon.rooms[random_room]:
            if random.random() < 0.8:
                # sentence = grammar.flatten("#origin#")
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
    # distance = find_distance(dungeon.rooms,dungeon.player.position,random_room)
    # print(distance)
    exit_lefts = num_exits
    while exit_lefts > 0:
        random_room = random.choice(list(dungeon.rooms.keys()))
        if random_room.is_exit == False:
            random_room.is_exit = True
            exit_lefts -= 1

    # Find a random room with a reasonable distance from the player to place Chameleos
    candidate_room = random.choice(list(dungeon.rooms.keys()))
    while find_distance(dungeon.rooms,dungeon.player.position,candidate_room) < chameleos_min_distance:
        candidate_room = random.choice(list(dungeon.rooms.keys()))
    else:
        dungeon.set_chameleos_location(candidate_room)
    return dungeon

