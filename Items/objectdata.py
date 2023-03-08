from models import Weapon, Hero, Enemy, Trap, Room
from database import session

weapon_data = {
    "Dagger": {"price": 25, "damage": 15},
    "Sword": {"price": 50, "damage": 20},
    "Axe": {"price": 100, "damage": 25},
    "Bow": {"price": 200, "damage": 30},
}

weapons = []
for name, data in weapon_data.items():
    weapon = Weapon(name=name, damage=data["damage"])
    weapons.append(weapon)

session.bulk_save_objects(weapons)

hero_data = {
    "Berserk": {"price": 75, "health": 150, "damage": 10},
    "Knight": {"price": 100, "health": 120, "damage": 20},
    "Thief": {"price": 125, "health": 110, "damage": 15},
    "Healer": {"price": 150, "health": 100, "damage": 12}
}

heroes = []
for name, data in hero_data.items():
    hero = Hero(name=name, health=data["health"], damage=data["damage"])
    heroes.append(hero)

session.bulk_save_objects(heroes)

enemy_data = {
    "Goblin": {"health": 80, "damage": 5, "gold": 10},
    "Troll": {"health": 100, "damage": 10, "gold": 25},
    "WereWolf": {"health": 150, "damage": 15, "gold": 30},
    "Vampire": {"health": 180, "damage": 20, "gold": 50},
    "Dragon": {"health": 200, "damage": 25, "gold": 60}
}

enemies = []
for name, data in enemy_data.items():
    enemy = Enemy(name=name, health=data["health"], damage=data["damage"], gold=data["gold"])
    enemies.append(enemy)

boss = Enemy(name="The Dark Lord", health=1000, damage=30, gold=1003)
enemies.append(boss)

session.bulk_save_objects(enemies)

trap_data = {
    "crossbow": {"damage": 10},
    "hole": {"damage": 5},
    "beartrap": {"damage": 8}
}

traps = []
for name, data in trap_data.items():
    trap = Trap(name=name, damage=data["damage"])
    traps.append(trap)

session.bulk_save_objects(traps)

room_data = {
    "Grotto of the Mad Forest": {},
    "Maze of the Spirit's Cult": {},
    "Crypt of the Cruel Paladin": {},
    "Tombs of the Vanishing Horsemen": {},
    "The Swamp Point": {},
    "The Perfumed Tunnels": {},
    "The Wondering Haunt": {},
    "The Ethereal Pits": {},
    "The Mesmerizing Haunt": {},
    "The Nether Delves": {},
}

rooms = []
for name, data in room_data.items():
    room = Room(name=name)
    rooms.append(room)

adjective_data= {
    "Abandoned": {},
    "Dilapidated": {},
    "Dusty": {},
    "Eerie": {},
    "Elegant": {},
    "Empty": {},
    "Enchanted": {},
    "Enormous": {},
    "Fancy": {},
    "Frightening": {},
    "Gloomy": {},
    "Haunted": {},
    "Huge": {},
    "Imposing": {},
    "Impressive": {},
}

session.bulk_save_objects(rooms)

session.commit()

stmt = session.query(Weapon).all()
for row in stmt:
    print(row.name, row.damage)

stmt = session.query(Hero).all()
for row in stmt:
    print(row.name, row.health, row.damage)

stmt = session.query(Enemy).all()
for row in stmt:
    print(row.name, row.health, row.damage, row.gold)


