import json
import random


class RoundController:
    def __init__(self):

        self.status = "not played"
        self.pair_players = []
        self.points_player1 = 0
        self.points_player2 = 0
        self.round_datas = []

    def write_round_datas(self, tournaments_datas, round_datas):

        tour_name = "Round " + str(tournaments_datas["current round"])
        path_clubs = f"datas/tournaments/{tournaments_datas["tournament name"]}/{tour_name}.json"
        with open(path_clubs, "w") as file:
            json.dump(round_datas, file)

    def generate_first_round(self, tournament_datas):

        nb_pairs = len(tournament_datas["players list"]) / 2
        for i in range(int(nb_pairs)):
            pair_players = []
            for j in range(2):
                player = random.choice(tournament_datas["players list"])
                tournament_datas["players list"].remove(player)
                pair_players.extend([player])

            self.round_datas.extend([self.status, pair_players, self.points_player1, self.points_player2])

        return self.round_datas

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

    def load_round_datas(self, tournament_datas):

        with open(f"datas/tournaments/"
                  f"{tournament_datas["tournament name"]}/"
                  f"Round {tournament_datas["current round"]}.json", "r") as file:
            return json.load(file)
