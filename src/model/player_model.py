from datetime import datetime


class Player:
    def __init__(self):
        self.players_list = []
        self.pair_players = []

        self.id = "AB12345"
        self.first_name = ""
        self.last_name = ""
        self.birthdate = "../../...."
        self.inscription_date = str(datetime.now().strftime("%m/%d/%y"))
