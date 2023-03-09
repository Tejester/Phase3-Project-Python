import markovify
from dungeon_map import DungeonMap,generate_dungeon
# from room import Door
from direction import Direction
import click
from click import style
from room import InteractionMessages
from entities import ActivityLevels
import random
from end_states import EndState,end_game
from dungeon_colors import MessageColors
from sqlalchemy import create_engine, func,select
from end_states import ScoreTable
from sqlalchemy.orm import sessionmaker


scoretable = ScoreTable()

num_rooms = 20
num_exits = 1
treasure_generated = 20
max_treasures_per_room = 3
chameleos_min_distance = 5
first_room = True
dungeon = generate_dungeon(num_rooms,num_exits,treasure_generated,max_treasures_per_room,chameleos_min_distance)

engine = create_engine('sqlite:///scores.db', echo=True)


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
        click.echo(style("Chameleos grumbles at you but does nothing.",fg=MessageColors.CHAMELEOS.value))
        if random.random() > 0.2:
            click.echo(style("Maybe he's a little hungry? You should try to feed him some shrimp.",fg=MessageColors.SHRIMP.value))
    elif(activity_level == ActivityLevels.DISGRUNTLED):
        click.echo(style("Chameleos attempts to scratch you...",MessageColors.CHAMELEOS.value))
        if chameleos_hit_attempt(0.3):
            dungeon.player.take_damage(1,dungeon)
        if chameleos_swallow_instadeath():
            end_game(EndState.SWALLOWED,dungeon)
    elif(activity_level == ActivityLevels.FURIOUS):
        click.echo(style("Chameleos attempts to attack you with its tongue...",MessageColors.CHAMELEOS.value))
        if chameleos_hit_attempt(0.5):
            dungeon.player.take_damage(2,dungeon)
        if chameleos_swallow_instadeath():
            end_game(EndState.SWALLOWED,dungeon)
    elif(activity_level == ActivityLevels.BLOODTHIRSTY):
        click.echo(style("Chameleos attempts to breathe fire in your direction.",fg=MessageColors.CHAMELEOS.value))
        if chameleos_hit_attempt(0.7):
            dungeon.player.take_damage(3,dungeon)
        if chameleos_swallow_instadeath():
            end_game(EndState.SWALLOWED,dungeon)
    

def chameleos_hit_attempt(hit_chance:float):
    if random.random() > hit_chance:
        click.echo(style("But you manage to dodge Chameleos' attack.",fg=MessageColors.PLAYER.value))
        return False
    else:
        click.echo(style("And you get hurt.",fg=MessageColors.BAD.value))
        return True



def chameleos_swallow_instadeath():
    click.echo(style("Chameleos attempts to swallow you whole...",fg=MessageColors.CHAMELEOS.value))
    if random.random() > 0.1:
        click.echo(style("But you manage to escape the tongue of Chameleos by the skin of your teeth.",fg=MessageColors.PLAYER.value))
        return False
    else:
        click.echo(style("You became his lunch!",fg=MessageColors.BAD.value))
        dungeon.player.hp -= 100
        return True
    
def chameleos_same_room_action():
    if dungeon.in_same_room():
        if(dungeon.chameleos.activity_level == ActivityLevels.SLUMBER):
            click.echo(style("Chameleos is sleeping soundly.",fg=MessageColors.CHAMELEOS.value))
            chameleos_attack(dungeon.chameleos.activity_level)
        elif(dungeon.chameleos.activity_level == ActivityLevels.CRANKY):
            click.echo(style("Chameleos is glaring at you.",fg=MessageColors.CHAMELEOS.value))
            chameleos_attack(dungeon.chameleos.activity_level)
        elif(dungeon.chameleos.activity_level == ActivityLevels.DISGRUNTLED):
            click.echo(style("Chameleos is getting ready to attack you.",fg=MessageColors.CHAMELEOS.value))
            chameleos_attack(dungeon.chameleos.activity_level)
        elif(dungeon.chameleos.activity_level == ActivityLevels.FURIOUS):
            click.echo(style("Chameleos is charging at you.",fg=MessageColors.CHAMELEOS.value))
            chameleos_attack(dungeon.chameleos.activity_level)      
        elif(dungeon.chameleos.activity_level == ActivityLevels.BLOODTHIRSTY):
            click.echo(style("Chameleos is salivating as though his dinner has been served!",fg=MessageColors.CHAMELEOS.value))
            chameleos_attack(dungeon.chameleos.activity_level)
        return True
    else:
        return False




@click.command()
@click.argument("direction", type=click.Choice([d.value for d in Direction]))
def go(direction):
    # if dungeon.player.position == dungeon.chameleos.position:
    #     if random.random() > 0.4:
    #         click.echo(style("You manage to escape the tongue of Chameleos by the skin of your teeth.",fg=MessageColors.PLAYER.value))
    #     else:
    #         click.echo(style("Chameleos has eaten you.",fg=MessageColors.BAD.value))
    if dungeon.move_player(direction):
        click.echo(style(f"ROOM: {dungeon.player.position.room_name}",fg=MessageColors.LOCATION.value))
        if not dungeon.chameleos.activity_level == ActivityLevels.SLUMBER:
            chameleos_steps(dungeon.chameleos.activity_level.value)
    if dungeon.player.position.is_exit:
        click.echo(style("This is an exit!",fg=MessageColors.PLAYER.value))
    chameleos_same_room_action()


@click.command()
def look():
    for direction in dungeon.rooms[dungeon.player.position].items():
        click.echo(style(f"There is a room to the {direction[0]}.",fg=MessageColors.PLAYER.value))
    for treasure in dungeon.player.position.contents.keys():
        click.echo(style(f"({treasure}) There is a {dungeon.player.position.contents[treasure].name} here.",fg=MessageColors.TREASURE.value))
    if dungeon.player.position.is_exit:
        click.echo(style("This is an exit!",fg=MessageColors.PLAYER.value))
    
@click.command()
def exit():
    if dungeon.player.position.is_exit:
        dungeon.player.hp -= 100
        end_game(EndState.WON,dungeon)
    else:
        click.echo(style("There is no exit here!",fg=MessageColors.BAD.value))

@click.command()
def inventory():
    # print(dungeon.player.position.contents)
    count = 1
    for item in dungeon.player.inventory.keys():
        click.echo(style(f"({item}) {dungeon.player.inventory[item].name}",fg=MessageColors.TREASURE.value))

@click.command()
@click.argument("treasure_key", type=str)
def grab(treasure_key):
    if treasure_key not in dungeon.player.position.contents:
        click.echo(style("That is not a real treasure.",MessageColors.BAD.value))
        return
    else:
        element = dungeon.player.position.contents.pop(treasure_key)
        dungeon.player.inventory[str(treasure_key)] = element
        dungeon.noise_scale += 1
        click.echo(style(f"You have picked up the {element.name}.",fg=MessageColors.GOOD.value))

@click.command()
@click.argument("treasure_key", type=str)
def drop(treasure_key):
    if treasure_key not in dungeon.player.inventory.keys():
        click.echo(style("You don't have that treasure.",fg=MessageColors.BAD.value))
        return
    else:
        element = dungeon.player.inventory.pop(treasure_key)
        dungeon.player.position.contents[str(treasure_key)] = element
        click.echo(style(f"You have dropped the {element.name}.",fg=MessageColors.BAD.value))

@click.command()
@click.argument("treasure_key", type=str)
def appraise(treasure_key):
    if treasure_key in dungeon.player.position.contents.keys():
        click.echo(style("Pick up the treasure before you appraise it.",fg=MessageColors.BAD.value))
        return
    elif treasure_key not in dungeon.player.inventory.keys():
        click.echo(style("There is no such treasure.",fg=MessageColors.BAD.value))
        return
    else:
        t_name = dungeon.player.inventory[treasure_key].name
        t_desc = dungeon.player.inventory[treasure_key].desc
        t_value = dungeon.player.inventory[treasure_key].value
        t_weight = dungeon.player.inventory[treasure_key].weight
        click.echo(style(f"{t_name} is a treasure worth {t_value} gold pieces. It weighs {t_weight} pounds. {t_desc}",fg=MessageColors.TREASURE.value))

@click.command()
def listen():
    # print("Player Location: ",dungeon.player.position)
    # print("Chameleos Location: ",dungeon.chameleos.position)
    if(dungeon.is_neighbor(dungeon.player.position,dungeon.chameleos.position)):
        if dungeon.chameleos.activity_level == ActivityLevels.SLUMBER:
            click.echo(style(f"You hear an odd snoring sound coming from the room to the {dungeon.is_neighbor(dungeon.player.position,dungeon.chameleos.position)}.",MessageColors.PLAYER.value))
        elif dungeon.chameleos.activity_level == ActivityLevels.CRANKY:
            click.echo(style(f"You hear a slight chittering sound coming from the room to the {dungeon.is_neighbor(dungeon.player.position,dungeon.chameleos.position)}.",fg=MessageColors.PLAYER.value))
        elif dungeon.chameleos.activity_level == ActivityLevels.DISGRUNTLED:
            click.echo(style(f"You hear a loud chittering sound coming from the room to the {dungeon.is_neighbor(dungeon.player.position,dungeon.chameleos.position)}.",fg=MessageColors.PLAYER.value))
        elif dungeon.chameleos.activity_level == ActivityLevels.FURIOUS:
            click.echo(style(f"You hear a sound much like a wet sponge being thrown at a wall from the room to the {dungeon.is_neighbor(dungeon.player.position,dungeon.chameleos.position)}.", fg=MessageColors.PLAYER.value))
        elif dungeon.chameleos.activity_level == ActivityLevels.BLOODTHIRSTY:
            click.echo(style(f"You hear an ear-piercing scream coming from the room to the {dungeon.is_neighbor(dungeon.player.position,dungeon.chameleos.position)}.",fg=MessageColors.PLAYER.value))

@click.command()
def scream():
    dungeon.scream()
    if not dungeon.chameleos.activity_level == ActivityLevels.SLUMBER:
        chameleos_steps(dungeon.chameleos.activity_level.value)
    chameleos_same_room_action()

@click.command()
def wait():
    if not dungeon.chameleos.activity_level == ActivityLevels.SLUMBER:
        click.echo(style("You wait for a brief moment.",fg=MessageColors.PLAYER.value))
        chameleos_steps(dungeon.chameleos.activity_level.value)
    chameleos_same_room_action()


@click.command()
def shrimpify():
    if dungeon.player.position.shrimpified:
        if random.random() > 0.5:
            click.echo(style("You already placed shrimp in this room. Can we leave? It's starting to smell.",fg=MessageColors.BAD.value))
        else:
            click.echo(style("This room is already shrimpified. You don't want to be part of the meal do you?",fg=MessageColors.SHRIMP.value))
    else:
        click.echo(style("A massive, dragon-sized shrimp appears out of your storage ring.",fg=MessageColors.SHRIMP.value))
        random_message_index = random.randint(0,len(shrimp_placement_messages)-1)
        click.echo(style(shrimp_placement_messages[random_message_index],fg=MessageColors.SHRIMP.value))
        dungeon.player.shrimpify(dungeon.player.position)
    chameleos_same_room_action()

@click.command()
def status():
    dungeon.player.display_health_status()

@click.command()
def here():
    click.echo(style("ROOM: " +dungeon.player.position.room_name,fg=MessageColors.LOCATION.value))
    


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
cli.add_command(here)

if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session = Session()
    max_score = session.query(func.max(ScoreTable.score)).scalar()
    click.echo("The highest score is: " + str(max_score))
    session.commit()
    session.close()
    while dungeon.player.hp > 0:
        if first_room:
            click.echo(style("ROOM: " + dungeon.player.position.room_name,fg=MessageColors.LOCATION.value))
            first_room = False
        # click.echo(dungeon.rooms)
        cmd = click.prompt("What do you want to do?",type=str)
        cmd_parts = cmd.split()
        try:
            # click.clear()
            cli(cmd_parts)
        except SystemExit:
            pass