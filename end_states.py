from enum import Enum
import click
from functools import reduce
import sys

class EndState(Enum):
    WON = 0
    DEAD = 1
    SWALLOWED = 2

# Pass in the DungeonMap object so we can access the game information
def end_game(end_condition:EndState,dungeon):
    if end_condition == EndState.WON:
        click.echo("You have escaped the cave of Chameleos!")
        click.echo("Now let's see how you did...")
        if(list(dungeon.player.inventory) == []):
            click.echo("You have not found any treasures.")
        else:
            display_inventory_treasures(dungeon)
            display_missed_treasures(dungeon)
    elif end_condition == EndState.DEAD:
        click.clear()
        click.echo("You have died.")
    elif end_condition == EndState.SWALLOWED:
        click.clear()
        click.echo("You have been swallowed by Chameleos.")
    # Exit the game
    raise click.exceptions.Exit(0)
def display_missed_treasures(dungeon):
    n = 0
    listing_count = 1
    final_inventory = set(dungeon.player.inventory.values())
    dungeon_inventory = set(dungeon.dungeon_treasures)
    click.echo(f"You have missed {len(dungeon.dungeon_treasures)} treasures:")
    dungeon_inventory.difference_update(final_inventory)
    dungeon_inventory = list(dungeon_inventory)
    while len(dungeon_inventory) != listing_count - 1:
        foursection = dungeon_inventory[n:n+4]
        if(len(foursection) < 4):
            foursection = dungeon_inventory[n:len(dungeon_inventory)]
        else:
            n += 4
        click.pause("Missed #"+str(listing_count)+": "+foursection[0].name+" with a value of "+str(foursection[0].value))
        listing_count += 1
        for treasure in foursection[1:]:
            click.echo("Missed #"+str(listing_count)+": "+treasure.name+" with a value of "+str(treasure.value))
            listing_count += 1
    click.echo("Total Value of Missed Treasures: "+ str(reduce(lambda a,b:a+b, [treasure.value for treasure in dungeon_inventory])))

def display_inventory_treasures(dungeon):
    click.echo("Treasures Found: " +str(len(dungeon.player.inventory)))
    # Display four treasures in the player's inventory at a time.
    n = 0
    listing_count = 1
    final_inventory = list(dungeon.player.inventory.values())
    while len(final_inventory) != listing_count - 1:
        foursection = final_inventory[n:n+4]
        if(len(foursection) < 4):
            foursection = final_inventory[n:len(final_inventory)]
        else:
            n += 4
        click.pause("Missed #"+str(listing_count)+": "+foursection[0].name+" with a value of "+str(foursection[0].value))
        listing_count += 1
        for treasure in foursection[1:]:
            click.echo("Missed #"+str(listing_count)+": "+treasure.name+" with a value of "+str(treasure.value))
            listing_count += 1
    click.echo("Total Value of Treasures Found: " + str(reduce(lambda a,b:a+b, [treasure.value for treasure in final_inventory])))
