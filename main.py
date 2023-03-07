from dungeon_map import DungeonMap,generate_dungeon
from direction import Direction
import click
from enemy import Enemy
import random
import os
from traps import Trap

# monster info
monsters = Enemy.monsters
monster_name = random.choice(list(monsters.keys()))
monster_health = monsters[monster_name]["health"]
monster_damage = monsters[monster_name]["damage"]
monster_gold = monsters[monster_name]["gold"]

#traps


dungeon = generate_dungeon(100)

@click.command
@click.argument("direction", type=click.Choice([d.value for d in Direction]))
def go(direction):
    if dungeon.move_player(direction):
        os.system('clear')
        click.echo(f"You are now in room {dungeon.player_location}")

@click.command
def look():
    for direction in dungeon.rooms[dungeon.player_location].items():
        click.echo(f"There is a room to the {direction}.")
    if random.random() < 0.2:
        traps = Trap.traps
        trap_name = random.choice(list(traps.keys()))
        trap_dmg = traps[trap_name]["damage"]
        click.echo(f"There is a {trap_name} trap, you should disarm it!")
                

@click.group()
def cli():
    pass
                
cli.add_command(go)
cli.add_command(look)



if __name__ == "__main__":
    while True:
        cmd = click.prompt("What do you want to do?",type=str)
        cmd_parts = cmd.split()
        try:
            cli(cmd_parts)
        except SystemExit:
            pass
