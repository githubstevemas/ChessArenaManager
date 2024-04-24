class MatchModel:

    def __init__(self, match_nb, status, pair_players, points_player1, points_player2):
        self.match_nb = match_nb
        self.status = status
        self.pair_players = pair_players
        self.points_player1 = points_player1
        self.points_player2 = points_player2

    def __str__(self):
        return f"{self.match_nb}, {self.status}, {self.pair_players}, {self.points_player1}, {self.points_player2}"
