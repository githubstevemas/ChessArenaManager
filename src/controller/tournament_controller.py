import json
import os.path
from datetime import datetime

from src.view import main_view
from src.view import player_view
from src.model.tournament_model import Tournament
from src.model.player_model import Player
from src.view.report_view import Table


class TournamentController:

    def __init__(self):

        self.tournament_model = Tournament()
        self.players = Player()
        self.table_view = Table()

    def main(self):

        while True:
            main_view.main()
            main_choice = int(input("Your choice ? "))

            if main_choice == 1:
                # create tournament
                user_choice = main_view.ask_for_create()

                if user_choice == 1:
                    pass

                elif user_choice == 2:
                    self.create_random_tournament()
                    # self.generate_new_round()

            elif main_choice == 2:
                # player menu
                player_view.player_menu()
                player_menu_choice = int(input("Your choice ? "))

                if player_menu_choice == 1:
                    # create player
                    create_choice = main_view.ask_for_create()

                    if create_choice == 1:
                        # add player manualy
                        player_datas = {"id": player_view.add_player_id(), "first name": player_view.add_player_firstname(),
                                        "last name": player_view.add_player_lastname(),
                                        "birthdate": player_view.add_player_birthdate()}
                        self.players.write_player_datas(player_datas)
                        main_view.display_created(player=True)
                    elif create_choice == 2:
                        # add player randomly
                        self.players.add_players_randomly(1)
                        main_view.display_created(player=True)
                elif player_menu_choice == 2:
                    # add player to tournament
                    if os.path.exists("datas/tournaments/tournaments_datas.json"):
                        tournaments = self.tournament_model.load_tournaments_datas()
                        tournament_choice = input(player_view.choose_tournament(tournaments))
                        players = self.players.load_players_datas()
                        player_choice = input(player_view.choose_player(players))

                        """ ajouter la methode pour ajouter un joueur a un tournois donné"""

            elif main_choice == 3:
                # run tournaments
                self.run_tournament_menu()

            elif main_choice == 4:
                # print reports
                reports_choice = main_view.reports_menu()

                if reports_choice == 1:
                    if os.path.exists("datas/tournaments/players.json"):
                        datas = self.players.load_players_datas()
                        self.table_view.print_table(datas)
                    else:
                        main_view.no_players()
                    main_view.pause_display()

                elif reports_choice == 2:
                    if os.path.exists("datas/tournaments/tournaments_datas.json"):
                        datas = self.load_tournaments_datas()
                        self.table_view.print_table(datas)
                    else:
                        main_view.no_tournament()
                    main_view.pause_display()


    def create_random_tournament(self):

        self.tournament_model.create_tournament()

        # self.players.generate_pairs(self.players.players_list)

        main_view.display_created(tournament=True)

    def generate_new_round(self):

        tournaments_datas = self.load_tournaments_datas()
        self.tournament_model.write_round_datas(tournaments_datas[-1], self.players.pair_players)

    def load_tournaments_datas(self):

        with open("datas/tournaments/tournaments_datas.json", "r") as file:
            return json.load(file)

    def load_round_datas(self, tournaments_datas):

        with open(f"datas/tournaments/{tournaments_datas["tournament name"]}/round {tournaments_datas["current turn"]}.json",
                  "r") as file:
            return json.load(file)

    def run_tournament_menu(self):

        tournaments_datas = self.load_tournaments_datas()
        tournois_cours = []

        for i in tournaments_datas:
            if i["start date"] == "Non defini":
                tournois_cours.append(i)
            elif i["end date"] == "Non defini":
                tournois_cours.append(i)

        main_view.display_tournaments(tournois_cours)
        main_view.return_option()

        tournament_choice = int(input("Which tournament do you want to play ? "))

        if tournament_choice == 0:
            self.main()

        while int(tournament_choice) > len(tournaments_datas):
            tournament_choice = main_view.wrong_choice()

        current_tournament = tournois_cours[tournament_choice - 1]
        self.choose_match_to_play(current_tournament)

    def choose_match_to_play(self, current_tournament):
        """ affiche la liste des matchs non termines """

        round_datas = self.load_round_datas(current_tournament)

        nb_matchs_restants = 0
        matchs_to_play = []

        for i in range(len(round_datas)):
            if round_datas[i] == "not played":
                nb_matchs_restants += 1
                matchs_to_play.append(round_datas[i + 1])

        if nb_matchs_restants == 0:
            self.finish_round(current_tournament)

        main_view.display_matchs(current_tournament, nb_matchs_restants, matchs_to_play)
        main_view.return_option()
        match_choice = int(input("Your choice ? "))

        while int(match_choice) > len(current_tournament):
            match_choice = main_view.wrong_choice()

        if match_choice == 0:
            self.main()

        index_match = round_datas.index(matchs_to_play[match_choice - 1])
        self.add_points(current_tournament, round_datas, index_match)

    def add_points(self, current_tournament, round_datas, match_index):

        match_players = round_datas[match_index]
        main_view.add_points_view(match_players)

        winner = input("What is the number of the winning player : ")

        if int(winner) == 1:
            round_datas[match_index + 1] = 1
        elif int(winner) == 2:
            round_datas[match_index + 2] = 1

        round_datas[match_index - 1] = "over"

        if current_tournament["start date"] == "Non defini":
            old_tournaments_datas = self.load_tournaments_datas()

            for tournament in old_tournaments_datas:
                if tournament["tournament name"] == current_tournament["tournament name"]:
                    tournament["start date"] = str(datetime.now().strftime("%m/%d/%y"))

            self.tournament_model.write_tournaments_json(old_tournaments_datas)

        self.tournament_model.write_round_datas(current_tournament, round_datas)
        main_view.display_saved()

        self.choose_match_to_play(current_tournament)

    def finish_round(self, current_tournament):

        main_view.round_over(current_tournament)
        current_tournament["current turn"] += 1

        old_tournaments_datas = self.load_tournaments_datas()

        for tournament in old_tournaments_datas:
            if tournament["tournament name"] == current_tournament["tournament name"]:
                tournament["current round"] += 1

        self.tournament_model.write_tournaments_json(old_tournaments_datas)

        """players_list = self.tournament_model.load_players_datas(current_tournament["tournament name"])
        round_results = self.tournament_model.load_round_datas(current_tournament["tournament name"],
                                                               current_tournament["tour en cours"] - 1)

        self.players.generate_pairs(players_list)"""

        self.main()
