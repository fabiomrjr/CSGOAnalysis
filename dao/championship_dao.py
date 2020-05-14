from sqlalchemy import and_
from model.championship import Championship
from dao.dao import DAO
from sqlalchemy import and_
from model.championship import Championship

class ChampionshipDAO(DAO):

    def __init__(self):
        DAO.__init__(self)

    def createChampionship(self, name, start_date, award_money, award):

        c1 = Championship(name, start_date, award_money, award)

        try:
            self.session.add(c1)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        return c1

    def getChampionshipByNameAndStartDate(self, name, start_date):
        try:
            if start_date == None:
                item = self.session.query(Championship).filter(Championship.name == str(name)).first()
            else:
                item = self.session.query(Championship).filter(and_(Championship.name == str(name), Championship.start_date == start_date.strftime("%Y-%m-%d %H:%M:00"))).first()
        except:
            self.session.rollback()
            raise

        return item