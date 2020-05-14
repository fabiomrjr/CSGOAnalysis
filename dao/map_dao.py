import config
from sqlalchemy import create_engine, text, and_
from sqlalchemy.orm import sessionmaker, subqueryload, selectinload
from model.map import Map
from dao.dao import DAO

class MapDAO(DAO):

    def __init__(self):
        DAO.__init__(self)

    def createMap(self, game_id, map_name, team1_tr_rounds, team2_tr_rounds, team1_ct_rounds, team2_ct_rounds, overtime_team1_rounds, overtime_team2_rounds, team1_total_rounds, team2_total_rounds):

        c1 = Map(game_id, map_name, team1_tr_rounds, team2_tr_rounds, team1_ct_rounds, team2_ct_rounds, overtime_team1_rounds, overtime_team2_rounds, team1_total_rounds, team2_total_rounds)

        try:
            self.session.add(c1)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        return c1

    def getMapByGameId(self, game_id, map_name):
        try:
            item = self.session.query(Map).filter(and_(Map.id_game == int(game_id), Map.map_name == map_name)).first()
        except:
            self.session.rollback()
            raise

        return item