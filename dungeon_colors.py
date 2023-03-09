from enum import Enum

class MessageColors(Enum):
    # Shrimp color rgb value, peach/pink
    SHRIMP = (255,218,185)
    # Bad color rgb value. Red, duh!
    BAD = (255,0,0)
    # Chameleos color rgb value. He is green. This is for chameleos actions
    CHAMELEOS = (0,255,0)
    # Treasure color rgb value. Yellow
    TREASURE = (255,215,0)
    # Color when something good happens. Should be Sky Blue
    GOOD = (135,206,250)
    # Color for player actions and directions. A bright neon purple
    PLAYER = (255,0,255)
    # Color for location names. A bright neon blue
    LOCATION = (0,0,255)
