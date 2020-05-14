import config
from sqlalchemy import create_engine, text, and_
from sqlalchemy.orm import sessionmaker, with_polymorphic, subqueryload
from model.player_map_statistic import PlayerMapStatistic
from dao.dao import DAO

class PlayerMapStatsDAO(DAO):

    def __init__(self):
        DAO.__init__(self)

    def createPlayerMapStats(self, team_id, map_id, player_id, kills, deaths, plus_minos, adr, kast, rating2):

        c1 = PlayerMapStatistic(team_id, map_id, player_id, kills, deaths, plus_minos, adr, kast, rating2)

        try:
            self.session.add(c1)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        return c1

    def getPlayerMapStatsByPlayerTeamAndMap(self, team_id, map_id, player_id):
        try:
            item = self.session.query(PlayerMapStatistic).filter(and_(PlayerMapStatistic.id_team_player == int(team_id), PlayerMapStatistic.id_map_game == int(map_id), PlayerMapStatistic.id_player == int(player_id))).first()
        except:
            self.session.rollback()
            raise

        return item