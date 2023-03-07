from enum import Enum

# This defines all the floor ranges for difficulty, monster, loot generation, etc.
# Dungeon is about 25 levels deep
class FloorRanges(Enum):
    MEADOWS = 1
    HARDERMEADOWS = 2
    LUSHMEADOWS = range(3,5)
    FOREST = range(5,7)
    DEEPFOREST = range(7,10)
    CRYPT = range(10,13)
    ANCIENTCRYPT = range(13,15)
    SPIRE = range(15,17)
    DARKSPIRE = range(17,19)
    PALACE = range(19,22)
    IMMORTALPALACE = range(22,25)
