import markovify
from dungeon_map import DungeonMap, generate_dungeon
from direction import Direction
import click
from chameleon import Chameleon

chameleon = Chameleon()
dungeon = generate_dungeon(100, chameleon)

@click.command()
@click.argument("direction", type=click.Choice([d.value for d in Direction]))
def go(direction):
    if dungeon.move_player(direction):
        click.echo(f"You are now in {dungeon.player_location.name}")

@click.command()
def look():
    for direction in dungeon.rooms[dungeon.player_location].items():
        click.echo(f"There is a room to the {direction[0]}.")

@click.command()
@click.pass_obj("chameleon")
def chase(chameleon):
    click.echo("The chameleon is chasing you!")
    while chameleon.current_room != dungeon.player_location:
        noise_scale = chameleon.move_towards_player(dungeon)
        click.echo(f"The chameleon moved {noise_scale} units")

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = {"chameleon": chameleon}

cli.add_command(go)
cli.add_command(look)
cli.add_command(chase)

if __name__ == "__main__":
    while True:
        click.clear()
        click.echo("You are in the " + dungeon.player_location.name)
        cmd = click.prompt("What do you want to do?", type=str)
        cmd_parts = cmd.split()
        try:
            click.clear()
            cli(obj={"chameleon": chameleon}).invoke(cmd_parts)
        except SystemExit:
            pass

    cli(obj={"chameleon": chameleon}).run()
