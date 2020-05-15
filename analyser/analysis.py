import pandas as pd
from db import db
import requests
from bs4 import BeautifulSoup, Comment
from datetime import datetime as dt
from analyser.team_indicators import TeamIndicators
from dao.team_dao import TeamDAO
from dao.game_dao import GameDAO

class Analysis():
    def __init__(self):
        pass

    def getAnalysis(self, team1Name, team2Name, maps):

        team1 = TeamDAO().getTeamByLikeName(team1Name)
        team2 = TeamDAO().getTeamByLikeName(team2Name)

        team1Games = GameDAO().listTeamMapsGames(None, team1Name)
        team2Games = GameDAO().listTeamMapsGames(None, team2Name)

        confidenceTeam1 = TeamIndicators().get_team_confidence(team1.id_team, team1Games)
        confidenceTeam2 = TeamIndicators().get_team_confidence(team2.id_team, team2Games)

        winLostByRankAndMap1 = TeamIndicators().win_lost_percentage_by_rank_window(team1Name, team1Games)
        winLostByRankAndMap2 = TeamIndicators().win_lost_percentage_by_rank_window(team2Name, team2Games)

        winLostCountGameByRank1 = TeamIndicators().win_lost_count_game_by_rank_window(team1Name, team1Games)
        winLostCountGameByRank2 = TeamIndicators().win_lost_count_game_by_rank_window(team2Name, team2Games)

        team1Info = {"Team": team1Name,
                     "Rank": team1.actual_rank,
                     "Confidence": 0.0,
                     "WinPercentageOppRank": {},
                     "MapsCountOppRank": {}}
        team2Info = {"Team": team2Name,
                     "Rank": team2.actual_rank,
                     "Confidence": 0.0,
                     "WinPercentageOppRank": {},
                     "MapsCountOppRank": {}}

        team1Info["Confidence"] = (confidenceTeam1.get(maps[0])["Confidence"]) if confidenceTeam1.get(maps[0]) != None else 0.0
        team2Info["Confidence"] = (confidenceTeam2.get(maps[1])["Confidence"]) if confidenceTeam2.get(maps[1]) != None else 0.0

        team1Info["WinPercentageOppRank"] = TeamIndicators().getWinPercentageByOppRankAndMaps(winLostByRankAndMap1, team2.actual_rank, maps)
        team2Info["WinPercentageOppRank"] = TeamIndicators().getWinPercentageByOppRankAndMaps(winLostByRankAndMap2, team1.actual_rank, maps)

        team1Info["MapsCountOppRank"] = TeamIndicators().getWin2MapsAnd3MapsPercentageByOppRank(winLostCountGameByRank1, team2.actual_rank)
        team2Info["MapsCountOppRank"] = TeamIndicators().getWin2MapsAnd3MapsPercentageByOppRank(winLostCountGameByRank2, team1.actual_rank)

        print(team1Info)
        print(team2Info)

