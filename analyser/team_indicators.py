import pandas as pd
import numpy as np
from dao.game_dao import GameDAO


def get_average_opp_rank_by_map(team_last_10_games, team_id):
    d = {}
    for game in team_last_10_games:
        for map_item in game.maps:
            if game.id_team1 == team_id:
                if d.get(map_item.map_name) is None:
                    t = {map_item.map_name: {"OppRankSum": game.team2_rank, "count": 1, "average": 0.0}}
                    d.update(t)
                else:
                    d[map_item.map_name]["OppRankSum"] = d[map_item.map_name]["OppRankSum"] + game.team2_rank
                    d[map_item.map_name]["count"] = d[map_item.map_name]["count"] + 1
            else:
                if d.get(map_item.map_name) is None:
                    t = {map_item.map_name: {"OppRankSum": game.team1_rank, "count": 1, "average": 0.0}}
                    d.update(t)
                else:
                    d[map_item.map_name]["OppRankSum"] = d[map_item.map_name]["OppRankSum"] + game.team1_rank
                    d[map_item.map_name]["count"] = d[map_item.map_name]["count"] + 1
    for item in d:
        d[item]["average"] = d[item]["OppRankSum"] / d[item]["count"]
    return d


def get_plus_minos_rounds_team(games, team_id):
    d = {"Mirage": {"plusMinosRounds": 0.0}, "Dust2": {"plusMinosRounds": 0.0}, "Nuke": {"plusMinosRounds": 0.0},
         "Overpass": {"plusMinosRounds": 0.0}, "Inferno": {"plusMinosRounds": 0.0},
         "Vertigo": {"plusMinosRounds": 0.0}, "Train": {"plusMinosRounds": 0.0}, "Cache": {"plusMinosRounds": 0.0}}
    for game in games:
        for map_item in game.maps:
            if game.id_team1 == team_id:
                if d.get(map_item.map_name) is None:
                    t = {map_item.map_name: {
                        "plusMinosRounds": map_item.team1_total_rounds - map_item.team2_total_rounds}}
                    d.update(t)
                else:
                    d[map_item.map_name]["plusMinosRounds"] = d[map_item.map_name]["plusMinosRounds"] + \
                                                              map_item.team1_total_rounds - map_item.team2_total_rounds
            else:
                if d.get(map_item.map_name) is None:
                    t = {map_item.map_name: {
                        "plusMinosRounds": map_item.team2_total_rounds - map_item.team1_total_rounds}}
                    d.update(t)
                else:
                    d[map_item.map_name]["plusMinosRounds"] = d[map_item.map_name]["plusMinosRounds"] + \
                                                              map_item.team2_total_rounds - map_item.team1_total_rounds
    return d


def get_plus_minos_players_team(games):
    d = {"Mirage": {"plusMinosPlayers": 0.0}, "Dust2": {"plusMinosPlayers": 0.0}, "Nuke": {"plusMinosPlayers": 0.0},
         "Overpass": {"plusMinosPlayers": 0.0}, "Inferno": {"plusMinosPlayers": 0.0},
         "Vertigo": {"plusMinosPlayers": 0.0}, "Train": {"plusMinosPlayers": 0.0}, "Cache": {"plusMinosPlayers": 0.0}}
    for game in games:
        for map_item in game.maps:
            for playerStats in map_item.player_map_stats:
                if d.get(map_item.map_name) is None:
                    t = {map_item.map_name: {"plusMinosPlayers": 0}}
                    d.update(t)
                else:
                    d[map_item.map_name]["plusMinosPlayers"] = d[map_item.map_name][
                                                                   "plusMinosPlayers"] + playerStats.plus_minos

    return d


def get_team_confidence(team_games, team_id):
    d = {"Mirage": {"Pick": 0, "Win": 0, "Confidence": 0.0}, "Dust2": {"Pick": 0, "Win": 0, "Confidence": 0.0},
         "Nuke": {"Pick": 0, "Win": 0, "Confidence": 0.0}, "Overpass": {"Pick": 0, "Win": 0, "Confidence": 0.0},
         "Inferno": {"Pick": 0, "Win": 0, "Confidence": 0.0},"Vertigo": {"Pick": 0, "Win": 0, "Confidence": 0.0},
         "Train": {"Pick": 0, "Win": 0, "Confidence": 0.0},"Cache": {"Pick": 0, "Win": 0, "Confidence": 0.0}}
    for game in team_games:
        if game.team1.id_team == team_id:
            for map in game.maps:
                if map.map_name == game.team1_picks_maps:
                    if d.get(map.map_name) is None:
                        d2 = {map.map_name: {"Pick": 1, "Win": 0, "Confidence": 0.0}}
                        if map.team1_total_rounds > map.team2_total_rounds:
                            d2[map.map_name]["Win"] = 1
                        else:
                            d2[map.map_name]["Win"] = 0
                        d.update(d2)
                    else:
                        d[map.map_name]["Pick"] = d[map.map_name]["Pick"] + 1
                        if map.team1_total_rounds > map.team2_total_rounds:
                            d[map.map_name]["Win"] = d[map.map_name]["Win"] + 1
        elif game.team2.id_team == team_id:
            for map in game.maps:
                if map.map_name == game.team2_picks_maps:
                    if d.get(map.map_name) is None:
                        d2 = {map.map_name: {"Pick": 1, "Win": 0, "Confidence": 0.0}}
                        if map.team2_total_rounds > map.team1_total_rounds:
                            d2[map.map_name]["Win"] = 1
                        else:
                            d2[map.map_name]["Win"] = 0
                        d.update(d2)
                    else:
                        d[map.map_name]["Pick"] = d[map.map_name]["Pick"] + 1
                        if map.team2_total_rounds > map.team1_total_rounds:
                            d[map.map_name]["Win"] = d[map.map_name]["Win"] + 1
    for item in d:
        d[item]["Confidence"] = 100 * d[item]["Win"] / d[item]["Pick"] if d[item]["Pick"] != 0 else 0.0

    return d


class TeamIndicators:
    def __init(self):
        pass

    def win_lost_number_maps_by_rank_window(self, team1, team1games):
        d = {"<Top10": {}, "Top10-Top30": {}, "Top30-Top60": {}, "Top60-Top90": {}, ">Top90": {}}

        for game in team1games:
            if game.team1.name == team1:
                if game.team2_rank < 10:
                    d = self.update_dictionary_by_rank_window_and_number_of_maps(d, "<Top10", game.team1_score,
                                                                                 game.team2_score)
                elif 10 <= game.team2_rank < 30:
                    d = self.update_dictionary_by_rank_window_and_number_of_maps(d, "Top10-Top30", game.team1_score,
                                                                                 game.team2_score)
                elif 30 <= game.team2_rank < 60:
                    d = self.update_dictionary_by_rank_window_and_number_of_maps(d, "Top30-Top60", game.team1_score,
                                                                                 game.team2_score)
                elif 60 <= game.team2_rank < 90:
                    d = self.update_dictionary_by_rank_window_and_number_of_maps(d, "Top60-Top90", game.team1_score,
                                                                                 game.team2_score)
                else:
                    d = self.update_dictionary_by_rank_window_and_number_of_maps(d, ">Top90", game.team1_score,
                                                                                 game.team2_score)
            else:
                if game.team1_rank < 10:
                    d = self.update_dictionary_by_rank_window_and_number_of_maps(d, "<Top10", game.team2_score,
                                                                                 game.team1_score)
                elif 10 <= game.team1_rank < 30:
                    d = self.update_dictionary_by_rank_window_and_number_of_maps(d, "Top10-Top30", game.team2_score,
                                                                                 game.team1_score)
                elif 30 <= game.team1_rank < 60:
                    d = self.update_dictionary_by_rank_window_and_number_of_maps(d, "Top30-Top60", game.team2_score,
                                                                                 game.team1_score)
                elif 60 <= game.team1_rank < 90:
                    d = self.update_dictionary_by_rank_window_and_number_of_maps(d, "Top60-Top90", game.team2_score,
                                                                                 game.team1_score)
                else:
                    d = self.update_dictionary_by_rank_window_and_number_of_maps(d, ">Top90", game.team2_score,
                                                                                 game.team1_score)
        return d

    def win_lost_percentage_by_rank_window_and_maps(self, team_id, team_games):
        d = {"<Top10": {}, "Top10-Top30": {}, "Top30-Top60": {}, "Top60-Top90": {}, ">Top90": {}}

        for game in team_games:
            for game_map in game.maps:
                if game.id_team1 == team_id:
                    if game.team2_rank < 10:
                        d = self.update_dictionary_by_top_and_map(d, game_map, "<Top10", game_map.team1_total_rounds,
                                                                  game_map.team2_total_rounds)
                    elif 10 <= game.team2_rank < 30:
                        d = self.update_dictionary_by_top_and_map(d, game_map, "Top10-Top30",
                                                                  game_map.team1_total_rounds,
                                                                  game_map.team2_total_rounds)
                    elif 30 <= game.team2_rank < 60:
                        d = self.update_dictionary_by_top_and_map(d, game_map, "Top30-Top60",
                                                                  game_map.team1_total_rounds,
                                                                  game_map.team2_total_rounds)
                    elif 60 <= game.team2_rank < 90:
                        d = self.update_dictionary_by_top_and_map(d, game_map, "Top60-Top90",
                                                                  game_map.team1_total_rounds,
                                                                  game_map.team2_total_rounds)
                    else:
                        d = self.update_dictionary_by_top_and_map(d, game_map, ">Top90", game_map.team1_total_rounds,
                                                                  game_map.team2_total_rounds)
                else:
                    if game.team1_rank < 10:
                        d = self.update_dictionary_by_top_and_map(d, game_map, "<Top10", game_map.team2_total_rounds,
                                                                  game_map.team1_total_rounds)
                    elif 10 <= game.team1_rank < 30:
                        d = self.update_dictionary_by_top_and_map(d, game_map, "Top10-Top30",
                                                                  game_map.team2_total_rounds,
                                                                  game_map.team1_total_rounds)
                    elif 30 <= game.team1_rank < 60:
                        d = self.update_dictionary_by_top_and_map(d, game_map, "Top30-Top60",
                                                                  game_map.team2_total_rounds,
                                                                  game_map.team1_total_rounds)
                    elif 60 <= game.team1_rank < 90:
                        d = self.update_dictionary_by_top_and_map(d, game_map, "Top60-Top90",
                                                                  game_map.team2_total_rounds,
                                                                  game_map.team1_total_rounds)
                    else:
                        d = self.update_dictionary_by_top_and_map(d, game_map, ">Top90", game_map.team2_total_rounds,
                                                                  game_map.team1_total_rounds)
        return d

    def update_dictionary_by_top_and_map(self, d, map, rankKey, totalRounds1, totalRounds2):
        if d[rankKey].get(map.map_name) is None:
            t = {map.map_name: {"Win": 0, "Lost": 0}}
            if totalRounds1 > totalRounds2:
                t[map.map_name]["Win"] = 1
            else:
                t[map.map_name]["Lost"] = 1
            d[rankKey].update(t)
        else:
            if totalRounds1 > totalRounds2:
                d[rankKey][map.map_name]["Win"] = d[rankKey][map.map_name]["Win"] + 1
            else:
                d[rankKey][map.map_name]["Lost"] = d[rankKey][map.map_name]["Lost"] + 1
        return d

    def update_dictionary_by_rank_window_and_number_of_maps(self, d, rankKey, totalRounds1, totalRounds2):
        if d[rankKey].get("2Or3Maps") is None:
            t = {"2Or3Maps": {"2Maps": 0, "3Maps": 0}}
            if totalRounds1 + totalRounds2 == 3:
                t["2Or3Maps"]["3Maps"] = 1
            else:
                t["2Or3Maps"]["2Maps"] = 1
            d[rankKey].update(t)
        else:
            if totalRounds1 + totalRounds2 == 3:
                d[rankKey]["2Or3Maps"]["3Maps"] = d[rankKey]["2Or3Maps"]["3Maps"] + 1
            else:
                d[rankKey]["2Or3Maps"]["2Maps"] = d[rankKey]["2Or3Maps"]["2Maps"] + 1
        return d

    def get_win_percentage_by_maps_and_opp_window_rank_dictionary(self, map_key, win_lost_map_team, opp_rank_key):
        Map1 = 100 * (win_lost_map_team[opp_rank_key][map_key]["Win"] /
                      (win_lost_map_team[opp_rank_key][map_key]["Win"] + win_lost_map_team[opp_rank_key][map_key][
                          "Lost"])) \
            if win_lost_map_team[opp_rank_key].get(map_key) is not None else 0.0

        return {map_key: Map1}

    def get_win_percentage_by_maps_and_opp_rank_dictionary(self, win_lost_map_team, opp_rank, maps):
        d = {}
        for map_key in maps:
            if opp_rank < 10:
                d.update(self.get_win_percentage_by_maps_and_opp_window_rank_dictionary(map_key, win_lost_map_team,
                                                                                        "<Top10"))
            elif 10 <= opp_rank < 30:
                d.update(self.get_win_percentage_by_maps_and_opp_window_rank_dictionary(map_key, win_lost_map_team,
                                                                                        "Top10-Top30"))
            elif 30 <= opp_rank < 60:
                d.update(self.get_win_percentage_by_maps_and_opp_window_rank_dictionary(map_key, win_lost_map_team,
                                                                                        "Top30-Top60"))
            elif 60 <= opp_rank < 90:
                d.update(self.get_win_percentage_by_maps_and_opp_window_rank_dictionary(map_key, win_lost_map_team,
                                                                                        "Top60-Top90"))
            elif opp_rank >= 90:
                d.update(self.get_win_percentage_by_maps_and_opp_window_rank_dictionary(map_key, win_lost_map_team,
                                                                                        ">Top90"))
        return d

    def get_win_on_2maps_or_3maps_percentage_by_opp_rank(self, win_lost_maps_by_opp_rank, oppActualRank):
        if oppActualRank < 10:
            Maps2 = 100 * ((win_lost_maps_by_opp_rank["<Top10"]["2Or3Maps"]["2Maps"]) / (
                    win_lost_maps_by_opp_rank["<Top10"]["2Or3Maps"]["2Maps"] +
                    win_lost_maps_by_opp_rank["<Top10"]["2Or3Maps"]["3Maps"]))
            Maps3 = 100 * ((win_lost_maps_by_opp_rank["<Top10"]["2Or3Maps"]["3Maps"]) / (
                    win_lost_maps_by_opp_rank["<Top10"]["2Or3Maps"]["2Maps"] +
                    win_lost_maps_by_opp_rank["<Top10"]["2Or3Maps"]["3Maps"]))
            return {"2Maps": Maps2, "3Maps": Maps3}
        elif 10 <= oppActualRank < 30:
            Maps2 = 100 * ((win_lost_maps_by_opp_rank["Top10-Top30"]["2Or3Maps"]["2Maps"]) / (
                    win_lost_maps_by_opp_rank["Top10-Top30"]["2Or3Maps"]["2Maps"] +
                    win_lost_maps_by_opp_rank["Top10-Top30"]["2Or3Maps"]["3Maps"]))
            Maps3 = 100 * ((win_lost_maps_by_opp_rank["Top10-Top30"]["2Or3Maps"]["3Maps"]) / (
                    win_lost_maps_by_opp_rank["Top10-Top30"]["2Or3Maps"]["2Maps"] +
                    win_lost_maps_by_opp_rank["Top10-Top30"]["2Or3Maps"]["3Maps"]))
            return {"2Maps": Maps2, "3Maps": Maps3}
        elif 30 <= oppActualRank < 60:
            Maps2 = 100 * ((win_lost_maps_by_opp_rank["Top30-Top60"]["2Or3Maps"]["2Maps"]) / (
                    win_lost_maps_by_opp_rank["Top30-Top60"]["2Or3Maps"]["2Maps"] +
                    win_lost_maps_by_opp_rank["Top30-Top60"]["2Or3Maps"]["3Maps"]))
            Maps3 = 100 * ((win_lost_maps_by_opp_rank["Top30-Top60"]["2Or3Maps"]["3Maps"]) / (
                    win_lost_maps_by_opp_rank["Top30-Top60"]["2Or3Maps"]["2Maps"] +
                    win_lost_maps_by_opp_rank["Top30-Top60"]["2Or3Maps"]["3Maps"]))
            return {"2Maps": Maps2, "3Maps": Maps3}
        elif 60 <= oppActualRank < 90:
            Maps2 = 100 * ((win_lost_maps_by_opp_rank["Top60-Top90"]["2Or3Maps"]["2Maps"]) / (
                    win_lost_maps_by_opp_rank["Top60-Top90"]["2Or3Maps"]["2Maps"] +
                    win_lost_maps_by_opp_rank["Top60-Top90"]["2Or3Maps"]["3Maps"]))
            Maps3 = 100 * ((win_lost_maps_by_opp_rank["Top60-Top90"]["2Or3Maps"]["3Maps"]) / (
                    win_lost_maps_by_opp_rank["Top60-Top90"]["2Or3Maps"]["2Maps"] +
                    win_lost_maps_by_opp_rank["Top60-Top90"]["2Or3Maps"]["3Maps"]))
            return {"2Maps": Maps2, "3Maps": Maps3}
        elif oppActualRank >= 90:
            Maps2 = 100 * ((win_lost_maps_by_opp_rank[">Top90"]["2Or3Maps"]["2Maps"]) / (
                    win_lost_maps_by_opp_rank[">Top90"]["2Or3Maps"]["2Maps"] +
                    win_lost_maps_by_opp_rank[">Top90"]["2Or3Maps"]["3Maps"]))
            Maps3 = 100 * ((win_lost_maps_by_opp_rank[">Top90"]["2Or3Maps"]["3Maps"]) / (
                    win_lost_maps_by_opp_rank[">Top90"]["2Or3Maps"]["2Maps"] +
                    win_lost_maps_by_opp_rank[">Top90"]["2Or3Maps"]["3Maps"]))
            return {"2Maps": Maps2, "3Maps": Maps3}

    def win_rank_matrix(self):
        df = pd.DataFrame(0, index= [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],#['top10','top20','top30','top40','top50','top60','top70', 'top80','top90','top100',
                                    #'top110'],
                          columns=['top10','top20','top30','top40','top50','top60','top70','top80','top90','top100',
                                   'top110'])
        df2 = pd.DataFrame(0, index= [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], columns=['top10', 'top20', 'top30', 'top40', 'top50', 'top60',
                                                           'top70', 'top80', 'top90', 'top100', 'top110'])
        games = GameDAO().list_last_games()
        for game_item in games:
            if game_item.team1_rank < 10:
                self.team2_win_rank_matrix(df, df2, game_item, 0)
            if 10 <= game_item.team1_rank < 20:
                self.team2_win_rank_matrix(df, df2, game_item, 1)
            if 20 <= game_item.team1_rank < 30:
                self.team2_win_rank_matrix(df, df2, game_item, 2)
            if 30 <= game_item.team1_rank < 40:
                self.team2_win_rank_matrix(df, df2, game_item, 3)
            if 40 <= game_item.team1_rank < 50:
                self.team2_win_rank_matrix(df, df2, game_item, 4)
            if 50 <= game_item.team1_rank < 60:
                self.team2_win_rank_matrix(df, df2, game_item, 5)
            if 60 <= game_item.team1_rank < 70:
                self.team2_win_rank_matrix(df, df2, game_item, 6)
            if 70 <= game_item.team1_rank < 80:
                self.team2_win_rank_matrix(df, df2, game_item, 7)
            if 80 <= game_item.team1_rank < 90:
                self.team2_win_rank_matrix(df, df2, game_item, 8)
            if 90 <= game_item.team1_rank < 100:
                self.team2_win_rank_matrix(df, df2, game_item, 9)
            if game_item.team1_rank >= 100:
                self.team2_win_rank_matrix(df, df2, game_item, 10)
        return df, df2

    def team2_win_rank_matrix(self, df, df2, game_item, team1_rank):
        self.diff_ranks_scores(team1_rank, 'top10', df, df2, 0, 10, game_item.team2_rank, game_item.team1_score,
                               game_item.team2_score)
        self.diff_ranks_scores(team1_rank, 'top20', df, df2, 10, 20, game_item.team2_rank, game_item.team1_score,
                               game_item.team2_score)
        self.diff_ranks_scores(team1_rank, 'top30', df, df2, 20, 30, game_item.team2_rank, game_item.team1_score,
                               game_item.team2_score)
        self.diff_ranks_scores(team1_rank, 'top40', df, df2, 30, 40, game_item.team2_rank, game_item.team1_score,
                               game_item.team2_score)
        self.diff_ranks_scores(team1_rank, 'top50', df, df2, 40, 50, game_item.team2_rank, game_item.team1_score,
                               game_item.team2_score)
        self.diff_ranks_scores(team1_rank, 'top60', df, df2, 50, 60, game_item.team2_rank, game_item.team1_score,
                               game_item.team2_score)
        self.diff_ranks_scores(team1_rank, 'top70', df, df2, 60, 70, game_item.team2_rank, game_item.team1_score,
                               game_item.team2_score)
        self.diff_ranks_scores(team1_rank, 'top80', df, df2, 70, 80, game_item.team2_rank, game_item.team1_score,
                               game_item.team2_score)
        self.diff_ranks_scores(team1_rank, 'top90', df, df2, 80, 90, game_item.team2_rank, game_item.team1_score,
                               game_item.team2_score)
        self.diff_ranks_scores(team1_rank, 'top100', df, df2, 90, 100, game_item.team2_rank, game_item.team1_score,
                               game_item.team2_score)
        self.diff_ranks_scores(team1_rank, 'top110', df, df2, 110, 400, game_item.team2_rank, game_item.team1_score,
                               game_item.team2_score)

    def diff_ranks_scores(self, team1_rank_key, team2_rank_key, df1, df2, lower_rank, higher_rank, team_rank, score1, score2):
        if lower_rank <= team_rank < higher_rank:
            if score1 > score2:
                df1.loc[team1_rank_key, team2_rank_key] = df1.loc[team1_rank_key, team2_rank_key] + 1
            df2.loc[team1_rank_key, team2_rank_key] = df2.loc[team1_rank_key, team2_rank_key] + 1

