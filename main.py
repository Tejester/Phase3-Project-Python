#THIS IS FOR TESTING PURPOSE


import random
from player import Player
from room import Rooms

player_name = Player.name
rooms = Rooms.rooms

while True:
    print('1. Enter Room')
    choice = input('> ')

    if choice == "1":
        curr_room = random.choice(list(rooms))
        room1 = random.choice(list(rooms))
        room2 = random.choice(list(rooms)) 
        print(f'You entered {curr_room}')
        print('Choose where you want to go next')
        print("Door 1")
        print("Door 2")
        choice = input('> ')
        if choice == "1":
            print(f'You entered {room1}')

            print("1 Goback")
            choice = input('> ')
            if choice == "1":
                print(f"you entered {curr_room}")

        elif choice == "2":
            print(f'You entered {room2}')
            print("1 Goback")
            choice = input('> ')
            if choice == "1":
                print(f"you entered {curr_room}")
