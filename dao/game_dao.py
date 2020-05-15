import pandas as pd
from sqlalchemy import create_engine, text, and_, or_
from sqlalchemy.orm import sessionmaker, subqueryload, selectinload, defaultload
from model.game import Game
from model.team import Team
from model.championship import Championship
from model.map import Map
from model.player_map_statistic import PlayerMapStatistic
from dao.dao import DAO

class GameDAO(DAO):

    def __init__(self):
        DAO.__init__(self)

    def createGame(self, championship_id, team1_id, team2_id, startDateTime, team1_score, team2_score, winner_team_id, best_of, team1_picks_maps, team2_picks_maps,
                 team1_removed_maps, team2_removed_maps, team1_rank, team2_rank):

        c1 = Game(championship_id, team1_id, team2_id, startDateTime, team1_score, team2_score, winner_team_id, best_of, team1_picks_maps, team2_picks_maps,
                 team1_removed_maps, team2_removed_maps, team1_rank, team2_rank)

        try:
            self.session.add(c1)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        return c1

    def updateGame(self, game, championship_id, team1_id, team2_id, startDateTime, team1_score, team2_score, winner_team_id, best_of, team1_picks_maps, team2_picks_maps,
                 team1_removed_maps, team2_removed_maps, team1_rank, team2_rank):

        game.update(championship_id, team1_id, team2_id, startDateTime, team1_score, team2_score, winner_team_id, best_of, team1_picks_maps, team2_picks_maps,
                 team1_removed_maps, team2_removed_maps, team1_rank, team2_rank)

        try:
            self.session.add(game)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        return game

    def getGameByTeamsAndDateTime(self, team1_id, team2_id, startDateTime):
        try:
            item = self.session.query(Game).filter(and_(Game.id_team1 == team1_id, Game.id_team2 == team2_id, Game.date == startDateTime.strftime("%Y-%m-%d %H:%M:00"))).first()
        except:
            self.session.rollback()
            raise

        return item

    def listLastGames(self):
        try:
            item = self.session.query(Game).order_by(Game.date.desc()).all()
        except:
            self.session.rollback()
            raise

        return item

    def listDataToAnalyser(self, team1_name, team2_name, maps0, maps1, maps2):
        try:

           #filter(and_(offense_plus_diffense.player.has(Player.id_player == int(player_id)),
           #            offense_plus_diffense.team.has(Team.id_team == int(team_id)),
           #            offense_plus_diffense.game.has(Game.id_game == int(game_id)))).first()

            dataframe = self.session.query(Game).options(selectinload(Game.team1), selectinload(Game.team2), selectinload(Game.maps)).\
                filter(and_(Game.best_of == 3, or_(Game.team1.has(Team.name == team1_name), Game.team2.has(Team.name == team1_name)),
                                                or_(Game.team1.has(Team.name == team2_name), Game.team2.has(Team.name == team2_name)),
                                                or_(Game.maps.any(Map.map_name == maps0), Game.maps.any(Map.map_name == maps1), Game.maps.any(Map.map_name == maps2)))).all()
        except:
            self.session.rollback()
            raise
        return dataframe

    def listTeamMapsGames(self, top, team_name):
        try:
            if top != None:
                dataframe = self.session.query(Game).options(selectinload(Game.team1), selectinload(Game.team2), selectinload(Game.maps)).\
                    filter(and_(Game.best_of == 3, or_(Game.team1.has(Team.name == team_name), Game.team2.has(Team.name == team_name)))).order_by(Game.date.desc()).limit(top).all()
            else:
                dataframe = self.session.query(Game).options(selectinload(Game.team1), selectinload(Game.team2), selectinload(Game.maps)).\
                    filter(and_(Game.best_of == 3, or_(Game.team1.has(Team.name == team_name), Game.team2.has(Team.name == team_name)))).all()
        except:
            self.session.rollback()
            raise
        return dataframe

    def listTeamGames(self, team1_name):
        try:
            dataframe = self.session.query(Game).options(selectinload(Game.team1), selectinload(Game.team2)).\
                filter(and_(Game.best_of == 3, or_(Game.team1.has(Team.name == team1_name), Game.team2.has(Team.name == team1_name)))).all()
        except:
            self.session.rollback()
            raise
        return dataframe

    def listTeamLastMapsGames(self, game_id, team_id, num_games):
        try:
            dataframe = self.session.query(Game).options(selectinload(Game.team1), selectinload(Game.team2), selectinload(Game.maps)).\
                filter(and_(Game.best_of == 3, Game.id_game < game_id, or_(Game.id_team1 == team_id, Game.id_team2 == team_id))).order_by(Game.date.desc()).limit(num_games).all()
        except:
            self.session.rollback()
            raise
        return dataframe

    def listTeamLastGamesWithPlayersStats(self, game_id, id_team1, num_games):
        try:
            #
            dataframe = self.session.query(Game).options(selectinload(Game.maps).selectinload(Map.player_map_stats)).join(Map).join(PlayerMapStatistic)\
                .filter(and_(Game.best_of == 3, Game.id_game < game_id, PlayerMapStatistic.id_team_player == id_team1)).order_by(Game.date.desc()).limit(int(num_games)).all()
            #print(literalquery(statement))
        except:
            self.session.rollback()
            raise
        return dataframe