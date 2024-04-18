import json
import random
import os
from datetime import datetime

from src.model.tournament_model import Tournament


class TournamentController:
    def __init__(self):
        self.tournament_model = Tournament()

    def generate_tournament_name(self):

        town = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
                              "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Francisco"])
        name = random.choice(["Battle arena", "Chess championship", "Tournament series", "King's conquest"])
        tournament_name = f"{town} - {name} {datetime.today().year}"
        return tournament_name, town

    def create_tournament_directory(self, tournament_name):

        dir_path = f"datas/tournaments/{tournament_name}"
        os.mkdir(dir_path)

    def generate_tournament_datas(self):

        tournament_infos = self.generate_tournament_name()
        # check si nom deja existant
        if os.path.exists(f"datas/tournaments/{tournament_infos[0]}"):
            tournament_infos = self.generate_tournament_name()
        self.create_tournament(tournament_infos)

    def create_tournament(self, tournament_infos):

        tournaments_datas = {"tournament name": tournament_infos[0],
                             "town": tournament_infos[1],
                             "start date": self.tournament_model.date_debut,
                             "end date": self.tournament_model.date_fin,
                             "rounds numbers": self.tournament_model.nb_tours,
                             "current round": self.tournament_model.current_round,
                             "tournaments list": self.tournament_model.turns_list,
                             "players list": self.tournament_model.players_list,
                             "description": self.tournament_model.description}

        os.mkdir(f"datas/tournaments/{tournaments_datas["tournament name"]}")

        if os.path.exists("datas/tournaments/tournaments_datas.json"):
            datas = self.load_tournaments_datas()
            datas.append(tournaments_datas)
        else:
            datas = [tournaments_datas]
        self.write_tournaments_json(datas)

    def non_started_tournaments(self, tournaments):

        non_started_tournaments = []
        for tournament in tournaments:
            if tournament["start date"] == "Not started":
                non_started_tournaments.append(tournament)
        return non_started_tournaments

    def load_tournaments_datas(self):

        with open("datas/tournaments/tournaments_datas.json", "r") as file:
            return json.load(file)

    def write_tournaments_json(self, datas):

        with open("datas/tournaments/tournaments_datas.json", "w") as file:
            json.dump(datas, file)

    def add_date(self, current_tournament, start_date):

        old_tournaments_datas = self.load_tournaments_datas()

        if start_date:
            for tournament in old_tournaments_datas:
                if tournament["tournament name"] == current_tournament["tournament name"]:
                    tournament["start date"] = str(datetime.now().strftime("%m/%d/%y %H:%M"))
        else:
            for tournament in old_tournaments_datas:
                if tournament["tournament name"] == current_tournament["tournament name"]:
                    tournament["end date"] = str(datetime.now().strftime("%m/%d/%y %H:%M"))

        self.write_tournaments_json(old_tournaments_datas)
