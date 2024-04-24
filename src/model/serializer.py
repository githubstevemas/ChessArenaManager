
def serialize_tournaments(tournament):
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
                serialized_match = serialize_match(match)
                matchs.append(serialized_match)
            rounds.append(matchs)
        tournament_datas["rounds list"] = rounds

    return tournament_datas


def serialize_match(match):

    match_datas = {"match nb": match.match_nb,
                   "status": match.status,
                   "pair players": match.pair_players,
                   "points player 1": match.points_player1,
                   "points player 2": match.points_player2}

    return match_datas
