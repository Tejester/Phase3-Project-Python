import random


class Chameleon:
    def __init__(self):
        self.current_room = None

    def set_current_room(self, room):
        self.current_room = room

    def set_random_starting_room(self, dungeon_map):
        player_room_name = dungeon_map.player_location.name
        candidate_room = None
        while candidate_room is None or abs(list(dungeon_map.rooms.keys()).index(candidate_room) - list(dungeon_map.rooms.keys()).index(player_room_name)) < 15:
            candidate_room = random.choice(list(dungeon_map.rooms.keys()))
        self.current_room = candidate_room
        print(candidate_room)


    
    def move_towards_player(self, dungeon_map, noise_scale):
        steps = min(5, max(1, noise_scale))
        for i in range(steps):
            if self.current_room == dungeon_map.player_location:
                print("The chameleon has caught you!")
                return True
            adjacent_rooms = dungeon_map.rooms[self.current_room].values()
            self.current_room = random.choice(list(adjacent_rooms))
        return False
    
chameleon = Chameleon()
