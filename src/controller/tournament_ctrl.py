import os
import random
import string

from datetime import datetime

from src.model import match_mdl
from src.model import tournament_mdl
from src.model.tournament_mdl import Tournament
from src.controller import json_manager

DATAS_PATH = "datas/tournaments/"
TOURNAMENT_PATH = f"{DATAS_PATH}tournaments_datas.json"


class TournamentController:
    def __init__(self):
        self.tournaments = []
        self.matchs = []
        self.rounds = []

    def generate_tournament_name(self):
        """ return tournament name randomly generated """

        town = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
                              "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Francisco"])
        name = random.choice(["Battle arena", "Chess championship", "Tournament series", "King's conquest"])
        tournament_name = f"{town} - {name} {datetime.today().year}"

        return tournament_name, town

    def generate_tournament_id(self):
        """ return generated tournament id like AB12345 """

        while True:
            tournament_id = ("T" +
                             random.choice(string.ascii_uppercase) +
                             str(random.randint(100, 999)) +
                             str(datetime.now().year)[-2:])

            if not os.path.exists(f"{DATAS_PATH}{tournament_id}"):
                break

        return tournament_id

    def generate_tournament_datas(self):
        """ run random generation functions """

        tournament_id = self.generate_tournament_id()
        tournament_infos = self.generate_tournament_name()

        self.create_tournament(tournament_infos, tournament_id)

    def create_tournament(self, tournament_infos, tournament_id):
        """ with datas, check tournament json and save datas on it """

        tournament = Tournament(tournament_id, tournament_infos[0], tournament_infos[1])

        os.mkdir(f"{DATAS_PATH}{tournament.tournament_id}")

        if self.check_tournament_json():
            tournaments_datas = self.load_tournaments_datas()
            tournaments_datas.append(tournament)
        else:
            tournaments_datas = [tournament]

        json_manager.dump_tournaments_json(tournaments_datas)

    def non_started_tournaments(self, tournaments):
        """ return from tournament list all non-started tournaments """

        non_started_tournaments = []
        for tournament in tournaments:
            if tournament.start_date == "Not started":
                non_started_tournaments.append(tournament)

        return non_started_tournaments

    def add_date(self, current_tournament, start_date):
        """ add start date or end date to a tournament """

        old_tournaments_datas = self.load_tournaments_datas()

        if start_date:
            for tournament in old_tournaments_datas:
                if tournament.name == current_tournament.name:
                    tournament.start_date = str(datetime.now().strftime("%m/%d/%y %H:%M"))
        else:
            for tournament in old_tournaments_datas:
                if tournament.name == current_tournament.name:
                    tournament.end_date = str(datetime.now().strftime("%m/%d/%y %H:%M"))

        json_manager.dump_tournaments_json(old_tournaments_datas)

    def load_tournaments_datas(self):
        """ load tournament json and return objects for tournaments and matchs """

        serialized_datas = json_manager.load_tournaments_json()
        self.tournaments = []
        for tournament in serialized_datas:
            tournament_object = tournament_mdl.deserialize(tournament)

            if tournament_object.rounds_list != "None":
                for i, round_data in enumerate(tournament_object.rounds_list):
                    matchs = []
                    for match_data in round_data:
                        match = match_mdl.deserialise(match_data)
                        matchs.append(match)
                    tournament_object.rounds_list[i] = matchs

            self.tournaments.append(tournament_object)

        return self.tournaments

    def check_tournament_json(self):
        """ check if there are already created tournaments """

        if os.path.exists(TOURNAMENT_PATH):
            return True
        else:
            return False
