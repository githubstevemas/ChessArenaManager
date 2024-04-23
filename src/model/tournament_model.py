import random
import string
from datetime import datetime


class Tournament:

    def __init__(self):

        self.start_date = "Not started"
        self.end_date = "Not finished"
        self.rounds_numbers = 4
        self.current_round = 1
        self.rounds_list = "None"
        self.players_list = "None"
        self.description = "None"

    @staticmethod
    def generate_tournament_id():
        return ("T" +
                random.choice(string.ascii_uppercase) +
                str(random.randint(100, 999)) +
                str(datetime.now().year)[-2:])
