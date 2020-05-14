import config
from sqlalchemy import create_engine, MetaData, Column, Integer, Float, Table, DateTime, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class db():
    def __init__(self):
        self.engine = create_engine(config.connectionString)
        self.meta = MetaData()

    def createTables(self):
        championship = Table(
            'championship', self.meta,
            Column('id_championship', Integer, primary_key=True, autoincrement=True),
            Column('name', String(100)),
            Column('start_date', DateTime),
            Column('award_money', Integer),
            Column('award', String(100))
        )

        player = Table(
            'player', self.meta,
            Column('id_player', Integer, primary_key=True, autoincrement=True),
            Column('name', String(60)),
            Column('nick', String(60)),
            Column('age', Integer)
        )

        team = Table(
            'team', self.meta,
            Column('id_team', Integer, primary_key=True, autoincrement=True),
            Column('name', String(50)),
            Column('homepage', String(100)),
            Column('actual_rank', Integer),
            Column('hltv_id', Integer)
        )

        game = Table(
            'game', self.meta,
            Column('id_game', Integer, primary_key=True, autoincrement=True),
            Column('id_championship', Integer),
            Column('id_team1', Integer),
            Column('id_team2', Integer),
            Column('id_winner_team', Integer),
            Column('id_predic_winner', Integer),
            Column('date', DateTime),
            Column('team1_score', Integer),
            Column('team2_score', Integer),
            Column('best_of', Integer),
            Column('team1_picks_maps', String(100)),
            Column('team2_picks_maps', String(100)),
            Column('team1_removed_maps', String(100)),
            Column('team2_removed_maps', String(100)),
            Column('team1_rank', Integer),
            Column('team2_rank', Integer)
        )

        map = Table(
            'map', self.meta,
            Column('id_map_game', Integer, primary_key=True, autoincrement=True),
            Column('id_game', Integer),
            Column('map_name', String(20)),
            Column('team1_tr_rounds', Integer),
            Column('team2_tr_rounds', Integer),
            Column('team1_ct_rounds', Integer),
            Column('team2_ct_rounds', Integer),
            Column('overtime_team1_rounds', Integer),
            Column('overtime_team2_rounds', Integer),
            Column('team1_total_rounds', Integer),
            Column('team2_total_rounds', Integer)
        )

        player_map_statistic = Table(
            'player_map_statistic', self.meta,
            Column('id_player_map_statistic', Integer, primary_key=True, autoincrement=True),
            Column('id_team_player', Integer),
            Column('id_map_game', Integer),
            Column('id_player', Integer),
            Column('kills', Integer),
            Column('deaths', Integer),
            Column('plus_minos', Integer),
            Column('adr', Float(precision=2)),
            Column('kast', Float(precision=2)),
            Column('rating2', Float(precision=2))
        )

        player_team_property = Table(
            'player_team_property', self.meta,
            Column('id_player_team_property', Integer, primary_key=True, autoincrement=True),
            Column('id_player', Integer),
            Column('id_team', Integer),
            Column('date_hire', DateTime),
            Column('date_fire', DateTime),
            Column('active', Boolean)
        )

        self.meta.create_all(self.engine)

        #column = Column('macdsub', Float(precision=8))
        #column_name = column.compile(dialect=self.engine.dialect)
        #column_type = column.type.compile(self.engine.dialect)
        #self.engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % ('candlesbyminute', column_name, column_type))
