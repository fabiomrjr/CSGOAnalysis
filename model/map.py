from datetime import datetime as dt
from datetime import timedelta as td
#from ..model.team import Team
from sqlalchemy import Column, Integer, Float, BigInteger, DateTime, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from model.player_map_statistic import PlayerMapStatistic
from db import base
from sqlalchemy.orm import relationship

#Base = declarative_base()

class Map(base):

    __tablename__ = 'map'
    __table_args__ = {'extend_existing': True}
    id_map_game = Column(Integer, primary_key=True, autoincrement=True)
    id_game = Column(Integer, ForeignKey('game.id_game'))
    map_name = Column(String(20))
    team1_total_rounds = Column(Integer)
    team2_total_rounds = Column(Integer)
    team1_tr_rounds = Column(Integer)
    team2_tr_rounds = Column(Integer)
    team1_ct_rounds = Column(Integer)
    team2_ct_rounds = Column(Integer)
    overtime_team1_rounds = Column(Integer)
    overtime_team2_rounds = Column(Integer)

    map_of_game = relationship("Game", lazy="noload", foreign_keys="Map.id_game", backref="game_of_map")
    player_map_stats = relationship("PlayerMapStatistic", lazy="noload", foreign_keys="PlayerMapStatistic.id_map_game", backref="playerstats_map")

    def __init__(self):
        pass


    def __init__(self, game_id, map_name, team1_tr_rounds, team2_tr_rounds, team1_ct_rounds, team2_ct_rounds, overtime_team1_rounds, overtime_team2_rounds, team1_total_rounds, team2_total_rounds):
        self.id_game = game_id
        self.map_name = map_name
        self.team1_tr_rounds = team1_tr_rounds
        self.team2_tr_rounds = team2_tr_rounds
        self.team1_ct_rounds = team1_ct_rounds
        self.team2_ct_rounds = team2_ct_rounds
        self.overtime_team1_rounds = overtime_team1_rounds
        self.overtime_team2_rounds = overtime_team2_rounds
        self.team2_total_rounds = team2_total_rounds
        self.team1_total_rounds = team1_total_rounds

    def json(self):
       return {'Need to be implemented' + 'date': self.date.strftime('%b %d %Y %I:%M%p')}\
