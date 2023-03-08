from dungeon_map import DungeonMap,generate_dungeon
from direction import Direction
import click
import random
from traps import Trap
from colorama import Fore, Back, Style
from items import Items
from entities import Player




#colors
reset = Style.RESET_ALL
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
blue = Fore.BLUE
trap_exists = True
trap_found = False

player = Player()
traps = Trap.traps
trap = Trap()
items = Items()

dungeon = generate_dungeon(100)

@click.command
@click.argument("direction", type=click.Choice([d.value for d in Direction]))
def go(direction):
    if dungeon.move_player(direction):
        click.echo(f"You are now in {green}{dungeon.player_location.name}{reset}")
        if trap.found == True:
            click.echo(f"You got cought in {red}Trap{reset}")
            trap.bleed = True
            trap.found = False
        if trap.bleed == True:
            click.echo(f"You are {red}bleeding{reset}")
            player.hp -= 5






@click.command
def look():
    for direction in dungeon.rooms[dungeon.player_location].items():
        click.echo(f"There is a room to the {blue}{direction[0]}{reset}.")
    trap_name = random.choice(list(traps.keys()))
    if random.random() < 0.2:
        trap.found = True
        click.echo(f'Watch out for that {red}{trap_name}{reset} trap')
    if random.random() < 0.1:
        items.cloth += 1
        click.echo(f'you found {green}cloth{reset} which can be used as a {green}bandage{reset}')


@click.command
def disarm():
    trap.found = False
    click.echo(f'Successfully disarmed trap')
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



    

@click.group()
def cli():
    pass
                
cli.add_command(go)
cli.add_command(look)
cli.add_command(disarm)
cli.add_command(bandage)




if __name__ == "__main__":
    while True:
        click.echo(f"You are in the {green}{dungeon.player_location.name}{reset}")
        click.echo(f"Your health {green}{player.hp}{reset}")
        cmd = click.prompt("What do you want to do?",type=str)
        cmd_parts = cmd.split()
        try:
            click.clear()
            cli(cmd_parts)
        except SystemExit:
            pass
