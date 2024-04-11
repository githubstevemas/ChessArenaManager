import json
from datetime import datetime

from src.view import main_view
from src.model.tournament_model import Tournament
from src.model.player_model import Player


class TournamentController:

    def __init__(self):

        self.tournament_model = Tournament()
        self.players = Player()

    def main(self):

        while True:
            main_view.main()
            choice = int(input("Your choice ? "))

            if choice == 1:
                main_view.create_tournament()
                create_choice = int(input("Your choice ? "))

                if create_choice == 2:
                    self.create_random_tournament()
                    self.generate_new_round()

            elif choice == 2:
                self.run_tournament_menu()

            elif choice == 3:
                tournaments_datas = self.load_tournaments_datas()
                main_view.display_tournaments(tournaments_datas)
                main_view.pause_display()
                self.main()

    def create_random_tournament(self):

        self.tournament_model.create_tournament()
        tournaments_datas = self.load_tournaments_datas()
        self.players.add_players(16, tournaments_datas)
        self.players.generate_pairs(self.players.players_list)

        main_view.display_created()

    def generate_new_round(self):

        tournaments_datas = self.load_tournaments_datas()
        self.tournament_model.write_round_datas(tournaments_datas[-1], self.players.pair_players)

    def load_tournaments_datas(self):
        with open("datas/tournaments/tournament_datas.json", "r") as file:
            return json.load(file)

    def load_round_datas(self, tournament_datas):
        with open(f"datas/tournaments/{tournament_datas["club id"]}/round {tournament_datas["tour en cours"]}.json",
                  "r") as file:
            return json.load(file)

    def run_tournament_menu(self):

        tournaments_datas = self.load_tournaments_datas()
        tournois_cours = []

        for i in tournaments_datas:
            if i["date de debut"] == "Non defini":
                tournois_cours.append(i)
            elif i["date de fin"] == "Non defini":
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

        if current_tournament["date de debut"] == "Non defini":
            old_tournament_datas = self.load_tournaments_datas()

            for tournament in old_tournament_datas:
                if tournament["club id"] == current_tournament["club id"]:
                    tournament["date de debut"] = str(datetime.now().strftime("%m %d %y - %H %M"))

            self.tournament_model.write_tournaments_json(old_tournament_datas)

        self.tournament_model.write_round_datas(current_tournament, round_datas)
        main_view.display_saved()

        self.choose_match_to_play(current_tournament)

    def finish_round(self, current_tournament):

        main_view.round_over(current_tournament)
        current_tournament["tour en cours"] += 1

        old_tournament_datas = self.load_tournaments_datas()

        for tournament in old_tournament_datas:
            if tournament["club id"] == current_tournament["club id"]:
                tournament["tour en cours"] += 1

        self.tournament_model.write_tournaments_json(old_tournament_datas)

        """players_list = self.tournament_model.load_players_datas(current_tournament["club id"])
        round_results = self.tournament_model.load_round_datas(current_tournament["club id"],
                                                               current_tournament["tour en cours"] - 1)

        self.players.generate_pairs(players_list)"""

        self.main()
