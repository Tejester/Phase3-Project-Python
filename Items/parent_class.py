class Item:
    def __init__(self, name, description, damage):
        self.name = name
        self.description = description
        self.damage = damage
        
    def use(self):
        print(f"You've picked up the {self.name}!")