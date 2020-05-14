import pandas as pd
import config
import requests
from bs4 import BeautifulSoup, Comment
from datetime import datetime as dt

from builder.player_builder import PlayerBuilder
from builder.team_builder import TeamBuilder
from dao.team_dao import TeamDAO
from buildGame import BuildGame

class BuildTeam:
    def __init__(self):
     pass

    def fullUpdateAllTeams(self, numberOfMatches):

        Teams = TeamDAO().listTeamsWithHomePage()

        for item in Teams:
            site = item.homepage
            if site == None or site == "":
                continue

            self.updateTeamAndPlayersInfo(item, site)

        self.machesBuilderByTeams(Teams, numberOfMatches)

    def updateTeamAndPlayersInfo(self, item, site):
        content = ""
        req = requests.get(site)
        if req.status_code == 200:
            print('Requisição de homepage time bem sucedida! Time ' + str(item.name))
            content = req.content
        soupDefault = BeautifulSoup(content, 'html.parser')
        table_players_info = soupDefault.find_all('div', attrs={'class': 'bodyshot-team g-grid'})
        table_team_rank = soupDefault.find_all('div', attrs={'class': 'profile-team-stat'})
        table_str = str(table_players_info[0])
        playersInfo = BeautifulSoup(table_str, 'html.parser')
        Players_Array = playersInfo.text.split("\n")
        world_rank = BeautifulSoup(str(table_team_rank[0]), 'html.parser').text.split("#")[1]
        PlayerBuilder().check(item.id_team, Players_Array)
        TeamBuilder().provideDefaultTeam(item.name, item.homepage, world_rank, item.hltv_id)

    def machesBuilderByTeams(self, Teams, numberOfMatches):
        for item in Teams:
            startDate = dt.now()
            results = "https://www.hltv.org/results?team=" + str(item.hltv_id)
            item = self.matchesBuilder(item, results, numberOfMatches)
            endDate = dt.now()
            print(
                "Finish Matches Builder Team " + str(item.name) + ". Seconds " + str((endDate - startDate).total_seconds()))

    def matchesBuilder(self, item, results, numberOfMatches):
        content2 = ""
        req = requests.get(results)
        if req.status_code == 200:
            print('Requisição de matches bem sucedida!')
            content2 = req.content

        soupDefault2 = BeautifulSoup(content2, 'html.parser')
        table_games_info = soupDefault2.find_all('a', attrs={'class': 'a-reset'})

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
            if count_match == numberOfMatches:
                break
        return item

    def fullUpdateByTeam(self, team_name, numberOfMatches):

        item = TeamDAO().getTeamByLikeName(team_name)

        site = item.homepage
        self.updateTeamAndPlayersInfo(item, site)

        startDate = dt.now()

        if item.hltv_id != None and item.hltv_id != "":
            results = "https://www.hltv.org/results?team=" + str(item.hltv_id)
            item = self.matchesBuilder(item, results, numberOfMatches)

        endDate = dt.now()
        print("Finish Matches Builder Team "+ str(item.name) + ". Seconds " + str((endDate - startDate).total_seconds()))