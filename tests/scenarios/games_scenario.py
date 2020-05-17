from model.game import Game
from model.map import Map
from model.team import Team

team1 = Team(1, "Team1", "", 1, 0)
team2 = Team(2, "Team2", "", 2, 0)
team3 = Team(3, "Team3", "", 3, 0)


def build_game_with_3maps_winning_picks():
    game = Game(None, team1.id_team, team2.id_team, None, 2, 1, team1.id_team, 3, "Mapa 1", "Mapa 2", "", "",
                "Mapa 3", team1.actual_rank, team2.actual_rank)
    game.team1 = team1
    game.team2 = team2
    map1 = Map(game.id_game, "Mapa 1", 9, 6, 6, 2, 0, 0, 16, 8)
    map2 = Map(game.id_game, "Mapa 2", 7, 8, 6, 8, 0, 0, 13, 16)
    map3 = Map(game.id_game, "Mapa 3", 7, 8, 6, 8, 0, 0, 13, 16)

    game.maps = [map1, map2, map3]

    return game


def build_game_with_2maps_dont_winning_picks():
    game = Game(None, team1.id_team, team2.id_team, None, 2, 1, team1.id_team, 3, "Mapa 1", "Mapa 2", "", "",
                "Mapa 3", team1.actual_rank, team2.actual_rank)
    game.team1 = team1
    game.team2 = team2
    map1 = Map(game.id_game, "Mapa 1", 6, 9, 2, 6, 0, 0, 8, 16)
    map2 = Map(game.id_game, "Mapa 2", 8, 7, 8, 4, 0, 0, 16, 11)
    map3 = Map(game.id_game, "Mapa 3", 7, 8, 6, 8, 0, 0, 13, 16)

    game.maps = [map1, map2, map3]

    return game

def build_game_with_2maps_winning_picks_team1_and_team3():
    game = Game(None, team1.id_team, team3.id_team, None, 2, 1, team1.id_team, 3, "Mapa 1", "Mapa 2", "", "",
                "Mapa 3", team1.actual_rank, team3.actual_rank)
    game.team1 = team1
    game.team2 = team3
    map1 = Map(game.id_game, "Mapa 1", 9, 6, 7, 6, 0, 0, 16, 12)
    map2 = Map(game.id_game, "Mapa 2", 8, 7, 8, 4, 0, 0, 16, 11)

    game.maps = [map1, map2]

    return game
