import config
from sqlalchemy import create_engine, text, or_, and_
from sqlalchemy.orm import sessionmaker
from model.team import Team
from dao.dao import DAO

class TeamDAO(DAO):
    def __init__(self):
        DAO.__init__(self)

    def createTeam(self, name, homepage, actual_rank, hltv_id):
        c1 = Team(name, homepage, actual_rank, hltv_id)

        try:
            self.session.add(c1)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        return c1

    def updateTeam(self, team, name, homepage, actual_rank, hltv_id):
        team.name = name
        if homepage != team.homepage:
            team.homepage = homepage
        if actual_rank != team.actual_rank:
            team.actual_rank = actual_rank
        team.hltv_id = hltv_id

        try:
            self.session.add(team)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        return team

    def getTeamByLikeName(self, name):
        try:
            item = self.session.query(Team).filter(Team.name.like("%" + name + "%")).first()
        except:
            self.session.rollback()
            raise

        return item

    def listTeamsWithHomePage(self):
        try:
            item = self.session.query(Team).filter(and_(Team.homepage.isnot(None), Team.homepage != "")).all()
        except:
            self.session.rollback()
            raise

        return item