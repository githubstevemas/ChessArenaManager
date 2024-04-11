import random
import string
import os
import json


class Tournament:

    def __init__(self):

        self.date_debut = "Non defini"
        self.date_fin = "Non defini"
        self.nb_tours = 4
        self.current_turn = 1
        self.turns_list = "Non defini"
        self.players_list = "Non defini"
        self.description = "Non defini"

    def generate_club_id(self):

        club_id = (random.choice(string.ascii_uppercase) +
                   random.choice(string.ascii_uppercase) +
                   str(random.randint(10000, 99999)))
        self.create_club_directory(club_id)

        ville = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
                               "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Francisco"])

        return club_id, ville

    def create_club_directory(self, club_id):

        dir_path = f"datas/tournaments/{club_id}"
        os.mkdir(dir_path)

    def create_tournament(self):
        # informations tournois

        club_infos = self.generate_club_id()
        club_datas = {"club id": club_infos[0],
                      "ville": club_infos[1],
                      "date de debut": self.date_debut,
                      "date de fin": self.date_fin,
                      "nombre de tours": self.nb_tours,
                      "tour en cours": self.current_turn,
                      "liste des tours": self.turns_list,
                      "liste des joueurs": self.players_list,
                      "description": self.description}

        if not os.path.exists("datas/tournaments/tournament_datas.json"):
            datas = [club_datas]
        else:
            datas = self.load_tournaments_datas()
            datas.append(club_datas)

        self.write_tournaments_json(datas)

    def load_tournaments_datas(self):
        with open("datas/tournaments/tournament_datas.json", "r") as file:
            return json.load(file)

    def write_tournaments_json(self, new_datas):

        with open("datas/tournaments/tournament_datas.json", "w") as file:
            json.dump(new_datas, file)

    def load_round_datas(self, club_id, round_nb):

        with open(f"datas/tournaments/{club_id}/Round {round_nb}.json", "r") as file:
            return json.load(file)

    def write_round_datas(self, tournament_datas, round_datas):

        tour_name = "Round " + str(tournament_datas["tour en cours"])
        path_clubs = f"datas/tournaments/{tournament_datas["club id"]}/{tour_name}.json"
        with open(path_clubs, "w") as file:
            json.dump(round_datas, file)

    def load_players_datas(self, club_id):

        path = f"datas/tournaments/{club_id}/players.json"
        with open(path, "r") as file:
            return json.load(file)

    def write_players_datas(self, club_id, datas):

        path = f"datas/tournaments/{club_id}/players.json"
        with open(path, "w") as file:
            json.dump(datas, file)
