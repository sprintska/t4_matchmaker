from operator import itemgetter
from .QueryContext import getMatchHistory
import random


class Matchmaker:
    def __init__(self, tournament_id):

        self.tournament_id = tournament_id
        self.match_history = getMatchHistory(self.tournament_id)

        try:
            self.players = self.match_history["data"]["Tournament"][0]["Ladder"]
        except KeyError:
            self.players = False
            self.pairings = False
            return

        random.shuffle(self.players)
        self.unpaired_players = self.players

        self.pairings = []
        self.bye = None

    def generatePairings(self):

        # Fail gracefully if the tournament ladder is empty
        if not self.players:
            return False

        # Rank players to find last place for the bye
        players_ranked = sorted(
            self.players,
            key=itemgetter("tournament_points", "mov", "sos"),
            reverse=True,
        )

        self.bye = players_ranked[-1] if len(players_ranked) % 2 == 1 else None
        not self.bye or self.unpaired_players.remove(self.bye)

        # Break the equal-tp players out into lists to shuffle then re-concat them
        players_by_tp = {}

        for player in players_ranked:
            player = self.addPreviousOpponents(player)
            players_by_tp.setdefault(player["tournament_points"], []).append(player)

        players_by_tp = dict(sorted(players_by_tp.items(), reverse=True))
        self.players_in_pairing_order = []

        # Shuffle and concat
        for tp_tier in players_by_tp:
            random.shuffle(players_by_tp[tp_tier])
            self.players_in_pairing_order.extend(players_by_tp[tp_tier])

        # iterate through the micro-shuffled list and generate pairings
        for p_idx, player in enumerate(self.players_in_pairing_order):

            if player in self.unpaired_players:
                self.pairings.append(self.matchmakePlayer(player, p_idx))

    def addPreviousOpponents(self, player):

        player["previous_opponents"] = []

        matches = self.match_history["data"]["Match"]

        for match in matches:
            if player["id"] in [
                match_player["player_id"] for match_player in match["Players"]
            ]:
                for match_player in match["Players"]:
                    match_player["player_id"] == player["id"] or player[
                        "previous_opponents"
                    ].append(match_player["player_id"])

        return player

    def matchmakePlayer(self, player, player_index):
        # Recurse through the pairings order until we find the first player
        # this player hasn't played against before, then pair them.

        if (len(self.players_in_pairing_order) == player_index + 1) or (
            self.players_in_pairing_order[player_index + 1]
            not in player["previous_opponents"]
        ):
            self.unpaired_players.remove(player)
            self.unpaired_players.remove(
                self.players_in_pairing_order[player_index + 1]
            )
            return [player, self.players_in_pairing_order[player_index + 1]]
        else:
            return self.matchmakePlayer(player, player_index + 1)
