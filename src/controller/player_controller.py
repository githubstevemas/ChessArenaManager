import json
import os
import random
import string

from datetime import datetime

from src.model.player_model import Player
from src.view import player_view


class PlayerController:
    def __init__(self):

        self.player_model = Player()

    def write_player_datas(self, player):

        path = "datas/tournaments/players.json"

        player_datas = {"id": player.id,
                        "first name": player.first_name,
                        "last name": player.last_name,
                        "birthdate": player.birthdate,
                        "inscription date": player.inscription_date}
        datas = []

        if os.path.exists(path):
            datas = self.load_players_datas()

        datas.append(player_datas)

        with open("datas/tournaments/players.json", "w") as file:
            json.dump(datas, file)

    def load_players_datas(self):
        with open("datas/tournaments/players.json", "r") as file:
            return json.load(file)

    def add_player(self):

        self.player_model.id = player_view.add_player_id()
        self.player_model.first_name = player_view.add_player_firstname()
        self.player_model.last_name = player_view.add_player_lastname()
        self.player_model.birthdate = player_view.add_player_birthdate()

        self.write_player_datas(self.player_model)
        player_view.display_created()

    def add_players_randomly(self, count):

        for i in range(count):
            today = datetime.today()

            first_name_list = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
                               "William",
                               "Elizabeth", "David", "Susan", "Joseph", "Jessica", "Charles", "Karen"]
            last_name_list = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia",
                              "Rodriguez",
                              "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas"]

            year_birth = today.year - random.randint(16, 80)
            month_birth = random.randint(1, 12)
            day_birth = random.randint(1, 28)

            self.player_model.id = (random.choice(string.ascii_uppercase) +
                                random.choice(string.ascii_uppercase) +
                                str(random.randint(10000, 99999)))
            self.player_model.first_name = random.choice(first_name_list)
            self.player_model.last_name = random.choice(last_name_list)

            self.player_model.birthdate = f"{month_birth}/{day_birth}/{year_birth}"

            self.write_player_datas(self.player_model)
        player_view.display_created()

    def check_pair_players(self, players_list):

        if len(players_list) % 2 == 0:
            pair = True
        else:
            pair = False
        return pair

    def check_nb_players(self, players_list):

        if players_list == "None":
            player_view.insufficient_players()
            player_view.pause_display()
            insufficient = True
            return insufficient

        elif len(players_list) < 2:
            player_view.insufficient_players()
            player_view.pause_display()
            insufficient = True
            return insufficient

        else:
            insufficient = False
            return insufficient

    def add_player_to_tournament(self, player_id, tournament):

        if tournament["players list"] == "None":
            tournament["players list"] = []

        tournament["players list"].append(player_id)

        return tournament
