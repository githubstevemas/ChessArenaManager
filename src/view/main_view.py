import os


def main():
    print("TOURNAMENT MENU\n")
    print("[1] Create new tournament")
    print("[2] Player menu")
    print("[3] Run tournament")
    print("[4] View reports\n")
    choice = int(input("Your choice ? "))
    return choice


def ask_user_choice():
    choice = int(input("Your choice ? "))
    return choice


def reports_menu():
    print("\n")
    print("[1] Display all players")
    print("[2] Display tournaments reports")
    print("[3] Display registred players for a tournament")
    print("\n[0] Return\n")
    choice = int(input("Your choice ? "))
    return choice


def ask_for_create():
    print("\n")
    print("[1] Give informations manually")
    print("[2] Generate random informations")
    print("\n[0] Return\n")
    choice = int(input("Your choice ? "))
    return choice


def add_player_menu():
    pass


def wrong_choice():
    return int(input("Wrong choice, please make another one : "))


def display_created(tournament=False, round=False, player=False):

    print("\n")
    if tournament:
        print("Tournament successfully created.\n")
    elif round:
        print("Round successfully created.\n")
    elif player:
        print("Player successfully created.\n")
    pause_display()


def display_saved():
    print("\n")
    print("Successfully saved\n")
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
        if tournois[i]["start date"] == "None":
            print(f"[{i + 1}] {tournois[i]["tournament name"]} not started.")
        elif tournois[i]["end date"] == "None":
            print(f"[{i + 1}] {tournois[i]["tournament name"]} in progress.")
        else:
            print(f"[{i + 1}] {tournois[i]["tournament name"]} over.")


def all_tournaments_started():
    print("\n")
    print("All the tournaments are already started.\n")
    pause_display()


def ask_start():
    print("\n")
    print("Tournament not started yet, start it ?\n")
    print("[1] Yes")
    print("[2] No\n")
    print("Your choice : ")


def display_matchs(tournaments_datas, nb_matchs_restants, matchs_to_play):
    """ affiche les infos du round choisi et les matchs restants """

    print("\n")
    print(f"Round number {tournaments_datas["current round"]} in progress, "
          f"{nb_matchs_restants} more match(s) to play.\n")
    print("Choose a match :")

    for j in range(len(matchs_to_play)):
        print(f"[{j + 1}] {matchs_to_play[j][0]} vs {matchs_to_play[j][1]}")
    print("\n[0] Return\n")


def add_points_view(match):
    print("\n")
    print(f"[1] {match[0]} vs [2] {match[1]}")


def round_over(current_tournament):
    print("\n")
    print(f"Round {current_tournament["current round"]} from {current_tournament["tournament name"]} over.")


def no_players():
    print("\n")
    print("No player registred.")
    pause_display()


def no_tournament():
    print("\n")
    print("No tournament created.")
    pause_display()


def new_tournament_town():
    print("\n")
    tournament_town = input("Enter location tournament : ")
    return tournament_town.capitalize()


def new_tournament_name():
    print("\n")
    tournament_name = input("Enter tournament name : ")
    return tournament_name.capitalize()
