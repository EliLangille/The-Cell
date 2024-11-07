def menu():
    """This function displays the menu and either continues to the game or quits the program."""
    while True:
        print("MENU \n1. New Game \n2. Exit")
        choice = input()
        if choice == 1:
            print("Entering The Cell...")
            return
        elif choice == 2:
            print("Thanks for playing!")
            exit()
        else:
            print("Invalid choice, try again.")
            continue


if __name__ == "__main__":
    while True:
        menu()

        # Game code goes here
