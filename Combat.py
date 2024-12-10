import random


class Combat:
    def __init__(self, player, npc):
        self.player = player
        self.npc = npc
        self.turn = "player"

    def start_combat(self):
        print(f"\nCombat initiated between {self.player.get_name()} and {self.npc.get_name()}!")
        while self.player.get_health() > 0 and self.npc.get_health() > 0:
            if self.turn == "player":
                self.player_turn()
                self.turn = "npc"
            else:
                self.npc_turn()
                self.turn = "player"

        self.end_combat()

    def player_turn(self):
        print(f"{self.player.get_name()}'s turn:")
        self.player.show_health()
        self.npc.show_health()
        self.attack(self.player, self.npc)

    def npc_turn(self):
        print(f"{self.npc.get_name()}'s turn:")
        self.player.show_health()
        self.npc.show_health()
        self.attack(self.npc, self.player)

    def attack(self, attacker, defender):
        # if inventory empty, attack with fists
        if not attacker.get_inventory():
            weapon_name = "Fists"
            if attacker == self.player:
                damage = 3
            else:
                damage = 6
        else:
            # if attacker is of npc instance, pick item with the highest damage
            if attacker == self.npc:
                weapon = max(attacker.get_inventory(), key=lambda item: item.get_damage())
                damage = weapon.get_damage()

                # If fists better than item, use fists
                if damage < 6:
                    weapon_name = "Fists"
                    damage = 6
                else:
                    weapon_name = weapon.get_name()
            else:
                prompt = f"\nChoose a weapon to attack with: {', '.join([item.get_name() for item in attacker.get_inventory()])}\n> "
                weapon_name = input(prompt).title()

                weapon = next((item for item in attacker.get_inventory() if item.get_name() == weapon_name), None)
                if not weapon:
                    print("You don't have this weapon, your foe attacks instead.")
                    return

                damage = weapon.get_damage()

        damage_variance = random.randint(-2, 2)
        damage += damage_variance

        defender.health -= damage
        print(
            f"{attacker.get_name()} attacks {defender.get_name()} with {weapon_name} for {damage} damage!\n")

    def end_combat(self):
        if self.player.get_health() <= 0:
            print(f"{self.player.get_name()} has been defeated!")
        elif self.npc.get_health() <= 0:
            print(f"{self.npc.get_name()} has been defeated!")
            self.drop_inventory(self.npc)
            # Delete npc
            self.player.get_current_room().remove_npc(self.npc)

    def drop_inventory(self, character):
        print(f"{character.get_name()} drops their inventory:")
        for item in character.get_inventory():
            print(f"- {item.get_name()}")
            self.player.get_current_room().add_item(item)
        character.inventory.clear()
