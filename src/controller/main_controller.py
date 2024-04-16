import os.path
import shutil
from datetime import datetime

from src.view import main_view
from src.view import report_view
from src.view import player_view

from src.controller.tournament_controller import TournamentController
from src.controller.round_controller import RoundController
from src.controller.player_controller import PlayerController
from src.model.round_model import Round


class Controller:

    def __init__(self):

        self.tournament_controller = TournamentController()
        self.round_controller = RoundController()
        self.player_controller = PlayerController()
        self.round = Round()

    def main_menu(self):

        while True:
            main_choice = main_view.main()

            if main_choice == 0:
                # supprimer toutes les donnees
                for element in os.listdir("datas/tournaments"):
                    path = os.path.join("datas/tournaments", element)
                    if os.path.isfile(path):
                        os.remove(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path)

            if main_choice == 1:
                self.create_tournament_menu()

            elif main_choice == 2:
                self.player_menu()

            elif main_choice == 3:
                self.run_tournament_menu()

            elif main_choice == 4:
                self.reports_menu()

    def create_tournament_menu(self):

        user_choice = main_view.ask_for_create()

        if user_choice == 1:

            town = main_view.new_tournament_town()
            name = main_view.new_tournament_name()

            tournament_name = f"{town} - {name} {datetime.today().year}"

            tournament_datas = [tournament_name, town]
            self.tournament_controller.create_tournament(tournament_datas)
            main_view.display_created(tournament=True)

        elif user_choice == 2:
            self.tournament_controller.generate_tournament_datas()
            main_view.display_created(tournament=True)

        elif user_choice == 0:
            self.main_menu()

    def player_menu(self):

        while True:
            player_menu_choice = int(input(player_view.player_menu()))

            if player_menu_choice == 1:
                # create player
                create_choice = main_view.ask_for_create()

                if create_choice == 1:
                    # add player manualy
                    self.player_controller.add_player()
                elif create_choice == 2:
                    # add player randomly
                    self.player_controller.add_players_randomly(16)

            elif player_menu_choice == 2:
                # add player to tournament
                if os.path.exists("datas/tournaments/tournaments_datas.json"):

                    tournaments = self.tournament_controller.load_tournaments_datas()

                    not_started_tournaments = []
                    for tournament in tournaments:
                        if tournament["start date"] == "None":
                            not_started_tournaments.append(tournament)

                    if not not_started_tournaments:
                        main_view.all_tournaments_started()

                    tournament_choice = int(input(player_view.choose_tournament(not_started_tournaments)))
                    tournament = not_started_tournaments[tournament_choice - 1]

                    players = self.player_controller.load_players_datas()

                    players_not_added = []

                    for player in players:
                        if player["id"] not in tournament["players list"]:
                            players_not_added.append(player)

                    player_choice = int(input(player_view.choose_player(players_not_added)))

                    player_to_add = players_not_added[player_choice - 1]["id"]
                    print(f"joueur choisi : {player_to_add}")

                    new_tournament_datas = self.player_controller.add_player_to_tournament(player_to_add, tournament)

                    tournaments[tournament_choice - 1] = new_tournament_datas
                    self.tournament_controller.write_tournaments_json(tournaments)

                    main_view.display_saved()

                else:
                    player_view.no_tournament()
                    main_view.pause_display()

            elif player_menu_choice == 0:
                self.main_menu()

    def reports_menu(self):

        while True:
            reports_choice = main_view.reports_menu()
            if reports_choice == 1:
                if os.path.exists("datas/tournaments/players.json"):
                    datas = self.player_controller.load_players_datas()
                    report_view.print_table(datas)
                else:
                    main_view.no_players()
                main_view.pause_display()

            elif reports_choice == 2:
                if os.path.exists("datas/tournaments/tournaments_datas.json"):
                    datas = self.tournament_controller.load_tournaments_datas()
                    report_view.print_table(datas)
                else:
                    main_view.no_tournament()
                main_view.pause_display()

            elif reports_choice == 3:
                tournaments_datas = self.tournament_controller.load_tournaments_datas()
                main_view.display_tournaments(tournaments_datas)
                tournament = main_view.ask_user_choice()

                players_list = self.player_controller.load_players_datas()

                list_to_display = []

                for player_id in tournaments_datas[tournament - 1]["players list"]:
                    for player_datas in players_list:
                        if player_id == player_datas["id"]:
                            list_to_display.append(player_datas)

                report_view.print_table(list_to_display)
                main_view.pause_display()

            elif reports_choice == 0:
                self.main_menu()

    def create_first_round(self, current_tournament):

        pair_list = self.player_controller.check_pair_players(current_tournament["players list"])

        if not pair_list:
            player_view.non_pair_list()
            self.main_menu()

        insufficient_players = self.player_controller.check_nb_players(current_tournament["players list"])

        if insufficient_players:
            player_view.insufficient_players()
            self.main_menu()
        else:
            pairs = self.round_controller.generate_first_round(current_tournament)
            self.round_controller.write_round_datas(current_tournament, pairs)

        self.add_start_date(current_tournament)

    def run_tournament_menu(self):

        tournaments_datas = self.tournament_controller.load_tournaments_datas()
        tournois_cours = []

        for i in tournaments_datas:
            if i["start date"] == "None":
                tournois_cours.append(i)
            elif i["end date"] == "None":
                tournois_cours.append(i)

        main_view.display_tournaments(tournois_cours)

        tournament_choice = int(input("\nWhich tournament do you want to play ? "))

        if tournament_choice == 0:
            self.main_menu()

        while int(tournament_choice) > len(tournaments_datas):
            tournament_choice = main_view.wrong_choice()

        current_tournament = tournois_cours[tournament_choice - 1]
        self.play_a_match(current_tournament)

    def play_a_match(self, current_tournament):

        """ bonus : verifier si le fichier round est cree suite a un premier match """
        if not os.path.exists(f"datas/tournaments/"
                              f"{current_tournament["tournament name"]}/"
                              "Round 1.json"):
            self.create_first_round(current_tournament)

        round_datas = self.round_controller.load_round_datas(current_tournament)

        nb_matchs_restants = 0
        matchs_to_play = []

        for i in range(len(round_datas)):
            if round_datas[i] == "not played":
                nb_matchs_restants += 1
                matchs_to_play.append(round_datas[i + 1])

        main_view.display_matchs(current_tournament, nb_matchs_restants, matchs_to_play)
        match_choice = int(input("Your choice ? "))

        while int(match_choice) > len(current_tournament):
            match_choice = main_view.wrong_choice()

        index_match = round_datas.index(matchs_to_play[match_choice - 1])
        self.add_points(current_tournament, round_datas, index_match)

        if nb_matchs_restants == 1:
            """ finish round """
            self.finish_round(current_tournament)

    def add_start_date(self, current_tournament):
        old_tournaments_datas = self.tournament_controller.load_tournaments_datas()

        for tournament in old_tournaments_datas:
            if tournament["tournament name"] == current_tournament["tournament name"]:
                tournament["start date"] = str(datetime.now().strftime("%m/%d/%y"))

        self.tournament_controller.write_tournaments_json(old_tournaments_datas)

    def add_points(self, current_tournament, round_datas, match_index):

        match_players = round_datas[match_index]
        main_view.add_points_view(match_players)

        winner = input("What is the number of the winning player : ")

        if int(winner) == 1:
            round_datas[match_index + 1] += 1
        elif int(winner) == 2:
            round_datas[match_index + 2] += 1

        round_datas[match_index - 1] = "over"

        self.round_controller.write_round_datas(current_tournament, round_datas)
        main_view.display_saved()

    def finish_round(self, current_tournament):

        main_view.round_over(current_tournament)
        main_view.pause_display()

        if current_tournament["current round"] == 4:
            self.finish_tournament(current_tournament)

        old_tournaments_datas = self.tournament_controller.load_tournaments_datas()

        # change current round
        new_tournaments_datas = self.round_controller.increment_round(current_tournament, old_tournaments_datas)
        self.tournament_controller.write_tournaments_json(new_tournaments_datas)

        # generate new json round
        round_datas = self.round_controller.load_round_datas(current_tournament)
        new_round = self.round_controller.generate_new_pairs(round_datas)

        current_tournament["current round"] += 1
        # a ameliorer

        self.round_controller.write_round_datas(current_tournament, new_round)
        self.main_menu()

    def finish_tournament(self, current_tournament):
        current_round = self.round_controller.load_round_datas(current_tournament)

        players_list = []
        i = 1
        while i < len(current_round):
            players = current_round[i]
            scores = current_round[i+1:i+3]
            players_list.extend(zip(players, scores))
            i += 4

        final_list = sorted(players_list, key=lambda x: x[1], reverse=True)
        player_view.display_winners(final_list)
        main_view.pause_display()

