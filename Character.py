class Character:
    def __init__(self, name, description, health=100, inventory=None, current_room=None):
        self.name = name
        self.description = description
        self.health = health
        self.inventory = inventory if inventory else []
        self.current_room = current_room

    def get_name(self):
        return self.name

    def get_health(self):
        return self.health

    def get_inventory(self):
        return self.inventory

    def get_current_room(self):
        return self.current_room

    def show_description(self):
        print(self.description)

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def move_to_room(self, room):
        self.current_room = room
