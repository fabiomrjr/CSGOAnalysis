from datetime import datetime as dt
from datetime import timedelta as td
from sqlalchemy import Column, Integer, Float, BigInteger, DateTime, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import base
from .player import Player
Base = declarative_base()

class PlayerMapStatistic(base):

    __tablename__ = 'player_map_statistic'
    __table_args__ = {'extend_existing': True}
    id_player_map_statistic = Column(Integer, primary_key=True, autoincrement=True)
    id_team_player = Column(Integer, ForeignKey('team.id_team'))
    id_map_game = Column(Integer, ForeignKey('map.id_map_game'))
    id_player = Column(Integer, ForeignKey('player.id_player'))
    kills = Column(Integer)
    deaths = Column(Integer)
    plus_minos = Column(Integer)
    adr = Column(Float(precision=2))
    kast = Column(Float(precision=2))
    rating2 = Column(Float(precision=2))

    player_of_stats = relationship("Player", lazy="noload",foreign_keys="PlayerMapStatistic.id_player", backref="player_stats")
    team_of_stats = relationship("Team", lazy="noload", foreign_keys="PlayerMapStatistic.id_team_player", backref="team_stats")
    map_of_stats = relationship("Map", lazy="noload", foreign_keys="PlayerMapStatistic.id_map_game", backref="map_stats")

    def __init__(self):
        pass

    def __init__(self, team_id, map_id, player_id, kills, deaths, plus_minos, adr, kast, rating2):
        self.id_team_player = team_id
        self.id_map_game = map_id
        self.kills = kills
        self.deaths = deaths
        self.plus_minos = plus_minos
        self.adr = adr
        self.kast = kast
        self.rating2 = rating2
        self.id_player = player_id

    def json(self):
       return {'Need to be implemented' + 'date': self.date.strftime('%b %d %Y %I:%M%p')}\
