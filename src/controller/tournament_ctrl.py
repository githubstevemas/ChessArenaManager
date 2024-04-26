import random
import os
import string
from datetime import datetime

from src.controller import json_manager
from src.model.match_mdl import MatchModel
from src.model.tournament_mdl import Tournament


class TournamentController:
    def __init__(self):
        self.tournaments = []
        self.matchs = []
        self.rounds = []

    @staticmethod
    def generate_tournament_name():
        """ return tournament name randomly generated """

        town = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
                              "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Francisco"])
        name = random.choice(["Battle arena", "Chess championship", "Tournament series", "King's conquest"])
        tournament_name = f"{town} - {name} {datetime.today().year}"
        return tournament_name, town

    @staticmethod
    def generate_tournament_id():
        """ generate tournament id like AB12345 """

        while True:
            tournament_id = ("T" +
                             random.choice(string.ascii_uppercase) +
                             str(random.randint(100, 999)) +
                             str(datetime.now().year)[-2:])

            if not os.path.exists(f"datas/tournaments/{tournament_id}"):
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

        os.mkdir(f"datas/tournaments/{tournament.tournament_id}")

        if os.path.exists("datas/tournaments/tournaments_datas.json"):
            tournaments_datas = self.load_tournaments_datas()
            tournaments_datas.append(tournament)
        else:
            tournaments_datas = [tournament]

        json_manager.dump_tournaments_json(tournaments_datas)

    @staticmethod
    def non_started_tournaments(tournaments):
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
            print("adding strat date")
            for tournament in old_tournaments_datas:
                if tournament.name == current_tournament.name:
                    tournament.start_date = str(datetime.now().strftime("%m/%d/%y %H:%M"))
        else:
            for tournament in old_tournaments_datas:
                if tournament.name == current_tournament.name:
                    tournament.end_date = str(datetime.now().strftime("%m/%d/%y %H:%M"))

        json_manager.dump_tournaments_json(old_tournaments_datas)

    def load_tournaments_datas(self):
        """ load tournament json and instantiates objects for tournaments and matchs"""

        serialized_datas = json_manager.load_tournaments_json()
        self.tournaments = []
        for tournaments in serialized_datas:
            tournament = Tournament(tournaments["id"],
                                    tournaments["name"],
                                    tournaments["town"],
                                    tournaments["start date"],
                                    tournaments["end date"],
                                    tournaments["rounds nb"],
                                    tournaments["current round"],
                                    tournaments["rounds list"],
                                    tournaments["players list"],
                                    tournaments["description"])

            if tournament.rounds_list != "None":
                for i, round_data in enumerate(tournament.rounds_list):
                    matchs = []
                    for match_data in round_data:
                        match = MatchModel(
                            match_data["match nb"],
                            match_data["status"],
                            match_data["pair players"],
                            match_data["points player 1"],
                            match_data["points player 2"]
                        )
                        matchs.append(match)
                    tournament.rounds_list[i] = matchs

            self.tournaments.append(tournament)

        return self.tournaments
