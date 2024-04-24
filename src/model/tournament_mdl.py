

class Tournament:

    def __init__(self, tournament_id,
                 name,
                 town,
                 start_date="Not started",
                 end_date="Not finished",
                 round_numbers=4,
                 current_round=1,
                 rounds_list="None",
                 players_list="None",
                 description="None"):

        self.tournament_id = tournament_id
        self.name = name
        self.town = town
        self.start_date = start_date
        self.end_date = end_date
        self.rounds_numbers = round_numbers
        self.current_round = current_round
        self.rounds_list = rounds_list
        self.players_list = players_list
        self.description = description
