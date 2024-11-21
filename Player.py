import Character


class Player(Character):
    def __init__(self, name, description, health=100):
        super().__init__(name, description, health)

    def show_health(self):
        print(f"HEALTH: {self.health}")

    def show_inventory(self):
        print("INVENTORY:\n")
        for item in self.inventory:
            print(f"{item.get_name()} - {item.get_description()} - {item.get_damage()} damage")
