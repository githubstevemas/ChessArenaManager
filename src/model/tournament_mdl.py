from src.model import match_mdl


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


def deserialize(tournament):
    tournament_datas = Tournament(tournament["id"],
                                  tournament["name"],
                                  tournament["town"],
                                  tournament["start date"],
                                  tournament["end date"],
                                  tournament["rounds nb"],
                                  tournament["current round"],
                                  tournament["rounds list"],
                                  tournament["players list"],
                                  tournament["description"])
    return tournament_datas


def serialize(tournament):
    tournament_datas = {"id": tournament.tournament_id,
                        "name": tournament.name,
                        "town": tournament.town,
                        "start date": tournament.start_date,
                        "end date": tournament.end_date,
                        "rounds nb": tournament.rounds_numbers,
                        "current round": tournament.current_round,
                        "rounds list": tournament.rounds_list,
                        "players list": tournament.players_list,
                        "description": tournament.description}

    if tournament_datas["rounds list"] != "None":
        rounds = []
        for round_datas in tournament_datas["rounds list"]:
            matchs = []
            for match in round_datas:
                serialized_match = match_mdl.serialize(match)
                matchs.append(serialized_match)
            rounds.append(matchs)
        tournament_datas["rounds list"] = rounds

    return tournament_datas
