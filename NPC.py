import Character


class NPC(Character):
    def __init__(self, name, description, health=100, hostile=False, dialogue_tree=None):
        super().__init__(name, description, health)
        self.hostile = hostile
        self.dialogue_tree = dialogue_tree if dialogue_tree else {}

    def get_goal(self):
        return self.goal

    def is_hostile(self):
        return self.hostile

    def set_hostile(self, hostile):
        self.hostile = hostile

    def talk(self):
        # Get start of tree and print initial prompt
        current_dialogue = self.dialogue_tree
        print(current_dialogue["response"])

        # Loop through dialogue tree
        while current_dialogue:
            # Break if there are no more options
            if not current_dialogue["options"]:
                break

            # Print options
            for i, option in enumerate(current_dialogue["options"]):
                print(f"{i + 1}. {option['text']}")

            # Get user choice
            try:
                choice = int(input()) - 1
            except ValueError:
                print("Invalid choice.")
                continue

            # If choice in bounds, print response and apply consequences
            if 0 <= choice < len(current_dialogue["options"]):
                # Print response
                next_dialogue = current_dialogue["options"][choice].get("next_dialogue")
                if next_dialogue:
                    print(next_dialogue["response"])

                # Apply consequences
                consequence = current_dialogue["options"][choice].get("consequence")
                if consequence:
                    self.apply_consequence(consequence)

                # Move to next dialogue (None if not present, will break loop)
                current_dialogue = next_dialogue
            else:
                print("Invalid choice.")

    # Just a concept demo, will likely move this to game logic Class later
    def apply_consequence(self, consequence):
        if consequence["type"] == "reveal_item":
            item = consequence.get("item")
            if item:
                print(f"An item is revealed in the room: {item.get_name()}")
                self.get_current_room().add_item(item)
        elif consequence["type"] == "become_hostile":
            self.set_hostile(True)
        # Will be expanded further as story is created

    """Sample dialogue tree:
        dialogue_tree = {
            "response": "hello",
            "options": [
                {
                    "text": "where am i",
                    "next_dialogue": {
                        "response": "in this jail cell",
                        "options": [
                            {
                                "text": "how do we get out?",
                                "consequence": {
                                    "type": "reveal_item",
                                    "item": some_item  # Replace with actual item object
                                },
                                "next_dialogue": {
                                    "response": "we need the key, the jailer has it",
                                    "options": []
                                }
                            },
                            {
                                "text": "how did i get here?",
                                "next_dialogue": {
                                    "response": "nobody knows how they get here",
                                    "options": [
                                        {
                                            "text": "how long have you been here?",
                                            "next_dialogue": {
                                                "response": "too long",
                                                "options": []
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        }"""