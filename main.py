from Commands import Commands
from Item import Item
from Key import Key
from Player import Player
from NPC import NPC
from Room import Room


def menu():
    """This function displays the menu and returns whether the user chose to play or not.

    :return: True if the user chose to play, False otherwise."""
    while True:
        # Get input
        print("MENU \n1. New Game \n2. Exit")
        try:
            choice = int(input())
        except ValueError:
            print("Invalid input, please pick 1 or 2.")
            continue

        # Check input and return T/F
        if choice == 1:
            return True
        elif choice == 2:
            return False
        else:
            print("Invalid choice, please try again.")
            continue


def game(depth=0):
    """This function is the main game story."""
    # Add text for endings
    escape_ending = "You take the ladder and as you climb, you see daylight approaching. You've escaped The Cell!"
    death_ending = "You have died. Game Over."
    eternity_ending = "Your sanity slowly slips away as you find yourself back in the cell again and again and again. Game Over."

    # End game if player has been in the cell for too long
    if depth >= 5:
        print(eternity_ending)
        return

    # Create items
    lockpick = Key("Lockpick", "A small, metal lockpick.", "cell_lock")
    mystery_coin = Item("Coin", "A strange coin with an unknown symbol.")
    rusted_bar = Item("Bar", "A rusty bar that used to be part of the cell door.", 12)

    # Create rooms
    cell_room = Room("Cell", "A dark and damp cell with an iron barred door.")
    cell_room.add_item(rusted_bar)
    hallway_room = Room("Hallway", "A long hallway with flickering torches on the walls.")
    exit_room = Room("Exit", "A small, damp room with a ladder in the middle. It seems to lead to the surface.")

    cell_room.linked_rooms['N'] = hallway_room
    hallway_room.linked_rooms['S'] = cell_room
    cell_room.set_lock('N', "cell_lock")

    hallway_room.linked_rooms['E'] = exit_room
    exit_room.linked_rooms['W'] = hallway_room

    # Create NPCs
    cellmate_dialogue = {
        "response": "I bet you're wondering how you got here.",
        "options": [
            {
                "text": "Yes, actually.",
                "next_dialogue": {
                    "response": "So many have come and gone, none of us know how we got here.",
                    "options": [
                        {
                            "text": "So there's a way out then?",
                            "consequences": {
                                {
                                    "type": "reveal_item",
                                    "item": lockpick
                                },
                                {
                                    "type": "tree_resolved",
                                    "new_dialogue": "Go on, get out of here."
                                }
                            },
                            "next_dialogue": {
                                "response": "Not exactly. You'll find out soon enough. Here, take this for the door.",
                                "options": []
                            }
                        },
                        {
                            "text": "Well that sounds silly.",
                            "consequences": {
                                {
                                    "type": "reveal_item",
                                    "item": lockpick
                                },
                                {
                                    "type": "tree_resolved",
                                    "new_dialogue": "Go on, get out of here."
                                }
                            },
                            "next_dialogue": {
                                "response": "Take this and go find out for yourself.",
                                "options": []
                            }
                        }
                    ]
                }
            },
            {
                "text": "No, just tell me how to get out.",
                "consequences": {
                    {
                        "type": "reveal_item",
                        "item": lockpick
                    },
                    {
                        "type": "tree_resolved",
                        "new_dialogue": "Go on, get out of here."
                    }
                },
                "next_dialogue": {
                    "response": "Well that's not very polite, but fine. You'll find out soon enough, but take this.",
                    "options": []
                }
            }
        ]
    }
    cellmate = NPC("Cellmate", "A mysterious figure in the corner of the cell. It looks like they've been here a while.", dialogue_tree=cellmate_dialogue)
    minotaur = NPC("Minotaur", "A large, hulking beast. It looks angry.", hostile=True)

    # Add items to inventories
    cellmate.add_item(lockpick)
    minotaur.add_item(mystery_coin)

    # Add NPCs to rooms
    cell_room.add_npc(cellmate)
    hallway_room.add_npc(minotaur)

    # Create player
    player = Player("Player", "Your clothes are tattered and your hands scraped and dirty.", 100, current_room=cell_room)
    commands = Commands(player)

    # Opening text
    start_text = "You wake up in a dark cell..."

    # Start game
    print(start_text)
    commands.help()

    # Keep taking actions until user finds an ending
    while True:
        next_command = input("\n> ")
        commands.process_command(next_command)

        if player.get_current_room().get_name() == "Exit":
            if mystery_coin in player.get_inventory():
                print(escape_ending)
                break
            else:
                print("You climb the ladder and...")
                game(depth + 1)

        if player.get_health() <= 0:
            print(death_ending)
            break


if __name__ == "__main__":
    play = menu()

    while play:
        print("Starting new game...")
        game()

    print("Thanks for playing!")
