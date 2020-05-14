import config
from sqlalchemy import create_engine, text, and_
from sqlalchemy.orm import sessionmaker, subqueryload, selectinload
from model.player import Player
from model.player_team_property import PlayerTeamProperty
from dao.dao import DAO

class PlayerTeamPropertyDAO(DAO):

    def __init__(self):
        DAO.__init__(self)

    def commit(self, players):
        try:
            self.session.add_all(players)
            self.session.commit()
        except:
            self.session.rollback()
            raise

    def createPlayerProperty(self, team_id, player_id, date_hire, date_fire, isActive):

        c1 = PlayerTeamProperty(team_id, player_id, date_hire, date_fire, isActive)

        try:
            self.session.add(c1)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        return c1

    def getPlayerTeamPropertyByPlayerNameAndTeamCode(self, team_id, nick):
        try:
            item = self.session.query(PlayerTeamProperty).filter(and_(PlayerTeamProperty.player.has(Player.nick == nick), PlayerTeamProperty.id_team == team_id)).first()
        except:
            self.session.rollback()
            raise

        return item

    def listAllPlayerOfTeam(self, team_id):
        try:
            item = self.session.query(PlayerTeamProperty).options(selectinload(PlayerTeamProperty.player)).filter(PlayerTeamProperty.id_team == team_id).all()# from_statement(text(stringText)).all()
        except:
            self.session.rollback()
            raise

        return item