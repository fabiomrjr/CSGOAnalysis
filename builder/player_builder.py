import pandas as pd
from datetime import datetime as dt

from dao.player_dao import PlayerDAO
from dao.player_team_property_dao import PlayerTeamPropertyDAO

position_field = 3
player_name_field = 1
player_number_field = 0

class PlayerBuilder:
    def __init__(self):
     pass

    def check(self, team_id, players_array):
        players = PlayerTeamPropertyDAO().listAllPlayerOfTeam(team_id)
        for contractedPlayers in players:
            contractedPlayers.date_fire = dt.now()
            contractedPlayers.active = False

        for i in players_array:
            if i == "":
                continue

            player = PlayerDAO().getPlayerByNick(i)
            if player == None:
                player = PlayerDAO().createPlayer("", i, 0)

            newPlayer = True
            for playerOld in players:
                if playerOld.player.nick == i:
                    playerOld.active = True
                    playerOld.date_fire = None
                    newPlayer = False
                    break

            if newPlayer == True:
                hiring_date = dt.now()
                PlayerTeamPropertyDAO().createPlayerProperty(team_id, player.id_player, hiring_date, None, True)

        PlayerTeamPropertyDAO().commit(players)
        #PlayerDAO().closeSession()
        #PlayerPropertyDAO().closeSession()

    def createPastPlayer(self, team, nick, name):

        player = PlayerDAO().getPlayerByNick(nick)
        if player == None:
            player = PlayerDAO().createPlayer(name, nick, 0)
        else:
            player = PlayerDAO().updatePlayer(player, nick, name)

        playerProperty = PlayerTeamPropertyDAO().getPlayerTeamPropertyByPlayerNameAndTeamCode(team.id_team, nick)
        if playerProperty == None:
            hiring_date = dt.now()
            PlayerTeamPropertyDAO().createPlayerProperty(team.id_team, player.id_player, hiring_date, None, True)

        return player