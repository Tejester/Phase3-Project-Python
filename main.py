import markovify
from dungeon_map import DungeonMap,generate_dungeon
from direction import Direction
import click

dungeon = generate_dungeon(100)

@click.command
@click.argument("direction", type=click.Choice([d.value for d in Direction]))
def go(direction):
    if dungeon.move_player(direction):
        click.echo(f"You are now in {dungeon.player_location.name}")

@click.command
def look():
    for direction in dungeon.rooms[dungeon.player_location].items():
        click.echo(f"There is a room to the {direction[0]}.")

@click.group()
def cli():
    pass
                
cli.add_command(go)
cli.add_command(look)

if __name__ == "__main__":
    while True:
        click.clear()
        click.echo("You are in the " + dungeon.player_location.name)
        cmd = click.prompt("What do you want to do?",type=str)
        cmd_parts = cmd.split()
        try:
            click.clear()
            cli(cmd_parts)
        except SystemExit:
            pass