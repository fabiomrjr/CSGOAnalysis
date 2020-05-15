import util
import re

from builder.player_builder import PlayerBuilder
from dao.map_dao import MapDAO
from dao.game_dao import GameDAO
from dao.team_dao import TeamDAO
from dao.player_map_stats_dao import PlayerMapStatsDAO
from dao.championship_dao import ChampionshipDAO


class GameBuilder:

    def __init__(self):
        pass

    def create_game(self, game_info_array, picks_remove_info_array, maps_ct_tr_info_array, frames, team_rank_array,
                    rounds_detail_informations):

        team1_name = game_info_array[3]
        team2_name = game_info_array[17]
        team1_score = int(game_info_array[5])
        team2_score = int(game_info_array[19])
        game_hour = game_info_array[9]
        game_date = game_info_array[10]
        game_datetime = util.get_date_time_by_day_and_time(game_date, game_hour)
        championship_name = game_info_array[11]

        team1 = TeamDAO().getTeamByLikeName(str(team1_name))
        if team1 is None:
            team1 = TeamDAO().createTeam(team1_name, "", None, None)

        team2 = TeamDAO().getTeamByLikeName(str(team2_name))
        if team2 is None:
            team2 = TeamDAO().createTeam(team2_name, "", None, None)

        game = GameDAO().getGameByTeamsAndDateTime(team1.id_team, team2.id_team, game_datetime)
        # if game != None or len(frames) == 0:
        #    return

        team1_rank_ = "100" if "Unranked" in team_rank_array[0][1:] else team_rank_array[0][1:]
        team2_rank_ = "100" if "Unranked" in team_rank_array[1][:-1] else team_rank_array[1][:-1]
        team1_rank = int(team1_rank_)
        team2_rank = int(team2_rank_)

        best_of = int(picks_remove_info_array[0].split(" ")[2][:1])
        if best_of == 1:
            if team1_score > team2_score:
                team1_score = 1
                team2_score = 0
            else:
                team1_score = 0
                team2_score = 1

        team1_pick = ""
        team1_removes = ""
        team2_pick = ""
        team2_removes = ""

        count = 0
        for pick in picks_remove_info_array:
            if count <= 2:
                count = count + 1
                continue
            else:
                # splitted = pick.split(" ")
                # if len(splitted) < 2:
                #    break
                if " picked " in pick:
                    splitted = pick.split(" picked ")
                    if team1_name in splitted[0][3:]:
                        team1_pick = team1_pick + splitted[1] + ";"
                    elif team2_name in splitted[0][3:]:
                        team2_pick = team2_pick + splitted[1] + ";"
                elif " removed " in pick:
                    splitted = pick.split(" removed ")
                    if team1_name in splitted[0][3:]:
                        team1_removes = team1_removes + splitted[1] + ";"
                    elif team2_name in splitted[0][3:]:
                        team2_removes = team2_removes + splitted[1] + ";"
                count = count + 1
        team1_pick = team1_pick[:-1] if len(team1_pick) > 0 else team1_pick
        team1_removes = team1_removes[:-1] if len(team1_removes) > 0 else team1_removes
        team2_pick = team2_pick[:-1] if len(team2_pick) > 0 else team2_pick
        team2_removes = team2_removes[:-1] if len(team2_removes) > 0 else team2_removes

        championship = ChampionshipDAO().getChampionshipByNameAndStartDate(championship_name, None)
        if championship is None:
            championship = ChampionshipDAO().createChampionship(championship_name, None, None, None)

        if len(maps_ct_tr_info_array) < (4 + (best_of - 1) * 26):
            return

        # game = GameDAO().getGameByTeamsAndDateTime(team1.id_team, team2.id_team, game_datetime)
        if game is None:
            if team1_score > team2_score:
                game = GameDAO().createGame(championship.id_championship, team1.id_team, team2.id_team, game_datetime,
                                            team1_score, team2_score, team1.id_team, best_of,
                                            team1_pick, team2_pick, team1_removes, team2_removes, team1_rank,
                                            team2_rank)
            elif team1_score < team2_score:
                game = GameDAO().createGame(championship.id_championship, team1.id_team, team2.id_team, game_datetime,
                                            team1_score, team2_score, team2.id_team, best_of,
                                            team1_pick, team2_pick, team1_removes, team2_removes, team1_rank,
                                            team2_rank)
            else:
                game = GameDAO().createGame(championship.id_championship, team1.id_team, team2.id_team, game_datetime,
                                            team1_score, team2_score, None, best_of,
                                            team1_pick, team2_pick, team1_removes, team2_removes, team1_rank,
                                            team2_rank)
        else:
            if team1_score > team2_score:
                GameDAO().updateGame(game, championship.id_championship, team1.id_team, team2.id_team, game_datetime,
                                     team1_score, team2_score, team1.id_team, best_of,
                                     team1_pick, team2_pick, team1_removes, team2_removes, team1_rank, team2_rank)
            elif team1_score < team2_score:
                GameDAO().updateGame(game, championship.id_championship, team1.id_team, team2.id_team, game_datetime,
                                     team1_score, team2_score, team2.id_team, best_of,
                                     team1_pick, team2_pick, team1_removes, team2_removes, team1_rank, team2_rank)
            else:
                GameDAO().updateGame(game, championship.id_championship, team1.id_team, team2.id_team, game_datetime,
                                     team1_score, team2_score, None, best_of,
                                     team1_pick, team2_pick, team1_removes, team2_removes, team1_rank, team2_rank)

        maps_array = self.create_map(game, maps_ct_tr_info_array, rounds_detail_informations, best_of)
        self.createPlayerMapStats(maps_array, team1, team2, frames)

    def create_map(self, game, maps_ct_tr_info_array, rounds_detail_informations, best_of):
        map_list = []
        maps = ""

        count2 = 4
        for i in range(0, best_of):
            maps = maps + maps_ct_tr_info_array[count2] + ";"
            count2 = count2 + 26
        maps = maps[:-1] if len(maps) > 0 else ""

        for aux in range(0, len(rounds_detail_informations)):

            map_name = maps.split(";")[aux]
            team1_tr_rounds = None
            team2_tr_rounds = None
            team1_ct_rounds = None
            team2_ct_rounds = None
            overtime_team1_rounds = None
            overtime_team2_rounds = None

            count = 1
            aux2 = 0
            # for tag in rounds_detail_informations[aux].contests:
            while aux2 < 10:
                tag = rounds_detail_informations[aux].contents[aux2].text
                attrsLen = len(rounds_detail_informations[aux].contents[aux2].attrs)
                attrsclas = 0 if attrsLen == 0 else len(rounds_detail_informations[aux].contents[aux2].attrs['class'])

                if attrsLen != 0 and attrsclas != 0 and (
                        rounds_detail_informations[aux].contents[aux2].attrs['class'][0] == "ct" or
                        rounds_detail_informations[aux].contents[aux2].attrs['class'][0] == "t"):
                    tag_class = rounds_detail_informations[aux].contents[aux2].attrs['class'][0]
                    if count % 2 != 0:
                        if tag_class == "ct":
                            team1_ct_rounds = int(tag)
                        if tag_class == "t":
                            team1_tr_rounds = int(tag)
                    if count % 2 == 0:
                        if tag_class == "ct":
                            team2_ct_rounds = int(tag)
                        if tag_class == "t":
                            team2_tr_rounds = int(tag)
                    count = count + 1
                aux2 = aux2 + 1

            if len(rounds_detail_informations[aux].contents) > 10:
                overtime_team1_rounds = int(rounds_detail_informations[aux].contents[11].text)
                overtime_team2_rounds = int(rounds_detail_informations[aux].contents[13].text)

            overtime_team1_rounds_ = overtime_team1_rounds if overtime_team1_rounds != None else 0
            overtime_team2_rounds_ = overtime_team2_rounds if overtime_team2_rounds != None else 0
            team1_score = team1_ct_rounds + team1_tr_rounds + overtime_team1_rounds_
            team2_score = team2_ct_rounds + team2_tr_rounds + overtime_team2_rounds_

            createdMap = MapDAO().getMapByGameId(game.id_game, map_name)
            if createdMap == None:
                createdMap = MapDAO().createMap(game.id_game, map_name, team1_tr_rounds, team2_tr_rounds,
                                                team1_ct_rounds, team2_ct_rounds, overtime_team1_rounds,
                                                overtime_team2_rounds, team1_score, team2_score)

            map_list.append(createdMap)

        return map_list

    def createPlayerMapStats(self, maps_array, team1, team2, frames):

        count = 0
        count_team1 = (count + 1) * 2
        count_team2 = (count + 1) * 2 + 1
        for count in range(0, len(maps_array)):
            actual_map = maps_array[count]
            for counter in range(1, 6):
                player_name = frames[count_team1].values[counter][:][0]
                result = re.search('\'(.*)\'', player_name)
                nick = result.group(1)

                item = frames[count_team1].values[counter][:][1]
                kills = int(item.split("-")[0])
                deaths = int(item.split("-")[1])
                plus_minos = int(frames[count_team1].values[counter][:][2])
                adr = float(frames[count_team1].values[counter][:][3])
                kast = float(frames[count_team1].values[counter][:][4][:-1])
                rating2 = float(frames[count_team1].values[counter][:][5])

                player = PlayerBuilder().createPastPlayer(team1, nick, player_name)
                PlayerMapStatsDAO().createPlayerMapStats(team1.id_team, actual_map.id_map_game, player.id_player, kills,
                                                         deaths, plus_minos, adr, kast, rating2)

                player_name = frames[count_team2].values[counter][:][0]
                result = re.search('\'(.*)\'', player_name)
                nick = result.group(1)

                item = frames[count_team2].values[counter][:][1]
                kills = int(item.split("-")[0])
                deaths = int(item.split("-")[1])
                plus_minos = int(frames[count_team2].values[counter][:][2])
                adr = float(frames[count_team2].values[counter][:][3])
                kast = float(frames[count_team2].values[counter][:][4][:-1])
                rating2 = float(frames[count_team2].values[counter][:][5])

                player = PlayerBuilder().createPastPlayer(team1, nick, player_name)
                PlayerMapStats = PlayerMapStatsDAO().getPlayerMapStatsByPlayerTeamAndMap(team2.id_team,
                                                                                         actual_map.id_map_game,
                                                                                         player.id_player)
                if PlayerMapStats == None:
                    PlayerMapStatsDAO().createPlayerMapStats(team2.id_team, actual_map.id_map_game, player.id_player,
                                                             kills, deaths, plus_minos, adr, kast, rating2)

            count = count + 1
            count_team1 = (count + 1) * 2
            count_team2 = (count + 1) * 2 + 1
