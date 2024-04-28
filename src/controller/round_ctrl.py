import random

from src.model.match_mdl import MatchModel
from src.view import main_view
from src.view import player_view
from src.controller import check_inputs
from src.controller import json_manager
from src.controller.player_ctrl import PlayerController
from src.controller.tournament_ctrl import TournamentController


class RoundController:
    def __init__(self):

        self.tournament_ctrl = TournamentController()
        self.player_ctrl = PlayerController()
        self.rounds = []

    def write_round_datas(self, tournament_datas, round_datas):
        """ change tournament rounds list for a tournament, run json save and return tournament datas """

        tournaments = self.tournament_ctrl.load_tournaments_datas()

        for i in range(len(tournaments)):
            if tournaments[i].name == tournament_datas.name:
                tournaments[i].rounds_list = round_datas

        json_manager.dump_tournaments_json(tournaments)

        return tournaments

    def generate_firsts_pairs(self, tournament_datas):
        """ return first round object with registred players """

        nb_pairs = len(tournament_datas.players_list) / 2
        round_list = []
        for i in range(int(nb_pairs)):
            pair = []
            for j in range(2):
                player = random.choice(tournament_datas.players_list)
                tournament_datas.players_list.remove(player)
                pair.extend([player])
            match = MatchModel(i + 1, "not played", pair, 0, 0)

            round_list.append(match)
        return round_list

    def increment_round(self, current_tournament, old_tournaments_datas):
        """ increment current round number and return tournament datas """

        for tournament in old_tournaments_datas:
            if tournament.name == current_tournament.name:
                tournament.current_round += 1

        return old_tournaments_datas

    def generate_new_pairs(self, rounds):
        """ with the round data, sorts the players by score,
        makes pairs with them, makes pairs with the remaining players
        and checks if the new pairs have not already been created.
        Finaly, return new round """

        sorted_list = self.sort_players(rounds)

        # sort players in dict
        players_by_score = {}
        for player, score in sorted_list:
            if score not in players_by_score:
                players_by_score[score] = []
            players_by_score[score].append(player)

        pairs_ok = False
        while not pairs_ok:

            pairs = []
            remaining_players = []
            for score, liste_joueurs in players_by_score.items():
                random.shuffle(liste_joueurs)
                nb_joueurs = len(liste_joueurs)
                for i in range(0, nb_joueurs, 2):
                    if i + 1 < nb_joueurs:
                        pairs.append((liste_joueurs[i], liste_joueurs[i + 1]))
                if nb_joueurs % 2 != 0:
                    remaining_players.append(liste_joueurs[-1])

            if remaining_players:
                for j in range(0, len(remaining_players), 2):
                    remaining_pair = (remaining_players[j], remaining_players[j + 1])
                    pairs.append(remaining_pair)

            pairs_ok = self.check_already_together(rounds, pairs)

            if pairs_ok:
                new_list = self.reattribute_points(sorted_list, pairs)
                new_round = self.create_new_round(new_list)
                rounds.append(new_round)

        return rounds

    def sort_players(self, rounds):
        """ with rounds datas sort players by score and return players list """

        sorted_list = []
        for match in rounds[-1]:
            players = match.pair_players
            scores = [match.points_player1, match.points_player2]
            sorted_list.append((players[0], scores[0]))
            sorted_list.append((players[1], scores[1]))

        return sorted_list

    def reattribute_points(self, players_list, pairs):
        """ reattribute players points to the new created pairs """

        players_dict = dict(players_list)
        new_list = []

        for pair in pairs:
            player1, player2 = pair
            score1 = players_dict[player1]
            score2 = players_dict[player2]
            new_list.append([pair, score1, score2])

        return new_list

    def create_new_round(self, pairs):
        """ with pair players create new round and return matchs objects list """

        nb_pairs = len(pairs)
        matchs_datas = []

        for i in range(int(nb_pairs)):
            match = MatchModel(i + 1, "not played", pairs[i][0], pairs[i][1], pairs[i][2])
            matchs_datas.append(match)

        return matchs_datas

    def check_already_together(self, rounds, new_pairs):
        """ with new pairs check in rounds if pairs already exists and return boolean """

        print("checking for new pairs")
        old_pairs = []
        for matches in rounds:
            for pair in matches:
                old_pairs.append(frozenset(pair.pair_players))

        old_pairs_set = set(old_pairs)
        new_pairs_set = {frozenset(pair) for pair in new_pairs}

        for new_pair_set in new_pairs_set:
            if new_pair_set in old_pairs_set:
                return False

        return True

    def create_first_round(self, current_tournament):
        """ run generating functions to create the first round of tournament """

        round1 = self.generate_firsts_pairs(current_tournament)
        self.rounds.append(round1)
        tournaments_datas = self.write_round_datas(current_tournament, [round1])
        self.tournament_ctrl.add_date(current_tournament, start_date=True)

        # return current tournament with new datas
        for i in range(len(tournaments_datas)):
            if current_tournament.tournament_id == tournaments_datas[i].tournament_id:
                return tournaments_datas[i]

    def check_pair_players(self, players_list):
        """ with registred players attribute check if players nb is pair and return boolean """

        if len(players_list) % 2 == 0:
            return True
        else:
            player_view.non_pair_list()
            main_view.pause_display()
            return False

    def check_nb_players(self, players_list):
        """ with registred players attribute check if < 16, return boolean """

        if players_list == "None" or len(players_list) < 16:
            player_view.insufficient_players()
            main_view.pause_display()
            return False
        else:
            return True

    def choose_match_to_play(self, current_tournament):
        """ for a tournament display non-played matchs and ask to play one """

        nb_matchs_restants = 0
        matchs_to_play = []

        for match in current_tournament.rounds_list[-1]:
            if match.status == "not played":
                nb_matchs_restants += 1
                matchs_to_play.append(match)

        while True:
            match_choice = main_view.display_matchs(current_tournament, matchs_to_play)

            if check_inputs.digit(match_choice):
                if int(match_choice) > len(matchs_to_play):
                    main_view.wrong_choice()
                else:
                    break
            else:
                main_view.wrong_choice_digit()

        index_match = matchs_to_play[int(match_choice) - 1].match_nb

        self.add_points(current_tournament, current_tournament.rounds_list[-1], index_match)

        if nb_matchs_restants == 1:
            self.finish_round(current_tournament)

    def add_points(self, current_tournament, round_datas, index_match):
        """ for a match il a tournament round, ask who winns, add point(s) and go save round datas """

        for match in round_datas:
            if match.match_nb == index_match:
                main_view.add_points_view(match)

                while True:
                    winner = input("What is the number of the winning player : ")

                    if check_inputs.digit(winner) and int(winner) < 3:
                        if int(winner) == 1:
                            match.points_player1 += 1
                        elif int(winner) == 2:
                            match.points_player2 += 1
                        elif int(winner) == 0:
                            match.points_player1 += 0.5
                            match.points_player2 += 0.5
                        match.status = "over"
                        break
                    else:
                        main_view.wrong_choice()

        self.write_round_datas(current_tournament, [round_datas])
        main_view.display_saved()

    def finish_round(self, current_tournament):
        """ display round over and if current round not last increment round nb, go generate a new one and save it """

        main_view.round_over(current_tournament)

        if current_tournament.current_round != 4:
            old_tournaments_datas = self.tournament_ctrl.load_tournaments_datas()

            # change current round
            new_tournaments_datas = self.increment_round(current_tournament, old_tournaments_datas)
            json_manager.dump_tournaments_json(new_tournaments_datas)

            new_rounds = self.generate_new_pairs(current_tournament.rounds_list)

            current_tournament.current_round += 1
            self.write_round_datas(current_tournament, new_rounds)

        else:
            self.finish_tournament(current_tournament)

    def finish_tournament(self, current_tournament):
        """ display tournament over, add end date and display sorted winners """

        main_view.display_tournament_over()
        self.tournament_ctrl.add_date(current_tournament, start_date=False)

        final_list = self.sort_players(current_tournament.rounds_list[-1])
        player_view.display_winners(final_list)
        main_view.pause_display()
