import markovify
from dungeon_map import DungeonMap,generate_dungeon
# from room import Door
from direction import Direction
import click
from room import InteractionMessages

dungeon = generate_dungeon(100,99,50)

@click.command()
@click.argument("direction", type=click.Choice([d.value for d in Direction]))
def go(direction):
    if dungeon.move_player(direction):
        click.echo(f"You move to {dungeon.player.position.room_name}")
    if dungeon.player.position.is_exit:
        click.echo("This is an exit!")


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
        click.echo("You have escaped the dungeon!")
        exit()
    else:
        click.echo("There is no exit here!")

@click.command()
def inventory():
    print(dungeon.player.position.contents)
    count = 1
    for item in dungeon.player.inventory.keys():
        click.echo(f"{item}. {dungeon.player.inventory[item].name}")

@click.command()
@click.argument("treasure_key", type=click.Choice([key for key in dungeon.player.position.contents.keys()]))
def grab(treasure_key):
    element = dungeon.player.position.contents.pop(treasure_key)
    dungeon.player.inventory[str(treasure_key)] = element


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

if __name__ == "__main__":
    while True:
        click.echo("You are in the " + dungeon.player.position.room_name)
        cmd = click.prompt("What do you want to do?",type=str)
        cmd_parts = cmd.split()
        try:
            # click.clear()
            cli(cmd_parts)
        except SystemExit:
            pass