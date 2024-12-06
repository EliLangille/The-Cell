from Combat import Combat
from Key import Key


class Commands:
    def __init__(self, player):
        self.player = player

    def process_command(self, command):
        command = command.lower()
        parts = command.split(" ")
        if not parts:
            return ValueError("No command entered.")

        action = parts[0]
        match action:
            case "help":
                self.help()
            case "look":
                if len(parts) == 1 or command == "look at room":
                    self.look()
                else:
                    self.look_at(parts[2])
            case "health" | "inventory" | "show":
                if command == "show inventory" or command == "inventory":
                    self.show_inventory()
                elif command == "show health" or command == "health":
                    self.show_health()
                else:
                    print("Invalid command.")
            case "go" | "move":
                if len(parts) == 1:
                    print("Please specify a direction.")
                else:
                    self.move(parts[1])
            case "get" | "grab" | "take":
                self.take(parts[1])
            case "unlock":
                self.unlock(parts[1])
            case "talk":
                self.talk(parts[:-1])
            case _:
                print("Invalid command.")

    @staticmethod
    def help():
        print("COMMANDS:")
        print("help - Show available commands")
        print("look - Look around the room")
        print("look at [item] - Look at a specific item in the room or your inventory")
        print("health - Show player health")
        print("inventory - Show player inventory")
        print("go/move [north/east/south/west] - Move in a specified direction")
        print("get/take/grab [item] - Pick up an item in the room")
        print("unlock [direction] - Unlock a door in a specified direction")
        print("talk [npc] - Talk to an NPC")

    def look(self):
        room = self.player.get_current_room()
        print(room.get_description())

    def look_at(self, item_or_npc_name):
        # Check if object is an NPC in the room, an item in the room, or an item in inventory
        room = self.player.get_current_room()
        npc = next((npc for npc in room.get_npcs() if npc.get_name().lower() == item_or_npc_name), None)
        if npc:
            npc.show_description()
            return

        item = next((item for item in room.get_items() if item.get_name() == item_or_npc_name), None)
        if item:
            item.show_description()
            return

        item = next((item for item in self.player.get_inventory() if item.get_name() == item_or_npc_name), None)
        if item:
            item.show_description()
            return

        print("This character or object is not here.")

    def show_inventory(self):
        self.player.show_inventory()

    def show_health(self):
        self.player.show_health()

    def move(self, direction):
        room = self.player.get_current_room()
        next_room = room.get_linked_room(direction)
        if next_room:
            self.player.move_to_room(next_room)
            self.look()

            # Start combat is hostile NPC is in the room
            npc = next((npc for npc in next_room.get_npcs() if npc.is_hostile()), None)
            if npc:
                print(f"You have encountered the {npc.get_name()}!")
                combat = Combat(self.player, npc)
                combat.start_combat()
        else:
            print("You cannot move in that direction.")

    def take(self, item_name):
        room = self.player.get_current_room()
        item = next((item for item in room.get_items() if item.get_name().lower() == item_name), None)
        if item:
            self.player.add_item(item)
            room.remove_item(item)
            print(f"You picked up the {item_name}.")
        else:
            print("That item is not here.")

    def unlock(self, direction):
        direction = direction.upper()
        if direction not in ['N', 'E', 'S', 'W']:
            print("Invalid direction.")
            return

        room = self.player.get_current_room()
        lock = room.get_lock(direction)

        if lock:
            # Get all Key objects in inventory
            keys = [item for item in self.player.get_inventory() if isinstance(item, Key)]

            # If keys in inventory, try them all on the door
            if keys:
                for key in keys:
                    if key.get_lock() == lock:
                        room.set_lock(direction, None)
                        print(f"Unlocked the door to the {direction}.")
                        return

            print("You do not have the key to unlock this door.")

    def talk(self, npc_name):
        room = self.player.get_current_room()
        npc = next((npc for npc in room.get_npcs() if npc.get_name().lower() == npc_name), None)
        if npc:
            npc.talk()
        else:
            print(f"There is no {npc_name} here.")
