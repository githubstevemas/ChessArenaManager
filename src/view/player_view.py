
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
    print("[2] Add player to tournament\n")


def choose_tournament(tournaments):
    print("\n")
    for i in range(len(tournaments)):
        print(f"[{i + 1}] {tournaments[i]["tournament name"]}")
    print("\nChoose a tournament : ")


def choose_player(players):
    print("\n")
    for i in range(len(players)):
        print(f"[{i + 1}] {players[i]["first name"]} {players[i]["last name"]} (id {players[i]["id"]})")
    print("\nChoose a player : ")
