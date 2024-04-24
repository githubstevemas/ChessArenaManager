import json
import os
import random
import string

from datetime import datetime

from src.model.player_mdl import Player
from src.view import main_view
from src.view import player_view


class PlayerController:
    def __init__(self):
        self.players = []

    def write_player_datas(self, player):

        datas = []
        if os.path.exists("datas/tournaments/players.json"):
            datas = self.load_players_datas()
        datas.append(player)

        serialized_datas = []
        for player in datas:
            player_datas = {"id": player.id,
                            "first name": player.first_name,
                            "last name": player.last_name,
                            "birthdate": player.birthdate,
                            "inscription date": player.inscription_date}
            serialized_datas.append(player_datas)

        with open("datas/tournaments/players.json", "w") as file:
            json.dump(serialized_datas, file)

    def load_players_datas(self):

        with open("datas/tournaments/players.json", "r") as file:
            players_datas = json.load(file)

        self.players = []
        for data in players_datas:
            player = Player(data["id"],
                            data["first name"],
                            data["last name"],
                            data["birthdate"],
                            data["inscription date"])
            self.players.append(player)

        return self.players

    def create_player_manualy(self):

        player_id = player_view.add_player_id()
        first_name = player_view.add_player_firstname()
        last_name = player_view.add_player_lastname()
        birthdate = player_view.add_player_birthdate()
        inscription_date = str(datetime.now().strftime("%m/%d/%y"))

        player = Player(player_id, first_name, last_name, birthdate, inscription_date)

        self.write_player_datas(player)
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

            player_id = (random.choice(string.ascii_uppercase) +
                         random.choice(string.ascii_uppercase) +
                         str(random.randint(10000, 99999)))
            first_name = random.choice(first_name_list)
            last_name = random.choice(last_name_list)
            birthdate = f"{month_birth}/{day_birth}/{year_birth}"
            inscription_date = str(datetime.now().strftime("%m/%d/%y"))
            player = Player(player_id, first_name, last_name, birthdate, inscription_date)

            self.write_player_datas(player)
        player_view.display_created()
        main_view.pause_display()

    @staticmethod
    def non_added_players(players, tournament):

        players_non_added = []
        for player in players:
            if player.id not in tournament.players_list:
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
            player_to_add = players_non_added[int(player) - 1].id

            if tournament.players_list == "None":
                tournament.players_list = []
            tournament.players_list.append(player_to_add)

        return tournament

    def sort_players(self, tournament):

        players = tournament.rounds_list[-1]

        ids_list = []
        for match in players:
            players = match.pair_players
            scores = [match.points_player1, match.points_player2]
            ids_list.append((players[0], scores[0]))
            ids_list.append((players[1], scores[1]))

        players = self.load_players_datas()

        players_names = []

        for player in players:
            for id_player in ids_list:
                if player.id == id_player[0]:
                    player_infos = [player.first_name, player.last_name, player.id, id_player[1]]
                    players_names.append(player_infos)
        players_names.sort(key=lambda x: x[3], reverse=True)

        return players_names
