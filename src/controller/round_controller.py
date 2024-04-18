import json
import random
import os

from src.view import main_view
from src.view import player_view
from src.controller.tournament_controller import TournamentController
from src.model.round_model import RoundModel


class RoundController:
    def __init__(self):

        self.tournament_controller = TournamentController()
        self.round_model = RoundModel()

    def write_round_datas(self, tournaments_datas, round_datas):

        tour_name = "Round " + str(tournaments_datas["current round"])
        path_clubs = f"datas/tournaments/{tournaments_datas["tournament name"]}/{tour_name}.json"
        with open(path_clubs, "w") as file:
            json.dump(round_datas, file)

    def generate_firsts_pairs(self, tournament_datas):

        pair_list = []
        nb_pairs = len(tournament_datas["players list"]) / 2
        for i in range(int(nb_pairs)):
            pair_players = []
            for j in range(2):
                player = random.choice(tournament_datas["players list"])
                tournament_datas["players list"].remove(player)
                pair_players.extend([player])

            self.round_model.round_datas.extend([self.round_model.status,
                                                 pair_players,
                                                 self.round_model.points_player1,
                                                 self.round_model.points_player2])
            pair_list.append(pair_players)

        self.write_pairs_json(pair_list, tournament_datas)

        return self.round_model.round_datas

    def increment_round(self, current_tournament, old_tournaments_datas):

        for tournament in old_tournaments_datas:
            if tournament["tournament name"] == current_tournament["tournament name"]:
                tournament["current round"] += 1

        return old_tournaments_datas

    def generate_new_pairs(self, current_round):

        new_players_list = []
        i = 1
        while i < len(current_round):
            players = current_round[i]
            scores = current_round[i+1:i+3]
            new_players_list.extend(zip(players, scores))
            i += 4
        new_players_list.sort(key=lambda x: x[1])
        round_datas = []
        for i in range(0, len(new_players_list), 2):
            round_datas.append("not played")
            round_datas.append((new_players_list[i][0], new_players_list[i + 1][0]))
            round_datas.extend([new_players_list[i][1], new_players_list[i + 1][1]])

        return round_datas

    def write_pairs_json(self, pair_list, tournament):

        path_clubs = f"datas/tournaments/{tournament["tournament name"]}/pairs.json"
        with open(path_clubs, "w") as file:
            json.dump(pair_list, file)

    def load_pairs_json(self, tournament):

        with open(f"datas/tournaments/"
                  f"{tournament["tournament name"]}/"
                  f"pairs.json", "r") as file:

            return json.load(file)

    def load_round_datas(self, tournament_datas):

        with open(f"datas/tournaments/"
                  f"{tournament_datas["tournament name"]}/"
                  f"Round {tournament_datas["current round"]}.json", "r") as file:

            return json.load(file)

    def create_first_round(self, current_tournament):

        pairs = self.generate_firsts_pairs(current_tournament)
        self.write_round_datas(current_tournament, pairs)
        self.tournament_controller.add_date(current_tournament, start_date=True)

    def check_pair_players(self, players_list):

        if len(players_list) % 2 == 0:
            pair = True
        else:
            pair = False

        return pair

    def check_nb_players(self, players_list):

        if len(players_list) < 2:
            insufficient = True

            return insufficient

        else:
            insufficient = False

            return insufficient

    def check_already_together(self, pair, tournament):

        pairs = self.load_pairs_json(tournament)
        for i in range(len(pairs)):
            pass

            """ a finir """

    def choose_match_to_play(self, current_tournament):

        if not os.path.exists(f"datas/tournaments/"
                              f"{current_tournament["tournament name"]}/"
                              "Round 1.json"):
            self.create_first_round(current_tournament)

        round_datas = self.load_round_datas(current_tournament)
        nb_matchs_restants = 0
        matchs_to_play = []
        for i in range(len(round_datas)):
            if round_datas[i] == "not played":
                nb_matchs_restants += 1
                matchs_to_play.append(round_datas[i + 1])
        match_choice = int(main_view.display_matchs(current_tournament, matchs_to_play))

        while int(match_choice) > len(current_tournament):
            match_choice = main_view.wrong_choice()
        index_match = round_datas.index(matchs_to_play[match_choice - 1])
        self.add_points(current_tournament, round_datas, index_match)

        if nb_matchs_restants == 1:
            self.finish_round(current_tournament)

    def add_points(self, current_tournament, round_datas, match_index):

        match_players = round_datas[match_index]
        main_view.add_points_view(match_players)
        winner = input("What is the number of the winning player : ")
        if int(winner) == 1:
            round_datas[match_index + 1] += 1
        elif int(winner) == 2:
            round_datas[match_index + 2] += 1
        elif int(winner) == 0:
            round_datas[match_index + 1] += 0.5
            round_datas[match_index + 2] += 0.5
        round_datas[match_index - 1] = "over"
        self.write_round_datas(current_tournament, round_datas)
        main_view.display_saved()

    def finish_round(self, current_tournament):

        main_view.round_over(current_tournament)

        if current_tournament["current round"] != 4:
            old_tournaments_datas = self.tournament_controller.load_tournaments_datas()

            # change current round
            new_tournaments_datas = self.increment_round(current_tournament, old_tournaments_datas)
            self.tournament_controller.write_tournaments_json(new_tournaments_datas)

            # generate new json round
            round_datas = self.load_round_datas(current_tournament)
            new_round = self.generate_new_pairs(round_datas)

            current_tournament["current round"] += 1
            # a ameliorer

            self.write_round_datas(current_tournament, new_round)

        else:
            self.finish_tournament(current_tournament)

    def finish_tournament(self, current_tournament):

        main_view.display_tournament_over()
        current_round = self.load_round_datas(current_tournament)
        self.tournament_controller.add_date(current_tournament, start_date=False)
        players_list = []
        i = 1
        while i < len(current_round):
            players = current_round[i]
            scores = current_round[i + 1:i + 3]
            players_list.extend(zip(players, scores))
            i += 4
        final_list = sorted(players_list, key=lambda x: x[1], reverse=True)
        player_view.display_winners(final_list)
        main_view.pause_display()
