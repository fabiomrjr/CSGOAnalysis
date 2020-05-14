from datetime import datetime as dt
from datetime import timedelta as td
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import base
#Base = declarative_base()

class Championship(base):

    __tablename__ = 'championship'
    __table_args__ = {'extend_existing': True}
    id_championship = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    start_date = Column(DateTime)
    award_money = Column(Integer)
    award = Column(String(100))

    games = relationship("Game", lazy="noload", foreign_keys="Game.id_championship", backref="games_of_championship")

    def __init__(self):
        pass

    def __init__(self, name, start_date, award_money, award):
        self.name = name
        self.start_date = start_date
        self.award_money = award_money
        self.award = award

    def json(self):
       return {'Need to be implemented' + 'date': self.date.strftime('%b %d %Y %I:%M%p')}\
