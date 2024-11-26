import random


class CombatSystem:
    def __init__(self, player, npc):
        self.player = player
        self.npc = npc
        self.turn = "player" if player.get_current_room() == npc.get_current_room() else "npc"

    def start_combat(self):
        print(f"Combat initiated between {self.player.get_name()} and {self.npc.get_name()}!")
        while self.player.get_health() > 0 and self.npc.get_health() > 0:
            if self.turn == "player":
                self.player_turn()
                self.turn = "npc"
            else:
                self.npc_turn()
                self.turn = "player"

        self.end_combat()

    def player_turn(self):
        print("Player's turn:")
        action = input("Choose an action: (1) Attack (2) Flee: ")
        if action == "1":
            self.attack(self.player, self.npc)
        elif action == "2":
            self.flee(self.player)
        else:
            print("Invalid action. Turn forfeited.")

    def npc_turn(self):
        print("NPC's turn:")
        self.attack(self.npc, self.player)

    def attack(self, attacker, defender):
        weapon = input(f"Choose a weapon from inventory or type 'bare hands': ")
        if weapon == "bare hands":
            damage = 10  # Example damage value for bare hands
        else:
            item = next((item for item in attacker.get_inventory() if item.get_name() == weapon), None)
            if item:
                damage = item.get_damage()
            else:
                print("Invalid weapon. Turn forfeited.")
                return

        defender.health -= damage
        print(f"{attacker.get_name()} attacks {defender.get_name()} with {weapon} for {damage} damage!")

    def flee(self, character):
        if random.choice([True, False]):
            print(f"{character.get_name()} successfully fled the combat!")
            self.end_combat(fled=True)
        else:
            print(f"{character.get_name()} failed to flee and forfeits their turn.")

    def end_combat(self, fled=False):
        if fled:
            return

        if self.player.get_health() <= 0:
            print(f"{self.player.get_name()} has been defeated! Game Over.")
            exit()
        elif self.npc.get_health() <= 0:
            print(f"{self.npc.get_name()} has been defeated!")
            self.drop_inventory(self.npc)

    def drop_inventory(self, character):
        print(f"{character.get_name()} drops their inventory:")
        for item in character.get_inventory():
            print(f"- {item.get_name()}")
            self.player.get_current_room().add_item(item)
        character.inventory.clear()
