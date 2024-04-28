import os


def main():
    # [0] To enter debug menu
    print("TOURNAMENT MENU\n")
    print("[1] Create new tournament")
    print("[2] Player menu")
    print("[3] Run tournament")
    print("[4] View reports")
    print("[5] Add comment to tournament\n")
    return input("Your choice ? ")


def ask_user_choice():
    return input("Your choice ? ")


def reports_menu():
    print("\n")
    print("[1] Display all players")
    print("[2] Display tournaments list")
    print("[3] Display tournament informations")
    print("[4] Display registred players for a tournament")
    print("[5] Display rounds informations")
    print("[6] Display players rankings")
    print("\n[0] Return\n")
    return input("Your choice ? ")


def wrong_choice():
    print("Wrong choice, please make another one.\n")


def wrong_choice_digit():
    print("\nError, answer must be digit.")
    pause_display()


def wrong_choice_alpha():
    print("\nError, answer must be alpha.")
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
        if tournois[i].start_date == "Not started":
            print(f"[{i + 1}] {tournois[i].name}, not started.")
        elif tournois[i].end_date == "Not finished":
            print(f"[{i + 1}] {tournois[i].name}, in progress.")
        else:
            print(f"[{i + 1}] {tournois[i].name}, over.")
    return input("\nChoose a tournament : ")


def run_another_match():
    print("\nplay an other match ?\n")
    print("[1] Yes")
    print("[2] No\n")
    return input("Your choice : ")


def all_tournaments_started():
    print("\n")
    print("All the tournaments are already started.")
    pause_display()


def display_matchs(tournaments_datas, matchs_to_play):
    print("\n")
    print(f"Matchs from round number {tournaments_datas.current_round} :\n")
    for j in range(len(matchs_to_play)):
        print(f"[{j + 1}] {matchs_to_play[j].pair_players[0]} vs {matchs_to_play[j].pair_players[1]}")
    return input("\nChoose a match : ")


def display_round(rounds_nb):
    print("\n")
    return input(f"{rounds_nb} round(s) for this tournament, choose one to display : ")


def add_points_view(match):
    print("\n")
    print(f"[1] {match.pair_players[0]} or [2] {match.pair_players[1]}")
    print("[0] Draw\n")


def round_over(current_tournament):
    print("\n")
    print(f"Round {current_tournament.current_round} from {current_tournament.name} over.")
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
    print("No tournament started yet.")
    pause_display()


def no_player_to_add():
    print("\n")
    print("All players have already been added.")
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
    return input("Write your comment here, and press enter :")


def debug_menu():
    print("\n")
    print("Debug menu\n")
    print("[1] Create random tournament")
    print("[2] Create 16 random players")
    print("[3] Erease all datas")
    print("[0] Return\n")
    return input("Your choice : ")
