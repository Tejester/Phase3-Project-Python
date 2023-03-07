class Entity:
    def __init__(self,name):
        self.name = name

    @property.getter
    def name(self):
        return self.name
    @property.setter
    def name(self,value):
        self.name = value

    @property.getter
    def hp(self):
        return self.hp
    @property.setter
    def hp(self,value):
        self.hp = value

    @property.getter
    def max_hp(self):
        return self.max_hp
    @property.setter
    def max_hp(self,value):
        self.max_hp = value

    @property.getter
    def strength(self):
        return self.strength
    @property.setter
    def strength(self,value):
        self.strength = value

    @property.getter
    def dexterity(self):
        return self.dexterity
    @property.setter
    def dexterity(self,value):
        self.dexterity = value
    
    @property.getter
    def constitution(self):
        return self.constitution
    @property.setter
    def constitution(self,value):
        self.constitution = value
    
    @property.getter
    def intelligence(self):
        return self.intelligence
    @property.setter
    def intelligence(self,value):
        self.intelligence = value
    
    @property.getter
    def wisdom(self):
        return self.wisdom
    @property.setter
    def wisdom(self,value):
        self.wisdom = value
    
    @property.getter
    def charisma(self):
        return self.charisma
    @property.setter
    def charisma(self,value):
        self.charisma = value
    
    # All the other stats are derived from the 6 main stats.
    # For that reason, they should not be settable directly.
    # Monsters that affect these values will have to use special mutator methods.
    @property.getter
    def armor_class(self):
        return self.armor_class
    
    @property.getter
    def initiative(self):
        return self.initiative
    

class Player(Entity):
    def __init__(self,name):
        super().__init__(name)