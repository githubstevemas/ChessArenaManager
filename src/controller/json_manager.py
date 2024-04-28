import json

from src.model import tournament_mdl


def dump_tournaments_json(datas):
    serialized_datas = []
    for tournament in datas:
        tournament_datas = tournament_mdl.serialize(tournament)
        serialized_datas.append(tournament_datas)

    with open("datas/tournaments/tournaments_datas.json", "w") as file:
        json.dump(serialized_datas, file)


def load_tournaments_json():

    with open("datas/tournaments/tournaments_datas.json", "r") as file:
        return json.load(file)
