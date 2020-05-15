from datetime import datetime as dt
from datetime import timedelta as td

from sqlalchemy import Column, Integer, Float, BigInteger, DateTime, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
#from base import base
from model.map import Map
from db import base
from sqlalchemy.orm import relationship

#Base = declarative_base()

class Game(base):

    __tablename__ = 'game'
    __table_args__ = {'extend_existing': True}
    id_game = Column(Integer, primary_key=True, autoincrement=True)
    id_championship = Column(Integer, ForeignKey("championship.id_championship"))
    id_team1 = Column(Integer, ForeignKey("team.id_team"))
    id_team2 = Column(Integer, ForeignKey("team.id_team"))
    id_winner_team = Column(Integer, ForeignKey("team.id_team"), nullable=True)
    id_predic_winner = Column(Integer, ForeignKey("team.id_team"), nullable=True)
    date = Column(DateTime)
    team1_score = Column(Integer)
    team2_score = Column(Integer)
    best_of = Column(Integer)
    team1_picks_maps = Column(String(100))
    team2_picks_maps = Column(String(100))
    team1_removed_maps = Column(String(100))
    team2_removed_maps = Column(String(100))
    team1_rank = Column(Integer)
    team2_rank = Column(Integer)

    championship_ = relationship("Championship", lazy="noload", foreign_keys="Game.id_championship", backref="championship_of_game")
    maps = relationship("Map", lazy="noload", foreign_keys="Map.id_game", backref="maps_of_game")

    team1 = relationship("Team", lazy="noload", foreign_keys="Game.id_team1", backref="games_as_team1")
    team2 = relationship("Team", lazy="noload", foreign_keys="Game.id_team2", backref="games_as_team2")
    winner_team = relationship("Team", lazy="noload", foreign_keys="Game.id_winner_team", backref="games_winner")
    pred_winner_team = relationship("Team", lazy="noload", foreign_keys="Game.id_predic_winner", backref="games_pred_winner")

    def __init__(self):
        pass

    def __init__(self, championship_id, team1_id, team2_id, startDateTime, team1_score, team2_score, winner_team_id, best_of, team1_picks_maps, team2_picks_maps,
                 team1_removed_maps, team2_removed_maps, team1_rank, team2_rank):
        self.id_championship = championship_id
        self.id_team1 = team1_id
        self.id_team2 = team2_id
        self.team1_score = team1_score
        self.team2_score = team2_score
        self.date = startDateTime
        self.id_winner_team = winner_team_id
        self.best_of = best_of
        self.team1_picks_maps = team1_picks_maps
        self.team2_picks_maps = team2_picks_maps
        self.team1_removed_maps = team1_removed_maps
        self.team2_removed_maps = team2_removed_maps
        self.team1_rank = team1_rank
        self.team2_rank = team2_rank

    def update(self, championship_id, team1_id, team2_id, startdateTime, team1_score, team2_score, winner_team_id, best_of, team1_picks_maps, team2_picks_maps,
               team1_removed_maps, team2_removed_maps, team1_rank, team2_rank):
        self.id_championship = championship_id
        self.id_team1 = team1_id
        self.id_team2 = team2_id
        self.team1_score = team1_score
        self.team2_score = team2_score
        self.date = startdateTime
        self.id_winner_team = winner_team_id
        self.best_of = best_of
        self.team1_picks_maps = team1_picks_maps
        self.team2_picks_maps = team2_picks_maps
        self.team1_removed_maps = team1_removed_maps
        self.team2_removed_maps = team2_removed_maps
        self.team1_rank = team1_rank
        self.team2_rank = team2_rank

    def json(self):
       return {'Need to be implemented' + 'date': self.date.strftime('%b %d %Y %I:%M%p')}\
