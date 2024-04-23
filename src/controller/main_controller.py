import os.path
import shutil
from datetime import datetime

from src.view import main_view
from src.view import report_view
from src.view import player_view

from src.controller.tournament_controller import TournamentController
from src.controller.round_controller import RoundController
from src.controller.player_controller import PlayerController


class Controller:

    def __init__(self):

        self.tournament_controller = TournamentController()
        self.round_controller = RoundController()
        self.player_controller = PlayerController()

    def main_menu(self):

        while True:
            main_choice = main_view.main()

            if main_choice == "1":
                self.create_tournament_menu()
            elif main_choice == "2":
                self.player_menu()
            elif main_choice == "3":
                self.tournament_menu()
            elif main_choice == "4":
                self.reports_menu()
            elif main_choice == "5":
                self.add_comment_menu()
            elif main_choice == "0":
                self.debug_menu()
            elif main_choice == "9":
                tournament = self.tournament_controller.load_tournaments_datas()
                self.round_controller.generate_new_pairs(tournament[0]["tournament list"])

    def create_tournament_menu(self):

        town = main_view.new_tournament_town()
        name = main_view.new_tournament_name()

        tournament_name = f"{town} - {name} {datetime.today().year}"

        tournament_datas = [tournament_name, town]
        tournament_id = self.tournament_controller.generate_tournament_id()
        self.tournament_controller.create_tournament(tournament_datas, tournament_id)
        main_view.display_tournament_created()

    def player_menu(self):

        while True:
            player_menu_choice = player_view.player_menu()

            if player_menu_choice == "1":
                self.player_controller.create_player_manualy()
            elif player_menu_choice == "2":
                self.add_player_menu()
            elif player_menu_choice == "0":
                self.main_menu()

    def add_player_menu(self):

        # add player to tournament
        if not os.path.exists("datas/tournaments/tournaments_datas.json"):
            player_view.no_tournament()
            self.main_menu()

        if not os.path.exists("datas/tournaments/players.json"):
            main_view.no_players()
            self.main_menu()

        # display non started tournaments
        tournaments = self.tournament_controller.load_tournaments_datas()
        non_started_tournaments = self.tournament_controller.non_started_tournaments(tournaments)

        if not non_started_tournaments:
            main_view.all_tournaments_started()

        tournament_choice = int(player_view.choose_tournament(non_started_tournaments))
        tournament = non_started_tournaments[tournament_choice - 1]

        new_tournament_datas = self.player_controller.add_player_to_tournament(tournament)

        tournaments[tournament_choice - 1] = new_tournament_datas
        self.tournament_controller.write_tournaments_json(tournaments)
        main_view.display_saved()
        # display players non-added to choosen tournament

    def tournament_menu(self):

        tournaments_datas = self.tournament_controller.load_tournaments_datas()
        tournois_cours = []

        # choose tournament
        for i in tournaments_datas:
            if i["end date"] == "Not finished":
                tournois_cours.append(i)
        tournament_choice = int(main_view.display_tournaments(tournois_cours))

        if tournament_choice == 0:
            self.main_menu()

        while int(tournament_choice) > len(tournaments_datas):
            tournament_choice = main_view.wrong_choice()

        current_tournament = tournois_cours[tournament_choice - 1]

        # check players nb and if pairs
        insufficient_players = self.round_controller.check_nb_players(current_tournament["players list"])
        if insufficient_players:
            player_view.insufficient_players()
            main_view.pause_display()
            self.main_menu()
        pair_list = self.round_controller.check_pair_players(current_tournament["players list"])
        if not pair_list:
            player_view.non_pair_list()
            main_view.pause_display()
            self.main_menu()

        if current_tournament["tournament list"] == "None":
            current_tournament = self.round_controller.create_first_round(current_tournament)

        self.round_controller.choose_match_to_play(current_tournament)

        while True:
            print("\nplay an other match ?\n")
            print("[1] Yes")
            print("[2] No\n")
            choice = input("Your choice : ")
            if choice == "1":
                self.round_controller.choose_match_to_play(current_tournament)
            elif choice == "2":
                break

    def reports_menu(self):

        while True:
            reports_choice = main_view.reports_menu()
            if reports_choice == "1":
                self.report_players()
            elif reports_choice == "2":
                self.report_tournament_list()
            elif reports_choice == "3":
                self.report_tournament_infos()
            elif reports_choice == "4":
                self.report_players_tournament()
            elif reports_choice == "5":
                self.report_round_infos()
            elif reports_choice == "6":
                self.report_players_ranking()
            elif reports_choice == "0":
                self.main_menu()

    def report_players(self):

        if not os.path.exists("datas/tournaments/players.json"):
            main_view.no_players()
            self.reports_menu()

        datas = self.player_controller.load_players_datas()
        sorted_players = sorted(datas, key=lambda x: x["last name"])
        player_list = []
        for player in sorted_players:
            player_datas = {"last name": f"{player["last name"]}",
                            "first name": f"{player["first name"]}",
                            "id": f"{player["id"]}"}
            player_list.append(player_datas)
        report_view.print_table(player_list)
        main_view.pause_display()

    def report_tournament_list(self):

        if not os.path.exists("datas/tournaments/tournaments_datas.json"):
            main_view.no_tournament()
            self.reports_menu()

        datas = self.tournament_controller.load_tournaments_datas()
        tournament_list = []
        for tournament in datas:
            tournament_datas = {"tournament name": f"{tournament["tournament name"]}",
                                "tournament id": f"{tournament["tournament id"]}"}
            tournament_list.append(tournament_datas)

        report_view.print_table(tournament_list)
        main_view.pause_display()

    def report_tournament_infos(self):

        if not os.path.exists("datas/tournaments/tournaments_datas.json"):
            main_view.no_tournament()
            self.reports_menu()

        tournaments = self.tournament_controller.load_tournaments_datas()
        tournament_choice = main_view.display_tournaments(tournaments)
        tournament = tournaments[int(tournament_choice) - 1]
        tournament_datas = [{"tournament name": f"{tournament["tournament name"]}",
                             "start date": f"{tournament["start date"]}",
                             "end date": f"{tournament["end date"]}",
                             "current round": f"{tournament["current round"]}",
                             "description": f"{tournament["description"]}"}]

        report_view.print_table(tournament_datas)
        main_view.pause_display()

    def report_players_tournament(self):

        if not os.path.exists("datas/tournaments/players.json"):
            main_view.no_players()
            self.reports_menu()

        tournaments_datas = self.tournament_controller.load_tournaments_datas()
        tournament = main_view.display_tournaments(tournaments_datas)
        players_list = self.player_controller.load_players_datas()
        list_to_display = []

        for player_id in tournaments_datas[int(tournament) - 1]["players list"]:
            for player_datas in players_list:
                if player_id == player_datas["id"]:
                    list_to_display.append(player_datas)

        sorted_players = sorted(list_to_display, key=lambda x: x["last name"])
        sorted_list = []
        for player in sorted_players:
            player_datas = {"last name": f"{player["last name"]}",
                            "first name": f"{player["first name"]}",
                            "id": f"{player["id"]}"}
            sorted_list.append(player_datas)

        report_view.print_table(sorted_list)
        main_view.pause_display()

    def report_round_infos(self):

        if not os.path.exists("datas/tournaments/tournaments_datas.json"):
            main_view.no_tournament()
            self.reports_menu()

        tournaments = self.tournament_controller.load_tournaments_datas()
        started_tournaments = []
        for tournament in tournaments:
            if tournament["start date"] != "Not started":
                started_tournaments.append(tournament)
        if not started_tournaments:
            main_view.no_started_tournament()
            self.reports_menu()

        tournament_choice = main_view.display_tournaments(started_tournaments)
        tournament = started_tournaments[int(tournament_choice) - 1]

        report_view.print_rounds(tournament)
        main_view.pause_display()

    def report_players_ranking(self):

        if not os.path.exists("datas/tournaments/tournaments_datas.json"):
            main_view.no_tournament()
            self.reports_menu()

        tournaments = self.tournament_controller.load_tournaments_datas()
        started_tournaments = []
        for tournament in tournaments:
            if tournament["start date"] != "Not started":
                started_tournaments.append(tournament)
        if not started_tournaments:
            main_view.no_started_tournament()
            self.reports_menu()

        tournament_choice = main_view.display_tournaments(started_tournaments)
        tournament = started_tournaments[int(tournament_choice) - 1]

        players_names = self.player_controller.sort_players(tournament)

        report_view.print_players(players_names)
        main_view.pause_display()

    def add_comment_menu(self):

        if not os.path.exists("datas/tournaments/tournaments_datas.json"):
            main_view.no_tournament()
            self.reports_menu()

        tournaments = self.tournament_controller.load_tournaments_datas()
        tournament_choice = main_view.display_tournaments(tournaments)
        tournament = tournaments[int(tournament_choice) - 1]
        description = main_view.display_add_description()

        """ formater le texte pour json """

        for i in range(len(tournaments)):
            if tournaments[i]["tournament name"] == tournament["tournament name"]:
                tournaments[i]["description"] = description

        self.tournament_controller.write_tournaments_json(tournaments)

    def debug_menu(self):

        while True:
            debug_choice = main_view.debug_menu()

            if debug_choice == "1":
                self.tournament_controller.generate_tournament_datas()
                main_view.display_tournament_created()
            if debug_choice == "2":
                self.player_controller.create_players_randomly(16)
                player_view.display_created()
            if debug_choice == "3":
                for element in os.listdir("datas/tournaments"):
                    path = os.path.join("datas/tournaments", element)
                    if os.path.isfile(path):
                        os.remove(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
            if debug_choice == "0":
                self.main_menu()
