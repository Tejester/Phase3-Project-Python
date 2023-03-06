from parent_class import Item 

class Potion(Item):
    def __init__(self, name, description, damage, affect):
        super().__init__(name, description, damage)
        self.affect = affect 
        
    def use(self):
        print(f"You drink the {self.name} and heal {self.healing} HP!")


