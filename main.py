from dungeon_map import DungeonMap,generate_dungeon
# from room import Door
from direction import Direction
import click
import random
from traps import Trap
from colorama import Fore, Back, Style
from items import Items
from entities import Player
from room import InteractionMessages
from database import session, Score




#colors
reset = Style.RESET_ALL
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
blue = Fore.BLUE
trap_exists = True
trap_found = False

player = Player(10)
traps = Trap.traps
trap = Trap()
items = Items()

dungeon = generate_dungeon(100,99,50)

@click.command()
@click.argument("direction", type=click.Choice([d.value for d in Direction]))
def go(direction):
    if dungeon.move_player(direction):
        click.echo(f"You move to 📍 {blue}{dungeon.player.position.room_name}{reset}")
        if trap.found == True:
            click.echo(f"You got cought in {red}Trap{reset}")
            trap.bleed = True
            trap.found = False
        if trap.bleed == True:
            click.echo(f"You are {red}bleeding{reset}")
            player.take_damage(2)

    if dungeon.player.position.is_exit:
        click.echo(f"This is an {red}exit!{reset}")


@click.command()
def look():
    for direction in dungeon.rooms[dungeon.player.position].items():
        click.echo(f"There is a room to the 🧭 {blue}{direction[0]}{reset}.")
    trap_name = random.choice(list(traps.keys()))
    for treasure in dungeon.player.position.contents.keys():
        click.echo(f"({treasure}) There is a {yellow}{dungeon.player.position.contents[treasure].name}{reset} here.")
    if random.random() < 0.2:
        trap.found = True
        click.echo(f'Watch out for that {red}{trap_name}{reset} trap')
    if random.random() < 0.2:
        items.cloth += 1
        click.echo(f'you found {green}cloth{reset} which can be used as a {green}bandage{reset}')


@click.command
def disarm():
    trap.found = False
    click.echo(f'{blue}Successfully disarmed{reset} {red}trap{reset}')
    look()

@click.command
def bandage():
    if items.cloth > 0:
        items.bandaged = True
        click.echo(f"You applied a {green}bandage{reset} over your wound")
        trap.bleed = False
        items.cloth -= 1
    else:
        click.echo('You dont have enough of that')




@click.command()
def exit():
    if dungeon.player.position.is_exit:
        click.echo("You have escaped the dungeon!")
        exit()
    else:
        click.echo("There is no exit here!")

@click.command()
def inventory():
    # print(dungeon.player.position.contents)
    count = 1
    click.echo(f'{green}Inventory:{reset}')
    for item in dungeon.player.inventory.keys():
        click.echo(f"({item}) {yellow}{dungeon.player.inventory[item].name}{reset}")

@click.command()
@click.argument("treasure_key", type=str)
def grab(treasure_key):
    if treasure_key not in dungeon.player.position.contents:
        click.echo("That is not a real treasure.")
        return
    else:
        element = dungeon.player.position.contents.pop(treasure_key)
        dungeon.player.inventory[str(treasure_key)] = element
        player.curr_score += element.value
        click.echo(f"You have picked up the {yellow}{element.name}{reset}.")
        session.add(Score(score=player.curr_score))
        session.commit()
       


@click.command()
@click.argument("treasure_key", type=str)
def drop(treasure_key):
    if treasure_key not in dungeon.player.inventory.keys():
        click.echo("You don't have that treasure.")
        return
    else:
        element = dungeon.player.inventory.pop(treasure_key)
        dungeon.player.position.contents[str(treasure_key)] = element
        player.curr_score -= element.value
        click.echo(f"You have {red}dropped{reset} the {yellow}{element.name}{reset}.")

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
        click.echo(f"{yellow}{t_name}{reset} is a treasure worth 🤑 {yellow}{t_value}{reset} gold pieces. It weighs ⚖️  {blue}{t_weight}{reset} pounds. {green}{t_desc}{reset}")


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
cli.add_command(disarm)
cli.add_command(bandage)
cli.add_command(exit)
cli.add_command(inventory)
cli.add_command(grab)
cli.add_command(appraise)
cli.add_command(drop)
if __name__ == "__main__":
    while True:
        # click.echo(dungeon.player.position.contents)
        click.echo(f"You are in the 📍 {blue}{dungeon.player.position.room_name}{reset}")
        click.echo(f'Your current Score: {yellow}{player.curr_score}{reset}')
        if player.max_hp > 4:
            click.echo(f"Player Health Points: {green}{player.max_hp}{reset}")
        elif player.max_hp >0 and player.max_hp <= 4:
            click.echo(f"Player Health Points: {red}{player.max_hp}{reset}")
        cmd = click.prompt("What do you want to do?",type=str)
        cmd_parts = cmd.split()
        try:
            click.clear()
            cli(cmd_parts)
        except SystemExit:
            pass
        if player.max_hp <= 0:
            click.clear()
            click.echo(f'{red}{trap.game_over}{reset}')
            click.echo(f'{red}Unfortunatly you have bled out!{reset}'.center(500))
            click.echo(f'{blue}Total Loot Score {yellow}{player.curr_score}{reset}'.center(500))
            break