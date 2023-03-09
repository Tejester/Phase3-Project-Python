from enum import Enum
import click
from click import style
from dungeon_colors import MessageColors
from functools import reduce
import sys
from sqlalchemy import create_engine, Column, Integer, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///scores.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class ScoreTable(Base):
    __tablename__ = 'scoretable'
    id = Column(Integer, primary_key=True)
    score = Column(Integer)

class EndState(Enum):
    WON = 0
    DEAD = 1
    SWALLOWED = 2

# Pass in the DungeonMap object so we can access the game information
def end_game(end_condition:EndState,dungeon):
    Base.metadata.create_all(engine)
    if end_condition == EndState.WON:
        click.echo(style("You have escaped the cave of Chameleos!",MessageColors.GOOD.value))
        click.echo(style("Now let's see how you did...",MessageColors.GOOD.value))
        if(list(dungeon.player.inventory) == []):
            click.echo(style("You have not found any treasures.",MessageColors.BAD.value))
        else:
            display_inventory_treasures(dungeon)
            display_missed_treasures(dungeon)
            click.echo("Score saved to database!")
    elif end_condition == EndState.DEAD:
        click.clear()
        click.echo(style("You have died.",MessageColors.BAD.value))
    elif end_condition == EndState.SWALLOWED:
        click.clear()
        click.echo(style("You have been swallowed by Chameleos.",MessageColors.BAD.value))
    # Exit the game
    raise click.exceptions.Exit(0)
def display_missed_treasures(dungeon):
    n = 0
    listing_count = 1
    final_inventory = set(dungeon.player.inventory.values())
    dungeon_inventory = set(dungeon.dungeon_treasures)
    click.echo(style(f"You have missed {len(dungeon.dungeon_treasures)} treasures:",MessageColors.TREASURE.value))
    dungeon_inventory.difference_update(final_inventory)
    dungeon_inventory = list(dungeon_inventory)
    while len(dungeon_inventory) != listing_count - 1:
        foursection = dungeon_inventory[n:n+4]
        if(len(foursection) < 4):
            foursection = dungeon_inventory[n:len(dungeon_inventory)]
        else:
            n += 4
        click.pause(style("Missed #"+str(listing_count)+": "+foursection[0].name+" with a value of "+str(foursection[0].value),MessageColors.TREASURE.value))
        listing_count += 1
        for treasure in foursection[1:]:
            click.echo(style("Missed #"+str(listing_count)+": "+treasure.name+" with a value of "+str(treasure.value),MessageColors.TREASURE.value))
            listing_count += 1
    click.echo(style("Total Value of Missed Treasures: "+ str(reduce(lambda a,b:a+b, [treasure.value for treasure in dungeon_inventory])),MessageColors.TREASURE.value))

def display_inventory_treasures(dungeon):
    session = Session()
    click.echo(style("Treasures Found: " +str(len(dungeon.player.inventory)),MessageColors.TREASURE.value))
    # Display four treasures in the player's inventory at a time.
    n = 0
    listing_count = 1
    final_inventory = list(dungeon.player.inventory.values())
    my_score = reduce(lambda a,b:a+b, [treasure.value for treasure in final_inventory])
    new_score = ScoreTable(score=my_score)
    session.add(new_score)
    session.commit()
    session.close()
    while len(final_inventory) != listing_count - 1:
        foursection = final_inventory[n:n+4]
        if(len(foursection) < 4):
            foursection = final_inventory[n:len(final_inventory)]
        else:
            n += 4
        click.pause(style("Missed #"+str(listing_count)+": "+foursection[0].name+" with a value of "+str(foursection[0].value),MessageColors.TREASURE.value))
        listing_count += 1
        for treasure in foursection[1:]:
            click.echo(style("Missed #"+str(listing_count)+": "+treasure.name+" with a value of "+str(treasure.value),MessageColors.TREASURE.value))
            listing_count += 1
    click.echo(style("Total Value of Treasures Found: " + str(reduce(lambda a,b:a+b, [treasure.value for treasure in final_inventory])),MessageColors.TREASURE.value))
