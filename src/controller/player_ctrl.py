import os
import json
import random
import string

from datetime import datetime

from src.model import player_mdl
from src.model.player_mdl import Player
from src.view import main_view
from src.view import player_view
from src.controller import check_inputs

DATA_PATH = "datas/tournaments/"
PLAYERS_PATH = f"{DATA_PATH}players.json"


class PlayerController:
    def __init__(self):
        self.players = []

    def write_player_datas(self, player):
        """ save players to json file """

        datas = []
        if self.check_players_json():
            datas = self.load_players_datas()
        datas.append(player)

        serialized_datas = []
        for player in datas:
            player_datas = player_mdl.serialize(player)
            serialized_datas.append(player_datas)

        with open(PLAYERS_PATH, "w") as file:
            json.dump(serialized_datas, file)

    def load_players_datas(self):
        """ load datas players from json and return players objets"""

        with open(PLAYERS_PATH, "r") as file:
            players_datas = json.load(file)

        self.players = []
        for player_datas in players_datas:
            player = player_mdl.deserialize(player_datas)
            self.players.append(player)

        return self.players

    def create_players_randomly(self, count):
        """ create randomly all datas for player creation and save it """

        for i in range(count):
            today = datetime.today()
            first_name_list = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
                               "William", "Elizabeth", "David", "Susan", "Joseph", "Jessica", "Charles", "Karen",
                               "Christopher", "Kimberly", "Matthew", "Michelle", "Brian", "Ashley", "Daniel", "Megan"]
            last_name_list = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia",
                              "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
                              "Thomas", "Taylor", "Moore", "Jackson", "White", "Harris", "Martin", "Thompson", "Lewis"]
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

    def non_added_players(self, players, tournament):
        """ check if player is already registred to the tournament, return a list of non-added players """

        players_non_added = []
        for player in players:
            if player.id not in tournament.players_list:
                players_non_added.append(player)
        return players_non_added

    def add_player_to_tournament(self, tournament):
        """ load player list, ask to add a player and return tournament datas """

        players = self.load_players_datas()
        players_non_added = self.non_added_players(players, tournament)

        if not players_non_added:
            main_view.no_player_to_add()
            return False

        players_list = []
        while True:
            player_choice = player_view.choose_player(players_non_added)
            elements = player_choice.split(',')
            valid_choice = True
            for element in elements:
                if check_inputs.digit(element.strip()):
                    if int(element) < len(players_non_added) + 1:
                        players_list.append(element)
                    else:
                        main_view.wrong_choice()
                        valid_choice = False
                        break
                else:
                    main_view.wrong_choice()
                    valid_choice = False
                    break  # Sortir de la boucle for

            if valid_choice:
                break

        for player in players_list:
            player_to_add = players_non_added[int(player) - 1].id

            if tournament.players_list == "None":
                tournament.players_list = []
            tournament.players_list.append(player_to_add)
        return tournament

    def sort_players(self, sorted_players):
        """ return list of last round players sorted by score """

        players = self.load_players_datas()

        players_names = []

        for player in players:
            for id_player in sorted_players:
                if player.id == id_player[0]:
                    player_infos = [player.first_name, player.last_name, player.id, id_player[1]]
                    players_names.append(player_infos)
        players_names.sort(key=lambda x: x[3], reverse=True)

        return players_names

    def check_players_json(self):
        """ check if there are already registered players and return boolean """

        if os.path.exists(PLAYERS_PATH):
            return True
        else:
            return False
