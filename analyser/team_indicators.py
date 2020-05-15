from dao.game_dao import GameDAO


class TeamIndicators:
    def __init(self):
        pass

    def get_team_confidence(self, team1_id, team1games):
        d = {}
        for game in team1games:
            if game.team1.id_team == team1_id:
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
            elif game.team2.id_team == team1_id:
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
            d[item]["Confidence"] = 100 * d[item]["Win"] / d[item]["Pick"]

        return d

    def win_lost_count_game_by_rank_window(self, team1, team1games):
        d = {"<Top10": {},
             "Top10-Top30": {},
             "Top30-Top60": {},
             "Top60-Top90": {},
             ">Top90": {}
             }

        for game in team1games:
            if game.team1.name == team1:
                if game.team2_rank < 10:
                    d = self.updateDictionaryTopFieldAndGame(d, "<Top10", game.team1_score, game.team2_score)
                elif 10 <= game.team2_rank < 30:
                    d = self.updateDictionaryTopFieldAndGame(d, "Top10-Top30", game.team1_score, game.team2_score)
                elif 30 <= game.team2_rank < 60:
                    d = self.updateDictionaryTopFieldAndGame(d, "Top30-Top60", game.team1_score, game.team2_score)
                elif 60 <= game.team2_rank < 90:
                    d = self.updateDictionaryTopFieldAndGame(d, "Top60-Top90", game.team1_score, game.team2_score)
                else:
                    d = self.updateDictionaryTopFieldAndGame(d, ">Top90", game.team1_score, game.team2_score)
            else:
                if game.team1_rank < 10:
                    d = self.updateDictionaryTopFieldAndGame(d, "<Top10", game.team2_score, game.team1_score)
                elif 10 <= game.team1_rank < 30:
                    d = self.updateDictionaryTopFieldAndGame(d, "Top10-Top30", game.team2_score, game.team1_score)
                elif 30 <= game.team1_rank < 60:
                    d = self.updateDictionaryTopFieldAndGame(d, "Top30-Top60", game.team2_score, game.team1_score)
                elif 60 <= game.team1_rank < 90:
                    d = self.updateDictionaryTopFieldAndGame(d, "Top60-Top90", game.team2_score, game.team1_score)
                else:
                    d = self.updateDictionaryTopFieldAndGame(d, ">Top90")
        return d

    def win_lost_percentage_by_rank_window(self, team1, team1Games):
        d = {"<Top10": {},
             "Top10-Top30": {},
             "Top30-Top60": {},
             "Top60-Top90": {},
             ">Top90": {}
             }

        for game in team1Games:
            if game.team1.name == team1:
                for map in game.maps:
                    if game.team2_rank < 10:
                        d = self.updateDictionaryTopFieldAndMap(d, map, "<Top10", map.team1_total_rounds,
                                                                map.team2_total_rounds)
                    elif game.team2_rank >= 10 and game.team2_rank < 30:
                        d = self.updateDictionaryTopFieldAndMap(d, map, "Top10-Top30", map.team1_total_rounds,
                                                                map.team2_total_rounds)
                    elif game.team2_rank >= 30 and game.team2_rank < 60:
                        d = self.updateDictionaryTopFieldAndMap(d, map, "Top30-Top60", map.team1_total_rounds,
                                                                map.team2_total_rounds)
                    elif game.team2_rank >= 60 and game.team2_rank < 90:
                        d = self.updateDictionaryTopFieldAndMap(d, map, "Top60-Top90", map.team1_total_rounds,
                                                                map.team2_total_rounds)
                    else:
                        d = self.updateDictionaryTopFieldAndMap(d, map, ">Top90", map.team1_total_rounds,
                                                                map.team2_total_rounds)
            else:
                for map in game.maps:
                    if game.team1_rank < 10:
                        d = self.updateDictionaryTopFieldAndMap(d, map, "<Top10", map.team2_total_rounds,
                                                                map.team1_total_rounds)
                    elif game.team1_rank >= 10 and game.team1_rank < 30:
                        d = self.updateDictionaryTopFieldAndMap(d, map, "Top10-Top30", map.team2_total_rounds,
                                                                map.team1_total_rounds)
                    elif game.team1_rank >= 30 and game.team1_rank < 60:
                        d = self.updateDictionaryTopFieldAndMap(d, map, "Top30-Top60", map.team2_total_rounds,
                                                                map.team1_total_rounds)
                    elif game.team1_rank >= 60 and game.team1_rank < 90:
                        d = self.updateDictionaryTopFieldAndMap(d, map, "Top60-Top90", map.team2_total_rounds,
                                                                map.team1_total_rounds)
                    else:
                        d = self.updateDictionaryTopFieldAndMap(d, map, ">Top90")
        return d

    def updateDictionaryTopFieldAndMap(self, d, map, rankKey, totalRounds1, totalRounds2):
        if d[rankKey].get(map.map_name) == None:
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

    def updateDictionaryTopFieldAndGame(self, d, rankKey, totalRounds1, totalRounds2):
        if d[rankKey].get("2Or3Maps") == None:
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

    def getWinPercentageOppRankDictionary(self, maps, winLostMapTeam, mapKey):
        Map1 = 100 * (winLostMapTeam[mapKey][maps[0]]["Win"] /
                      (winLostMapTeam[mapKey][maps[0]]["Win"] + winLostMapTeam[mapKey][maps[0]]["Lost"])) if \
            winLostMapTeam[mapKey].get(maps[0]) != None else 0.0
        Map2 = 100 * (winLostMapTeam[mapKey][maps[1]]["Win"] /
                      (winLostMapTeam[mapKey][maps[1]]["Win"] + winLostMapTeam[mapKey][maps[1]]["Lost"])) if \
            winLostMapTeam[mapKey].get(maps[1]) != None else 0.0
        Map3 = 100 * (winLostMapTeam[mapKey][maps[2]]["Win"] /
                      (winLostMapTeam[mapKey][maps[2]]["Win"] + winLostMapTeam[mapKey][maps[2]]["Lost"])) if \
            winLostMapTeam[mapKey].get(maps[2]) != None else 0.0
        return {maps[0]: Map1, maps[1]: Map2, maps[2]: Map3}

    def getWinPercentageByOppRankAndMaps(self, winLostMapTeam, oppActualRank, maps):
        if oppActualRank < 10:
            return self.getWinPercentageOppRankDictionary(maps, winLostMapTeam, "<Top10")
        elif oppActualRank >= 10 and oppActualRank < 30:
            return self.getWinPercentageOppRankDictionary(maps, winLostMapTeam, "Top10-Top30")
        elif oppActualRank >= 30 and oppActualRank < 60:
            return self.getWinPercentageOppRankDictionary(maps, winLostMapTeam, "Top30-Top60")
        elif oppActualRank >= 60 and oppActualRank < 90:
            return self.getWinPercentageOppRankDictionary(maps, winLostMapTeam, "Top60-Top90")
        elif oppActualRank >= 90:
            return self.getWinPercentageOppRankDictionary(maps, winLostMapTeam, "<Top90")

    def getWin2MapsAnd3MapsPercentageByOppRank(self, winLostCountMapsByOppRank, oppActualRank):
        if oppActualRank < 10:
            Maps2 = 100 * ((winLostCountMapsByOppRank["<Top10"]["2Or3Maps"]["2Maps"]) / (
                    winLostCountMapsByOppRank["<Top10"]["2Or3Maps"]["2Maps"] +
                    winLostCountMapsByOppRank["<Top10"]["2Or3Maps"]["3Maps"]))
            Maps3 = 100 * ((winLostCountMapsByOppRank["<Top10"]["2Or3Maps"]["3Maps"]) / (
                    winLostCountMapsByOppRank["<Top10"]["2Or3Maps"]["2Maps"] +
                    winLostCountMapsByOppRank["<Top10"]["2Or3Maps"]["3Maps"]))
            return {"2Maps": Maps2, "3Maps": Maps3}
        elif oppActualRank >= 10 and oppActualRank < 30:
            Maps2 = 100 * ((winLostCountMapsByOppRank["Top10-Top30"]["2Or3Maps"]["2Maps"]) / (
                    winLostCountMapsByOppRank["Top10-Top30"]["2Or3Maps"]["2Maps"] +
                    winLostCountMapsByOppRank["Top10-Top30"]["2Or3Maps"]["3Maps"]))
            Maps3 = 100 * ((winLostCountMapsByOppRank["Top10-Top30"]["2Or3Maps"]["3Maps"]) / (
                    winLostCountMapsByOppRank["Top10-Top30"]["2Or3Maps"]["2Maps"] +
                    winLostCountMapsByOppRank["Top10-Top30"]["2Or3Maps"]["3Maps"]))
            return {"2Maps": Maps2, "3Maps": Maps3}
        elif oppActualRank >= 30 and oppActualRank < 60:
            Maps2 = 100 * ((winLostCountMapsByOppRank["Top30-Top60"]["2Or3Maps"]["2Maps"]) / (
                    winLostCountMapsByOppRank["Top30-Top60"]["2Or3Maps"]["2Maps"] +
                    winLostCountMapsByOppRank["Top30-Top60"]["2Or3Maps"]["3Maps"]))
            Maps3 = 100 * ((winLostCountMapsByOppRank["Top30-Top60"]["2Or3Maps"]["3Maps"]) / (
                    winLostCountMapsByOppRank["Top30-Top60"]["2Or3Maps"]["2Maps"] +
                    winLostCountMapsByOppRank["Top30-Top60"]["2Or3Maps"]["3Maps"]))
            return {"2Maps": Maps2, "3Maps": Maps3}
        elif oppActualRank >= 60 and oppActualRank < 90:
            Maps2 = 100 * ((winLostCountMapsByOppRank["Top60-Top90"]["2Or3Maps"]["2Maps"]) / (
                    winLostCountMapsByOppRank["Top60-Top90"]["2Or3Maps"]["2Maps"] +
                    winLostCountMapsByOppRank["Top60-Top90"]["2Or3Maps"]["3Maps"]))
            Maps3 = 100 * ((winLostCountMapsByOppRank["Top60-Top90"]["2Or3Maps"]["3Maps"]) / (
                    winLostCountMapsByOppRank["Top60-Top90"]["2Or3Maps"]["2Maps"] +
                    winLostCountMapsByOppRank["Top60-Top90"]["2Or3Maps"]["3Maps"]))
            return {"2Maps": Maps2, "3Maps": Maps3}
        elif oppActualRank >= 90:
            Maps2 = 100 * ((winLostCountMapsByOppRank[">Top90"]["2Or3Maps"]["2Maps"]) / (
                    winLostCountMapsByOppRank[">Top90"]["2Or3Maps"]["2Maps"] +
                    winLostCountMapsByOppRank[">Top90"]["2Or3Maps"]["3Maps"]))
            Maps3 = 100 * ((winLostCountMapsByOppRank[">Top90"]["2Or3Maps"]["3Maps"]) / (
                    winLostCountMapsByOppRank[">Top90"]["2Or3Maps"]["2Maps"] +
                    winLostCountMapsByOppRank[">Top90"]["2Or3Maps"]["3Maps"]))
            return {"2Maps": Maps2, "3Maps": Maps3}
