import os


def main():
    print("TOURNAMENT MENU\n")
    print("[1] Create new tournament")
    print("[2] Run tournament")
    print("[3] View rapports\n\n")


def create_tournament():
    print("\n")
    print("[1] Give the information manually")
    print("[2] Generate random informations\n")


def wrong_choice():
    return int(input("Wrong choice, please make another one : "))


def return_option():
    print("[0] Return")


def display_created():
    print("\n")
    print("Successfully created\n")
    pause_display()


def display_saved():
    print("\n")
    print("Successfully saved\n")
    pause_display()


def pause_display():
    if os.name == 'posix':
        input("Press any key to continue...")
    else:
        print("Press any key to continue...")
        os.system("pause >nul")


def display_tournaments(tournois):
    print("\n")
    print("Tournaments :\n")
    for i in range(len(tournois)):
        if tournois[i]["date de debut"] == "Non defini":
            print(f"[{i + 1}] {tournois[i]["club id"]} not started.")
        elif tournois[i]["date de fin"] == "Non defini":
            print(f"[{i + 1}] {tournois[i]["club id"]} in progress.")
        else:
            print(f"[{i + 1}] {tournois[i]["club id"]} over.")
    print("\n")


def display_matchs(tournament_datas, nb_matchs_restants, matchs_to_play):
    """ affiche les infos du round choisi et les matchs restants """

    print("\n")
    print(f"{tournament_datas["club id"]} club, from {tournament_datas["ville"]}")
    print(f"Round number {tournament_datas["tour en cours"]} in progress, "
          f"{nb_matchs_restants} more match(s) to play.\n")
    print("Choose a match :")

    for j in range(len(matchs_to_play)):
        print(f"[{j + 1}] {matchs_to_play[j][0]} vs {matchs_to_play[j][1]}")


def add_points_view(match):
    print("\n")
    print(f"[1] {match[0]} vs [2] {match[1]}")


def round_over(current_tournament):
    print("\n")
    print(f"Round {current_tournament["tour en cours"]} from {current_tournament["club id"]} over.")
