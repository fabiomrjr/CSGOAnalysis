import pandas as pd
import config
import requests
from bs4 import BeautifulSoup, Comment
from datetime import datetime as dt

from builder.player_builder import PlayerBuilder
from builder.team_builder import TeamBuilder
from dao.team_dao import TeamDAO
from build_game import BuildGame

class BuildTeam:
    def __init__(self):
     pass

    def update_matches_all_teams(self, number_of_matches):

        teams = TeamDAO().listTeamsWithHomePage()
        self.matches_find_and_build_by_teams(teams, number_of_matches)

    def full_update_all_teams(self, number_of_matches):

        teams = TeamDAO().listTeamsWithHomePage()

        for item in teams:
            site = item.homepage
            if site is None or site == "":
                continue

            self.update_team_and_players_info(item, site)

        self.matches_find_and_build_by_teams(teams, number_of_matches)

    def update_team_and_players_info(self, item, site):
        content = ""
        req = requests.get(site)
        if req.status_code == 200:
            print('Requisição de homepage time bem sucedida! Time ' + str(item.name))
            content = req.content
        soup_default = BeautifulSoup(content, 'html.parser')
        table_players_info = soup_default.find_all('div', attrs={'class': 'bodyshot-team g-grid'})
        table_team_rank = soup_default.find_all('div', attrs={'class': 'profile-team-stat'})
        table_str = str(table_players_info[0])
        players_info = BeautifulSoup(table_str, 'html.parser')
        players_array = players_info.text.split("\n")
        world_rank = BeautifulSoup(str(table_team_rank[0]), 'html.parser').text.split("#")[1]
        PlayerBuilder().check(item.id_team, players_array)
        TeamBuilder().provideDefaultTeam(item.name, item.homepage, world_rank, item.hltv_id)

    def matches_find_and_build_by_teams(self, teams, number_of_matches):
        for item in teams:
            start_date = dt.now()
            results = "https://www.hltv.org/results?team=" + str(item.hltv_id)
            item = self.matches_builder(item, results, number_of_matches)
            end_date = dt.now()
            print("Finish Matches Builder Team " + str(item.name) + ". Seconds " +
                  str((end_date - start_date).total_seconds()))

    def matches_builder(self, item, results, number_of_matches):
        content2 = ""
        req = requests.get(results)
        if req.status_code == 200:
            print('Requisição de matches bem sucedida!')
            content2 = req.content

        soup_default2 = BeautifulSoup(content2, 'html.parser')
        table_games_info = soup_default2.find_all('a', attrs={'class': 'a-reset'})

        count = 0
        for item in table_games_info:
            if "matches" in str(item["href"]):
                count = count + 1
        print("Numero de jogos " + str(count))

        count_match = 1
        for item in table_games_info:
            if "matches" in str(item["href"]):
                url = "https://www.hltv.org" + str(item["href"])
                print("Process match " + str(count_match) + " of " + str(count))
                print("Processing match url " + str(url))
                if url in config.urlsToNoConsider:
                    continue
                BuildGame().buildGame(url)
                count_match = count_match + 1
            if count_match == number_of_matches:
                break
        return item

    def full_update_by_team(self, team_name, number_of_matches):

        item = TeamDAO().getTeamByLikeName(team_name)

        site = item.homepage
        self.update_team_and_players_info(item, site)

        start_date = dt.now()

        if item.hltv_id is not None and item.hltv_id != "":
            results = "https://www.hltv.org/results?team=" + str(item.hltv_id)
            item = self.matches_builder(item, results, number_of_matches)

        end_date = dt.now()
        print("Finish Matches Builder Team "+ str(item.name) + ". Seconds " + str((end_date - start_date).total_seconds()))