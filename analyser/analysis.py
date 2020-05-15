import pandas as pd
from db import db
import requests
from bs4 import BeautifulSoup, Comment
from datetime import datetime as dt
from analyser.team_indicators import TeamPickMapsConfidence
from dao.team_dao import TeamDAO
from dao.game_dao import GameDAO

class Analysis():
    def __init__(self):
        pass

    def getWinPercentageOppRankDictionary(self, maps, winLostMapTeam, mapKey):
        Map1 = 100*(winLostMapTeam[mapKey][maps[0]]["Win"] /
                (winLostMapTeam[mapKey][maps[0]]["Win"] + winLostMapTeam[mapKey][maps[0]]["Lost"])) if \
            winLostMapTeam[mapKey].get(maps[0]) != None else 0.0
        Map2 = 100*(winLostMapTeam[mapKey][maps[1]]["Win"] /
                (winLostMapTeam[mapKey][maps[1]]["Win"] + winLostMapTeam[mapKey][maps[1]]["Lost"])) if \
            winLostMapTeam[mapKey].get(maps[1]) != None else 0.0
        Map3 = 100*(winLostMapTeam[mapKey][maps[2]]["Win"] /
                (winLostMapTeam[mapKey][maps[2]]["Win"] + winLostMapTeam[mapKey][maps[2]]["Lost"])) if \
            winLostMapTeam[mapKey].get(maps[2]) != None else 0.0
        return {maps[0]: Map1, maps[1]: Map2, maps[2]: Map3}

    def getWinPercentageOppRank(self, winLostMapTeam, oppActualRank, maps):
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

    def getAnalysis(self, team1, team2, maps):
        confidenceTeam1 = TeamPickMapsConfidence().get_team_confidence(team1)
        confidenceTeam2 = TeamPickMapsConfidence().get_team_confidence(team2)

        winLostByRankAndMap1 = TeamPickMapsConfidence().win_lost_percentage_by_rank_window(team1)
        winLostByRankAndMap2 = TeamPickMapsConfidence().win_lost_percentage_by_rank_window(team2)

        winLostCountGameByRank1 = TeamPickMapsConfidence().win_lost_count_game_by_rank_window(team1)
        winLostCountGameByRank2 = TeamPickMapsConfidence().win_lost_count_game_by_rank_window(team2)

        team1Object = TeamDAO().getTeamByLikeName(team1)
        team2Object = TeamDAO().getTeamByLikeName(team2)

        team1Info = {"Team": team1,
                     "Rank": team1Object.actual_rank,
                     "Confidence": 0.0,
                     "WinPercentageOppRank": {},
                     "MapsCountOppRank": {}}
        team2Info = {"Team": team2,
                     "Rank": team2Object.actual_rank,
                     "Confidence": 0.0,
                     "WinPercentageOppRank": {},
                     "MapsCountOppRank": {}}

        team1Info["Confidence"] = (confidenceTeam1.get(maps[0])["Confidence"]) if confidenceTeam1.get(maps[0]) != None else 0.0
        team2Info["Confidence"] = (confidenceTeam2.get(maps[1])["Confidence"]) if confidenceTeam2.get(maps[1]) != None else 0.0

        team1Info["WinPercentageOppRank"] = self.getWinPercentageOppRank(winLostByRankAndMap1, team2Object.actual_rank, maps)
        team2Info["WinPercentageOppRank"] = self.getWinPercentageOppRank(winLostByRankAndMap2, team1Object.actual_rank, maps)

        team1Info["MapsCountOppRank"] = self.getWin2MapsAnd3MapsPercentageByOppRank(winLostCountGameByRank1, team2Object.actual_rank)
        team2Info["MapsCountOppRank"] = self.getWin2MapsAnd3MapsPercentageByOppRank(winLostCountGameByRank2, team1Object.actual_rank)

        print(team1Info)
        print(team2Info)

