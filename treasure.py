import random

treasure_adjectives = ["shiny","rusty","old","new","broken","cracked","dented","crusty","dirty","clean","polished","dull","bent","worn","tarnished","chipped","scratched",
"cracked","crumbling","flaking","flimsy","fragile","frayed", "faded","fancy","fashionable","filthy","fluffy","fuzzy","glossy","grubby","grungy","grubby","grungy",
"encrusted", "etched", "exquisite", "fancy", "fine", "glittering", "glistening", "glowing", "gold", "golden", "gorgeous", "heavy", "impressive", "jeweled", "jewelled",
"salmon-scaled","shimmering","shiny","silver","silvered","sparkling","stained","stunning","tarnished","tattered","torn","tattered","torn","tattered","torn","tattered"]

treasure_nouns = ["coin","gem","jewel","ring","necklace","bracelet","earring","pendant","amulet","crown","tiara","scepter","sceptre","wand","staff","orb","crystal",
                  "gemstone","bracer","bangle","brooch","cufflink","locket","medallion","necklace","pendant","pin","ring","talisman","trinket","treasure","sword",
                  "dubloon","ducat","moonstone","sapphire","ruby","emerald","diamond","pearl","topaz","amethyst","opal","onyx","jade","obsidian","quartz","agate",
                  "amber","garnet","peridot","citrine","zircon","tourmaline","agate","amber","garnet","peridot","citrine","zircon","tourmaline","agate","amber",
                  "spoon","fork","knife","spork"]

treasure_descriptions = ["Has the symbol of a chicken on it.","Has the symbol of a cow on it.","Has the symbol of a dog on it.","Has the symbol of a cat on it.",
                         "Has a weird gem encrusted into it.","Could be used as a toothpick","Has a funny smell","Has a funny taste","Has a funny texture",
                         "Makes a funny jingle.","Seems to be singing.","Has a peculiar glow","Has a peculiar glow","It is dripping with blood","Feels like it is alive",
                         "Almost seems to be capturing your very soul.","Tastes like candy","Looks cheap.","Looks expensive.","Tastes like chicken.","Looking at it makes you dizzy",
                         "Looking at it makes you sad","Looking at it makes you happy","Looking at it makes you angry","Looking at it makes you sleepy","Looking at it makes you hungry",
                         "Makes your stomach hurt","Makes your head hurt","Makes your eyes hurt","Makes your ears hurt","Makes your nose hurt","Makes your mouth hurt",
                         "Makes your blood curdle","Makes your blood boil","Makes your blood freeze","Makes your blood run cold","Makes your blood run hot","Makes your blood run warm",
                         "Makes you constipated","You suddenly want to burst into laughter","You suddenly feel the urge to laugh"]



class Treasure:
    def __init__(self,name:str,desc:str,value:int,weight:int):
        self._name = name
        self._desc = desc
        self._value = value
        self._weight = weight

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,value):
        self._name = value

    @property
    def desc(self):
        return self._desc
    
    @desc.setter
    def desc(self,value):
        self._desc = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self,price):
        self._value = price

    @property
    def weight(self):
        return self._weight
    
    @weight.setter
    def weight(self,value):
        self._weight = value


def generate_treasures(treasure_count):
    treasures = []
    for i in range(treasure_count):
        random_name = random.choice(treasure_adjectives).title() + " " + random.choice(treasure_nouns).title()
        random_description = random.choice(treasure_descriptions)
        random_value = random.randint(10,100000)
        random_weight = random.randint(10,100)
        treasures.append(Treasure(random_name,random_description,random_value,random_weight))
    return treasures

