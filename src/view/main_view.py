import os


def main():
    print("TOURNAMENT MENU\n")
    print("[1] Create new tournament")
    print("[2] Player menu")
    print("[3] Run tournament")
    print("[4] View reports")
    print("[5] Add comment to tournament\n")
    choice = input("Your choice ? ")
    return choice


def ask_user_choice():
    choice = input("Your choice ? ")
    return choice


def reports_menu():
    print("\n")
    print("[1] Display all players")
    print("[2] Display tournaments list")
    print("[3] Display tournament informations")
    print("[4] Display registred players for a tournament")
    print("[5] Display rounds informations")
    print("\n[0] Return\n")
    choice = input("Your choice ? ")
    return choice


def ask_for_create():
    print("\n")
    print("[1] Give informations manually")
    print("[2] Generate random informations")
    print("\n[0] Return\n")
    choice = input("Your choice ? ")
    return choice


def add_player_menu():
    pass


def wrong_choice():
    return int(input("Wrong choice, please make another one."))


def wrong_choice_digit():
    print("\nError, answer must be digit.")
    pause_display()


def display_tournament_created():
    print("\n")
    print("Tournament successfully created.")
    pause_display()


def display_saved():
    print("\n")
    print("Successfully saved")
    pause_display()


def pause_display():
    if os.name == 'posix':
        input("Press [Enter] to continue...")
    else:
        print("Press [Enter] to continue...")
        os.system("pause >nul")


def display_tournaments(tournois):
    print("\n")
    print("Tournaments :\n")
    for i in range(len(tournois)):
        if tournois[i]["start date"] == "Not started":
            print(f"[{i + 1}] {tournois[i]["tournament name"]}, not started.")
        elif tournois[i]["end date"] == "Not finished":
            print(f"[{i + 1}] {tournois[i]["tournament name"]}, in progress.")
        else:
            print(f"[{i + 1}] {tournois[i]["tournament name"]}, over.")
    choice = input("\nChoose a tournament : ")
    return choice


def all_tournaments_started():
    print("\n")
    print("All the tournaments are already started.")
    pause_display()


def display_matchs(tournaments_datas, matchs_to_play):
    """ affiche les infos du round choisi et les matchs restants """

    print("\n")
    print(f"Round number {tournaments_datas["current round"]}, choose a match :\n")

    for j in range(len(matchs_to_play)):
        print(f"[{j + 1}] {matchs_to_play[j][0]} vs {matchs_to_play[j][1]}")
    print("\n[0] Return\n")
    choice = input("Your choice : ")
    return choice


def add_points_view(match):
    print("\n")
    print(f"[1] {match[0]} or [2] {match[1]}\n")
    print("[0] Draw")


def round_over(current_tournament):
    print("\n")
    print(f"Round {current_tournament["current round"]} from {current_tournament["tournament name"]} over.")
    pause_display()


def no_players():
    print("\n")
    print("No player registred.")
    pause_display()


def no_tournament():
    print("\n")
    print("No tournament created yet.")
    pause_display()


def no_started_tournament():
    print("\n")
    print("No tournament started yed.")
    pause_display()


def new_tournament_town():
    print("\n")
    tournament_town = input("Enter location tournament : ")
    return tournament_town.capitalize()


def new_tournament_name():
    print("\n")
    tournament_name = input("Enter tournament name : ")
    return tournament_name.capitalize()


def display_tournament_over():
    print("\n")
    print("Tournament over. Congratulations to :")


def display_add_description():
    print("\n")
    comment = input("Type your comment here :")
    return comment
