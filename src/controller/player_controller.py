import json
import os
import random
import string

from datetime import datetime

from src.model.player_model import Player
from src.view import main_view
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

    def create_player_manualy(self):

        self.player_model.id = player_view.add_player_id()
        self.player_model.first_name = player_view.add_player_firstname()
        self.player_model.last_name = player_view.add_player_lastname()
        self.player_model.birthdate = player_view.add_player_birthdate()
        self.write_player_datas(self.player_model)
        player_view.display_created()
        main_view.pause_display()

    def create_players_randomly(self, count):

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
        main_view.pause_display()

    @staticmethod
    def non_added_players(players, tournament):

        players_non_added = []
        for player in players:
            if player["id"] not in tournament["players list"]:
                players_non_added.append(player)
        return players_non_added

    def add_player_to_tournament(self, tournament):

        players = self.load_players_datas()
        players_non_added = self.non_added_players(players, tournament)
        player_choice = player_view.choose_player(players_non_added)

        elements = player_choice.split(',')
        players_list = []
        for element in elements:
            players_list.append(element.strip())

        for player in players_list:
            player_to_add = players_non_added[int(player) - 1]["id"]

            if tournament["players list"] == "None":
                tournament["players list"] = []
            tournament["players list"].append(player_to_add)

        return tournament

    def sort_players(self, tournament):

        players = tournament["tournament list"][-1]

        ids_list = []
        for match in players:
            players = match['pairs']
            scores = [match['points player 1'], match['points player 2']]
            ids_list.append((players[0], scores[0]))
            ids_list.append((players[1], scores[1]))

        players = self.load_players_datas()

        players_names = []

        for player in players:
            for id_player in ids_list:
                if player["id"] == id_player[0]:
                    player_infos = [player["first name"], player["last name"], player["id"], id_player[1]]
                    players_names.append(player_infos)
        players_names.sort(key=lambda x: x[3], reverse=True)

        return players_names
