import pandas as pd
import requests
import util

from bs4 import BeautifulSoup
from dao.game_dao import GameDAO
from dao.team_dao import TeamDAO

from builder.game_builder import GameBuilder

class BuildGame:
    def __init__(self):
     pass

    def buildGame(self, url):
        content = ""
        req = requests.get(url)
        if req.status_code == 200:
            content = req.content

        soupDefault = BeautifulSoup(content, 'html.parser')

        game_info = soupDefault.find_all('div', attrs={'class': 'standard-box teamsBox'})
        game_info_array = BeautifulSoup(str(game_info[0]), 'html.parser').text.split("\n")

        picks_remove_info = soupDefault.find_all('div', attrs={'class': 'padding'})
        picks_remove_info_array = BeautifulSoup(str(picks_remove_info), 'html.parser').text.split("\n")

        maps_ct_tr_info = soupDefault.find_all('div', attrs={'class': 'flexbox-column'})
        maps_ct_tr_info_array = BeautifulSoup(str(maps_ct_tr_info), 'html.parser').text.split("\n")

        maps_stats_info = soupDefault.find_all('table', attrs={'class':'table totalstats'})
        frames = []
        for t in maps_stats_info:
            table = pd.read_html(str(t))[0]
            frames.append(table)

        team_game_rank = soupDefault.find_all('div', attrs={'class': 'teamRanking'})
        team_rank_array = BeautifulSoup(str(team_game_rank), 'html.parser').text.replace("World rank: #", "").split(",")

        rounds_detail_informations = soupDefault.find_all('div', attrs={'class': 'results-center-half-score'})

        GameBuilder().create_game(game_info_array, picks_remove_info_array, maps_ct_tr_info_array, frames, team_rank_array, rounds_detail_informations)

    def game_already_exist(self, game_info_array):

        if len(game_info_array) == 19:
            return True

        team1_name = game_info_array[3]
        team2_name = game_info_array[17]
        game_hour = game_info_array[9]
        game_date = game_info_array[10]
        game_datetime = util.get_date_time_by_day_and_time(game_date, game_hour)

        team1 = TeamDAO().getTeamByLikeName(str(team1_name))
        if team1 == None:
            team1 = TeamDAO().createTeam(team1_name, "", None, None)

        team2 = TeamDAO().getTeamByLikeName(str(team2_name))
        if team2 == None:
            team2 = TeamDAO().createTeam(team2_name, "", None, None)

        game = GameDAO().getGameByTeamsAndDateTime(team1.id_team, team2.id_team, game_datetime)
        if game != None:
            return True
        else:
            return False
