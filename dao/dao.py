import config
from db import db
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

class DAO:

    engine = None
    session = None

    def __init__(self):
        if self.session == None:
            self.engine = create_engine(config.connectionString)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            self.session.expire_on_commit = False

    def __del__(self):
        self.session.close()
