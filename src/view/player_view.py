import os


def add_player_id():
    player_id = input("National ID (ex : AB12345) ? ")
    return player_id.upper()


def add_player_firstname():
    firs_name = input("Player first name ? ")
    return firs_name.capitalize()


def add_player_lastname():
    last_name = input("Player last name ? ")
    return last_name.capitalize()


def add_player_birthdate():
    numbers = input("Player birthdate (ex : mmddyyyy) ? ")
    return numbers[0:2] + "/" + numbers[2:4] + "/" + numbers[4:8]


def player_menu():
    print("\n")
    print("[1] Create player")
    print("[2] Add player to tournament")
    print("\n[0] Return\n")
    choice = input("Your choice ? ")
    return choice


def choose_tournament(tournaments):
    print("\n")
    for i in range(len(tournaments)):

        print(f"[{i + 1}] {tournaments[i]["tournament name"]}")
    print("\nChoose a tournament :")


def choose_different_tournament():
    print("\n")
    print("This tournament is already stared.")


def ask_more():
    print("\n")
    print("Add more players to this tournaments ?.")
    print("[1] Yes")
    print("[2] No")
    choice = input("Your choice : ")
    return choice


def choose_player(players):
    print("\n")
    for i in range(len(players)):
        print(f"[{i + 1}] {players[i]["first name"]} {players[i]["last name"]} (id {players[i]["id"]})")
    print("\nChoose a player : ")


def non_pair_list():
    print("\n")
    print("The number of registered players for this tournament must be pair.")


def no_tournament():
    print("\n")
    print("No tournament are created.")


def insufficient_players():
    print("\n")
    print("Insufficient players in tournament, you must add more players.")


def display_created():
    print("\n")
    print("Player successfully created.\n")


def pause_display():
    if os.name == 'posix':
        input("Press [Enter] to continue...")
    else:
        print("Press [Enter] to continue...")
        os.system("pause >nul")


def display_winners(players_list):
    print("\n")
    print(f"{players_list[0][0]}, first place with {players_list[0][1]} points.")
    print(f"{players_list[1][0]}, second place with {players_list[1][1]} points.")
