import pandas as pd
from db import db
import requests
from bs4 import BeautifulSoup, Comment
from datetime import datetime as dt
import analyser.team_indicators as team_indicators

from analyser.team_indicators import TeamIndicators
from dao.team_dao import TeamDAO
from dao.game_dao import GameDAO

class Analysis:
    def __init__(self):
        pass

    def get_analysis(self, team1_name, team2_name, maps):

        team1 = TeamDAO().getTeamByLikeName(team1_name)
        team2 = TeamDAO().getTeamByLikeName(team2_name)

        team1_games_maps = GameDAO().list_team_top_games_maps(None, team1_name)
        team2_games_maps = GameDAO().list_team_top_games_maps(None, team2_name)

        team1_confidence = team_indicators.get_team_confidence(team1.id_team, team1_games_maps)
        team2_confidence = team_indicators.get_team_confidence(team2.id_team, team2_games_maps)

        winLostByRankAndMap1 = TeamIndicators().win_lost_percentage_by_rank_window_and_maps(team1_name, team1_games_maps)
        winLostByRankAndMap2 = TeamIndicators().win_lost_percentage_by_rank_window_and_maps(team2_name, team2_games_maps)

        winLostCountGameByRank1 = TeamIndicators().win_lost_number_maps_by_rank_window(team1_name, team1_games_maps)
        winLostCountGameByRank2 = TeamIndicators().win_lost_number_maps_by_rank_window(team2_name, team2_games_maps)

        team1Info = {"Team": team1_name, "Rank": team1.actual_rank, "Confidence": 0.0, "WinPercentageOppRank": {},
                     "MapsCountOppRank": {}}
        team2Info = {"Team": team2_name, "Rank": team2.actual_rank, "Confidence": 0.0, "WinPercentageOppRank": {},
                     "MapsCountOppRank": {}}

        team1Info["Confidence"] = (team1_confidence.get(maps[0])["Confidence"]) if team1_confidence.get(maps[0]) != None else 0.0
        team2Info["Confidence"] = (team2_confidence.get(maps[1])["Confidence"]) if team2_confidence.get(maps[1]) != None else 0.0

        team1Info["WinPercentageOppRank"] = TeamIndicators().get_win_percentage_by_maps_and_opp_rank_dictionary(winLostByRankAndMap1, team2.actual_rank, maps)
        team2Info["WinPercentageOppRank"] = TeamIndicators().get_win_percentage_by_maps_and_opp_rank_dictionary(winLostByRankAndMap2, team1.actual_rank, maps)

        team1Info["MapsCountOppRank"] = TeamIndicators().get_win_on_2maps_or_3maps_percentage_by_opp_rank(winLostCountGameByRank1, team2.actual_rank)
        team2Info["MapsCountOppRank"] = TeamIndicators().get_win_on_2maps_or_3maps_percentage_by_opp_rank(winLostCountGameByRank2, team1.actual_rank)

        print(team1Info)
        print(team2Info)

