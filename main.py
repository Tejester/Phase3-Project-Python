from dungeon_map import DungeonMap,generate_dungeon
from direction import Direction
import click

dungeon = generate_dungeon(100)

@click.command
@click.argument("direction", type=click.Choice([d.value for d in Direction]))
def go(direction):
    if dungeon.move_player(direction):
        click.echo(f"You are now in room {dungeon.player_location}")

@click.command
def look():
    for direction in dungeon.rooms[dungeon.player_location].items():
        click.echo(f"There is a room to the {direction}.")

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