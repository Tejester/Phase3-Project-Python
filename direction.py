from enum import Enum

# This defines all the room types

class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    NORTHEAST = "NE"
    SOUTHEAST = "SE"
    NORTHWEST = "NW"
    SOUTHWEST = "SW"