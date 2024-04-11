import random
from datetime import datetime

from src.model.tournament_model import Tournament


class Player:
    def __init__(self):
        self.tournament_model = Tournament()
        self.players_list = []
        self.pair_players = []

    def add_players(self, count, club_infos):

        prenoms = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William",
                   "Elizabeth", "David", "Susan", "Joseph", "Jessica", "Charles", "Karen"]
        noms_famille = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez",
                        "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas"]

        for i in range(count):
            player = {}

            prenom = random.choice(prenoms)
            prenoms.remove(prenom)

            nom = random.choice(noms_famille)
            noms_famille.remove(nom)

            aujourd_hui = datetime.today()
            annee_naissance = aujourd_hui.year - random.randint(18, 80)
            mois_naissance = random.randint(1, 12)
            jour_naissance = random.randint(1, 28)

            date_naissance = f"{annee_naissance}/{mois_naissance}/{jour_naissance}"

            pts_round1 = 0
            pts_round2 = 0
            pts_round3 = 0
            pts_round4 = 0

            player.update({"first_name": prenom,
                           "last_name": nom,
                           "birthday": date_naissance,
                           "points round 1": pts_round1,
                           "points round 2": pts_round2,
                           "points round 3": pts_round3,
                           "points round 4": pts_round4})

            self.players_list.append(player)

        self.tournament_model.write_players_datas(club_infos[-1]["club id"], self.players_list)

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
