class Room:
    def __init__(self, name, base_description, items=None, npcs=None):
        self.name = name
        self.base_description = base_description
        self.items = items if items else []
        self.npcs = npcs if npcs else []
        self.linked_rooms = {'N': None, 'E': None, 'S': None, 'W': None}
        self.locks = {'N': None, 'E': None, 'S': None, 'W': None}

    def get_name(self):
        return self.name

    def get_description(self):
        # Base room description
        description = self.base_description

        # Add room item descriptions
        if self.items:
            description += "\nYou see a "
            if len(self.items) > 2:
                description += ", ".join([item.get_name() for item in self.items[:-1]])
                description += ", and a " + self.items[-1].get_name()
            elif len(self.items) == 2:
                description += self.items[0].get_name() + " and a " + self.items[1].get_name()
            else:
                description += self.items[0].get_name()
            description += " here."

        # Add room NPC descriptions
        if self.npcs:
            description += "\nA "
            if len(self.npcs) > 2:
                description += ", ".join([npc.get_name() for npc in self.npcs[:-1]])
                description += ", and " + self.npcs[-1].get_name()
                description += " are"
            elif len(self.npcs) == 2:
                description += self.npcs[0].get_name() + " and " + self.npcs[1].get_name()
                description += " are"
            else:
                description += self.npcs[0].get_name()
                description += " is"
            description += " here."

        # Add room doors (linked rooms)
        direction_names = {'N': 'north', 'E': 'east', 'S': 'south', 'W': 'west'}
        directions = [direction_names[direction] for direction, room in self.linked_rooms.items() if room]
        description += "\nThere "
        if len(directions) == 0:
            description += "are no exits."
        elif len(directions) == 1:
            description += f"is a door to the {directions[0]}."
        elif len(directions) >= 2:
            description += f"are doors to the {', '.join(directions[:-1])}, and {directions[-1]}."

        return description

    def get_items(self):
        return self.items

    def get_npcs(self):
        return self.npcs

    def get_linked_room(self, direction):
        return self.linked_rooms.get(direction)

    def get_lock(self, direction):
        return self.locks.get(direction)

    def link_room(self, room, direction, lock=None):
        if direction in self.linked_rooms:
            self.linked_rooms[direction] = room
            self.locks[direction] = lock

    def set_lock(self, direction, lock_id):
        self.locks[direction] = lock_id

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def add_npc(self, npc):
        self.npcs.append(npc)

    def remove_npc(self, npc):
        if npc in self.npcs:
            self.npcs.remove(npc)