from parent_class import Item 

class Weapon(Item):
    def __init__(self, name, description, damage, affect):
        super().__init__(name, description, damage)
        self.affect = affect 
        
    def use(self):
        print(f"You've equipped {self.name}")

flatiron_sword = Weapon()


