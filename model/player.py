from datetime import datetime as dt
from datetime import timedelta as td
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import base
from model.player_team_property import PlayerTeamProperty
#Base = declarative_base()

class Player(base):

    __tablename__ = 'player'
    __table_args__ = {'extend_existing': True}
    id_player = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60))
    nick = Column(String(60))
    age = Column(Integer)

    player_maps_stats = relationship("PlayerMapStatistic", lazy="noload", foreign_keys="PlayerMapStatistic.id_player", backref="stats_player")
    properties = relationship("PlayerTeamProperty", lazy="noload", foreign_keys="PlayerTeamProperty.id_player", backref="property_player")

    def __init__(self):
        pass

    def __init__(self, name, nick, age):
        self.name = name
        self.nick = nick
        self.age = age

    def json(self):
       return {'Need to be implemented' + 'date': self.date.strftime('%b %d %Y %I:%M%p')}\
