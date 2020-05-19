from datetime import datetime as dt
from datetime import timedelta as td
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import base

#Base = declarative_base()

class Team(base):

    __tablename__ = 'team'
    __table_args__ = {'extend_existing': True}
    id_team = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    homepage = Column(String(100))
    actual_rank = Column(Integer)
    hltv_id = Column(Integer)

    #children = relationship("player", secondary=association_table)
    #player_properties_team = relationship("PlayerTeamProperty", lazy="noload", foreign_keys="PlayerTeamProperty.id_team", backref="property_team_player")

    t_pred_winner = relationship("Game", lazy="noload", foreign_keys="Game.id_predic_winner", back_populates="pred_winner_team")
    t_winner = relationship("Game", lazy="noload", foreign_keys="Game.id_winner_team", back_populates="winner_team")
    t_games_as_team1 = relationship("Game", lazy="noload", foreign_keys="Game.id_team1", back_populates="team1")
    t_games_at_team2 = relationship("Game", lazy="noload", foreign_keys="Game.id_team2", back_populates="team2")

    def __init__(self, id=None, name=None, homepage=None, actual_rank=None, hltv_id=None):
        self.id_team = id
        self.actual_rank = actual_rank
        self.name = name
        self.homepage = homepage
        self.hltv_id = hltv_id



