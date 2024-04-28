

class Player:

    def __init__(self, player_id, first_name, last_name, birthdate, inscription_date):

        self.id = player_id
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.inscription_date = inscription_date


def deserialize(player_datas):

    player = Player(player_datas["id"],
                    player_datas["first name"],
                    player_datas["last name"],
                    player_datas["birthdate"],
                    player_datas["inscription date"])

    return player


def serialize(player):

    player_datas = {"id": player.id,
                    "first name": player.first_name,
                    "last name": player.last_name,
                    "birthdate": player.birthdate,
                    "inscription date": player.inscription_date}

    return player_datas
