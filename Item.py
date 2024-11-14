class Item:
    def __init__(self, name, description, damage=1):
        self.name = name
        self.description = description
        self.damage = damage

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_damage(self):
        return self.damage
