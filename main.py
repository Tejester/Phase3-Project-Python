import markovify
from dungeon_map import DungeonMap,generate_dungeon
# from room import Door
from direction import Direction
import click
from room import InteractionMessages
from entities import ActivityLevels
import random
from end_states import EndState,end_game


num_rooms = 20
num_exits = 1
treasure_generated = 20
max_treasures_per_room = 3
chameleos_min_distance = 5
dungeon = generate_dungeon(num_rooms,num_exits,treasure_generated,max_treasures_per_room,chameleos_min_distance)

# Funny messages for whenever the player places shrimp in a room
shrimp_placement_messages = ["Good thing you took that fishing trip to Neo-Miami.","Since when did shrimp come in this size?",
                             "You're not sure if you should be proud or ashamed of yourself.","Maybe you should start a shrimp farm.",
                             "Don't you think you could've sold these for a lot more?","Plop!","It's raw, but it's also not for you to eat",
                             "Better the shrimp than you right?","Look at that size!!!:"]

def chameleos_steps(steps):
    for i in range(steps):
        dungeon.move_chameleos_towards_player()

def chameleos_attack(activity_level:ActivityLevels):
    if(activity_level == ActivityLevels.SLUMBER):
        return
    elif(activity_level == ActivityLevels.CRANKY):
        click.echo("Chameleos grumbles at you but does nothing.")
        if random.random() > 0.2:
            click.echo("Maybe he's a little hungry? You should try to feed him some shrimp.")
    elif(activity_level == ActivityLevels.DISGRUNTLED):
        click.echo("Chameleos attempts to scratch you...")
        if chameleos_hit_attempt(0.3):
            dungeon.player.take_damage(1,dungeon)
        if chameleos_swallow_instadeath():
            end_game(EndState.SWALLOWED,dungeon)
    elif(activity_level == ActivityLevels.FURIOUS):
        click.echo("Chameleos attempts to attack you with its tongue...")
        if chameleos_hit_attempt(0.5):
            dungeon.player.take_damage(2,dungeon)
        if chameleos_swallow_instadeath():
            end_game(EndState.SWALLOWED,dungeon)
    elif(activity_level == ActivityLevels.BLOODTHIRSTY):
        click.echo("Chameleos attempts to breathe fire in your direction.")
        if chameleos_hit_attempt(0.7):
            dungeon.player.take_damage(3,dungeon)
        if chameleos_swallow_instadeath():
            end_game(EndState.SWALLOWED,dungeon)
    

def chameleos_hit_attempt(hit_chance:float):
    if random.random() > hit_chance:
        click.echo("But you manage to dodge Chameleos' attack.")
        return False
    else:
        click.echo("And you get hurt.")
        return True



def chameleos_swallow_instadeath():
    click.echo("Chameleos attempts to swallow you whole...")
    if random.random() > 0.1:
        click.echo("But you manage to escape the tongue of Chameleos by the skin of your teeth.")
        return False
    else:
        click.echo("You became his lunch!")
        return True
    
def chameleos_same_room_action():
    if dungeon.in_same_room():
        if(dungeon.chameleos.activity_level == ActivityLevels.SLUMBER):
            click.echo("You see Chameleos sleeping soundly.")
            chameleos_attack(dungeon.chameleos.activity_level)
        elif(dungeon.chameleos.activity_level == ActivityLevels.CRANKY):
            click.echo("You see Chameleos glaring at you.")
            chameleos_attack(dungeon.chameleos.activity_level)
        elif(dungeon.chameleos.activity_level == ActivityLevels.DISGRUNTLED):
            click.echo("You see Chameleos getting ready to attack you.")
            chameleos_attack(dungeon.chameleos.activity_level)
        elif(dungeon.chameleos.activity_level == ActivityLevels.FURIOUS):
            click.echo("You see Chameleos charging at you.")
            chameleos_attack(dungeon.chameleos.activity_level)
        elif(dungeon.chameleos.activity_level == ActivityLevels.BLOODTHIRSTY):
            click.echo("You see Chameleos salivating as though his dinner has been served!")
            chameleos_attack(dungeon.chameleos.activity_level)
        return True
    else:
        return False




@click.command()
@click.argument("direction", type=click.Choice([d.value for d in Direction]))
def go(direction):
    if dungeon.player.position == dungeon.chameleos.position:
        if random.random() > 0.4:
            click.echo("You manage to escape the tongue of Chameleos by the skin of your teeth.")
        else:
            click.echo("Chameleos has eaten you.")
            SystemExit()
    if dungeon.move_player(direction):
        click.echo(f"You move to {dungeon.player.position.room_name}")
        if not dungeon.chameleos.activity_level == ActivityLevels.SLUMBER:
            chameleos_steps(dungeon.chameleos.activity_level.value)
    if dungeon.player.position.is_exit:
        click.echo("This is an exit!")
    chameleos_same_room_action()


@click.command()
def look():
    for direction in dungeon.rooms[dungeon.player.position].items():
        click.echo(f"There is a room to the {direction[0]}.")
    for treasure in dungeon.player.position.contents.keys():
        click.echo(f"({treasure}) There is a {dungeon.player.position.contents[treasure].name} here.")
    if dungeon.player.position.is_exit:
        click.echo("This is an exit!")
    
@click.command()
def exit():
    if dungeon.player.position.is_exit:
        end_game(EndState.WON,dungeon)
    else:
        click.echo("There is no exit here!")

@click.command()
def inventory():
    # print(dungeon.player.position.contents)
    count = 1
    for item in dungeon.player.inventory.keys():
        click.echo(f"({item}) {dungeon.player.inventory[item].name}")

@click.command()
@click.argument("treasure_key", type=str)
def grab(treasure_key):
    if treasure_key not in dungeon.player.position.contents:
        click.echo("That is not a real treasure.")
        return
    else:
        element = dungeon.player.position.contents.pop(treasure_key)
        dungeon.player.inventory[str(treasure_key)] = element
        dungeon.noise_scale += 1
        click.echo(f"You have picked up the {element.name}.")

@click.command()
@click.argument("treasure_key", type=str)
def drop(treasure_key):
    if treasure_key not in dungeon.player.inventory.keys():
        click.echo("You don't have that treasure.")
        return
    else:
        element = dungeon.player.inventory.pop(treasure_key)
        dungeon.player.position.contents[str(treasure_key)] = element
        click.echo(f"You have dropped the {element.name}.")

@click.command()
@click.argument("treasure_key", type=str)
def appraise(treasure_key):
    if treasure_key in dungeon.player.position.contents.keys():
        click.echo("Pick up the treasure before you appraise it.")
        return
    elif treasure_key not in dungeon.player.inventory.keys():
        click.echo("There is no such treasure.")
        return
    else:
        t_name = dungeon.player.inventory[treasure_key].name
        t_desc = dungeon.player.inventory[treasure_key].desc
        t_value = dungeon.player.inventory[treasure_key].value
        t_weight = dungeon.player.inventory[treasure_key].weight
        click.echo(f"{t_name} is a treasure worth {t_value} gold pieces. It weighs {t_weight} pounds. {t_desc}")

@click.command()
def listen():
    print("Player Location: ",dungeon.player.position)
    print("Chameleos Location: ",dungeon.chameleos.position)
    if(dungeon.is_neighbor(dungeon.player.position,dungeon.chameleos.position)):
        if dungeon.chameleos.activity_level == ActivityLevels.SLUMBER:
            click.echo(f"You hear an odd snoring sound coming from the room to the {dungeon.is_neighbor(dungeon.player.position,dungeon.chameleos.position)}.")
        elif dungeon.chameleos.activity_level == ActivityLevels.CRANKY:
            click.echo(f"You hear a slight chittering sound coming from the room to the {dungeon.is_neighbor(dungeon.player.position,dungeon.chameleos.position)}.")
        elif dungeon.chameleos.activity_level == ActivityLevels.DISGRUNTLED:
            click.echo(f"You hear a loud chittering sound coming from the room to the {dungeon.is_neighbor(dungeon.player.position,dungeon.chameleos.position)}.")
        elif dungeon.chameleos.activity_level == ActivityLevels.FURIOUS:
            click.echo(f"You hear a sound much like a wet sponge being thrown at a wall from the room to the {dungeon.is_neighbor(dungeon.player.position,dungeon.chameleos.position)}.")
        elif dungeon.chameleos.activity_level == ActivityLevels.BLOODTHIRSTY:
            click.echo(f"You hear an ear-piercing scream coming from the room to the {dungeon.is_neighbor(dungeon.player.position,dungeon.chameleos.position)}.")

@click.command()
def scream():
    dungeon.scream()
    if not dungeon.chameleos.activity_level == ActivityLevels.SLUMBER:
        chameleos_steps(dungeon.chameleos.activity_level.value)
    chameleos_same_room_action()

@click.command()
def wait():
    if not dungeon.chameleos.activity_level == ActivityLevels.SLUMBER:
        click.echo("You wait for a brief moment.")
        chameleos_steps(dungeon.chameleos.activity_level.value)
    chameleos_same_room_action()


@click.command()
def shrimpify():
    if dungeon.player.position.shrimpified:
        if random.random() > 0.5:
            click.echo("You already placed shrimp in this room. Can we leave? It's starting to smell.")
        else:
            click.echo("This room is already shrimpified. You don't want to be part of the meal do you?")
    else:
        click.echo("A massive, dragon-sized shrimp appears out of your storage ring.")
        random_message_index = random.randint(0,len(shrimp_placement_messages))
        click.echo(shrimp_placement_messages[random_message_index])
        dungeon.player.shrimpify(dungeon.player.position)
    chameleos_same_room_action()

@click.command()
def status():
    dungeon.player.display_health_status()
    


# @click.command()
# @click.argument("direction", type=click.Choice([d.value for d in Direction]))
# def lock(direction):
#     dungeon.player_location.door.lock()

# @click.command()
# @click.argument("direction", type=click.Choice([d.value for d in Direction]))
# def unlock(direction):
#     dungeon.player_location.door.unlock()

# @click.command()
# @click.argument("direction", type=click.Choice([d.value for d in Direction]))
# def destroy(direction):
#     dungeon.player_location.door.destroy()

@click.group()
def cli():
    pass
                
cli.add_command(go)
cli.add_command(look)
cli.add_command(exit)
cli.add_command(inventory)
cli.add_command(grab)
cli.add_command(appraise)
cli.add_command(drop)
cli.add_command(listen)
cli.add_command(scream)
cli.add_command(wait)
cli.add_command(shrimpify)
cli.add_command(status)

if __name__ == "__main__":
    while True:
        # click.echo(dungeon.rooms)
        click.echo("You are in the " + dungeon.player.position.room_name)
        cmd = click.prompt("What do you want to do?",type=str)
        cmd_parts = cmd.split()
        try:
            # click.clear()
            cli(cmd_parts)
        except SystemExit:
            pass