import random
import json
import string
import os

from datetime import datetime

from src.model.tournament_model import Tournament


class Player:
    def __init__(self):
        self.tournament_model = Tournament()
        self.players_list = []
        self.pair_players = []

    def write_player_datas(self, player_datas):

        path = "datas/tournaments/players.json"
        datas = []

        if os.path.exists(path):
            datas = self.load_players_datas()

        player_datas["inscription date"] = str(datetime.now().strftime("%m/%d/%y"))

        datas.append(player_datas)

        with open("datas/tournaments/players.json", "w") as file:
            json.dump(datas, file)

    def load_players_datas(self):
        with open("datas/tournaments/players.json", "r") as file:
            return json.load(file)

    def add_players_randomly(self, count):

        first_name_list = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William",
                           "Elizabeth", "David", "Susan", "Joseph", "Jessica", "Charles", "Karen"]

        last_name_list = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez",
                          "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas"]

        for i in range(count):

            today = datetime.today()
            year_birth = today.year - random.randint(16, 80)
            month_birth = random.randint(1, 12)
            day_birth = random.randint(1, 28)

            player_datas = {"id": (random.choice(string.ascii_uppercase) +
                                   random.choice(string.ascii_uppercase) +
                                   str(random.randint(10000, 99999))),
                            "first name": random.choice(first_name_list),
                            "last name": random.choice(last_name_list),
                            "birthdate": f"{month_birth}/{day_birth}/{year_birth}"}

            self.write_player_datas(player_datas)

    def generate_pairs(self, players_list):

        nb_pairs = len(players_list) / 2
        for i in range(int(nb_pairs)):
            pair = []
            played = "not played"
            points = 0

            for j in range(2):
                player = random.choice(players_list)
                players_list.remove(player)
                pair.extend([player["last_name"]])

            self.pair_players.extend([played, pair, points, points])
