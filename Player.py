from Character import Character


class Player(Character):
    def __init__(self, name, description, health=100, inventory=None, current_room=None):
        super().__init__(name, description, health, inventory, current_room)

    def show_inventory(self):
        print("INVENTORY:")
        for item in self.inventory:
            print(f"{item.get_name()} - {item.get_description()} - {item.get_damage()} damage")
