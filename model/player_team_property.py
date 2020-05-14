from datetime import datetime as dt
from datetime import timedelta as td
from sqlalchemy import Column, Integer, Float, BigInteger, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import base
Base = declarative_base()

class PlayerTeamProperty(base):

    __tablename__ = 'player_team_property'
    __table_args__ = {'extend_existing': True}
    id_player_team_property = Column(Integer, primary_key=True, autoincrement=True)
    id_player = Column(Integer, ForeignKey('player.id_player'))
    id_team = Column(Integer, ForeignKey('team.id_team'))
    date_hire = Column(DateTime)
    date_fire = Column(DateTime)
    active = Column(Boolean)

    player = relationship("Player", lazy="noload", foreign_keys="PlayerTeamProperty.id_player", backref="player_property_player")
    team = relationship("Team", lazy="noload", foreign_keys="PlayerTeamProperty.id_team", backref="team_player_property")

    def __init__(self):
        pass

    def __init__(self, team_id, player_id, date_hire, date_fire, isActive):
        self.id_player = player_id
        self.id_team = team_id
        self.date_hire = date_hire
        self.date_fire = date_fire
        self.active = isActive

    def json(self):
       return {'Need to be implemented' + 'date': self.date.strftime('%b %d %Y %I:%M%p')}\
