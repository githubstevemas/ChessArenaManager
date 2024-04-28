class MatchModel:

    def __init__(self, match_nb, status, pair_players, points_player1, points_player2):
        self.match_nb = match_nb
        self.status = status
        self.pair_players = pair_players
        self.points_player1 = points_player1
        self.points_player2 = points_player2

    def __str__(self):
        return f"{self.match_nb}, {self.status}, {self.pair_players}, {self.points_player1}, {self.points_player2}"


def deserialise(match):
    match_datas = MatchModel(match["match nb"],
                             match["status"],
                             match["pair players"],
                             match["points player 1"],
                             match["points player 2"])

    return match_datas


def serialize(match):
    match_datas = {"match nb": match.match_nb,
                   "status": match.status,
                   "pair players": match.pair_players,
                   "points player 1": match.points_player1,
                   "points player 2": match.points_player2}

    return match_datas
