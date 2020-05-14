import config
from sqlalchemy import create_engine, text, and_
from sqlalchemy.orm import sessionmaker
from model.player import Player
from dao.dao import DAO

class PlayerDAO(DAO):

    def __init__(self):
        DAO.__init__(self)

    def createPlayer(self, name, nick, age):

        c1 = Player(name, nick, age)

        try:
            self.session.add(c1)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        return c1

    def updatePlayer(self, player, nick, name):

        player.name = name
        player.nick = nick

        try:
            self.session.add(player)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        return player

    def getPlayerByNick(self, nick):
        try:
            item = self.session.query(Player).filter(Player.nick == str(nick)).first()
        except:
            self.session.rollback()
            raise

        return item