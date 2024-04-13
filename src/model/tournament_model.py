import random
import string
import os
import json

from datetime import datetime


class Tournament:

    def __init__(self):

        self.date_debut = "None"
        self.date_fin = "None"
        self.nb_tours = 4
        self.current_turn = 1
        self.turns_list = "None"
        self.players_list = "None"
        self.description = "None"

    def generate_tournament_name(self):

        town = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
                              "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Francisco"])
        name = random.choice(["Battle Arena", "Championship", "Tournament Series", "King's Conquest"])
        year = datetime.today().year

        tournament_name = f"{town}'s {name} {year}"
        return tournament_name, town

    def create_club_directory(self, tournament_name):

        dir_path = f"datas/tournaments/{tournament_name}"
        os.mkdir(dir_path)

    def create_tournament(self):
        # informations tournois

        club_infos = self.generate_tournament_name()

        tournaments_datas = {"tournament name": club_infos[0],
                      "town": club_infos[1],
                      "start date": self.date_debut,
                      "end date": self.date_fin,
                      "rounds numbers": self.nb_tours,
                      "current round": self.current_turn,
                      "tournaments list": self.turns_list,
                      "players list": self.players_list,
                      "description": self.description}

        os.mkdir(f"datas/tournaments/{tournaments_datas["tournament name"]}")

        if os.path.exists("datas/tournaments/tournaments_datas.json"):
            datas = self.load_tournaments_datas()
            datas.append(tournaments_datas)

        else:
            datas = [tournaments_datas]

        self.write_tournaments_json(datas)



    def load_tournaments_datas(self):


        with open("datas/tournaments/tournaments_datas.json", "r") as file:
            return json.load(file)

    def write_tournaments_json(self, new_datas):

        with open(f"datas/tournaments/tournaments_datas.json", "w") as file:
            json.dump(new_datas, file)

    def load_round_datas(self, tournament_name, round_nb):

        with open(f"datas/tournaments/{tournament_name}/Round {round_nb}.json", "r") as file:
            return json.load(file)

    def write_round_datas(self, tournaments_datas, round_datas):

        tour_name = "Round " + str(tournaments_datas["current round"])
        path_clubs = f"datas/tournaments/{tournaments_datas["tournament name"]}/{tour_name}.json"
        with open(path_clubs, "w") as file:
            json.dump(round_datas, file)
