def menu():
    """This function displays the menu and returns whether the user chose to play or not.

    :return: True if the user chose to play, False otherwise."""
    while True:
        print("MENU \n1. New Game \n2. Exit")
        try:
            choice = int(input())
            if choice == 1:
                return True
            elif choice == 2:
                return False
            else:
                print("Invalid choice, please try again.")
                continue
        except ValueError:
            print("Invalid input, please pick 1 or 2.")
            continue


if __name__ == "__main__":
    play = menu()

    while play:
        print("Starting new game...")
        # Game code here

    print("Thanks for playing!")