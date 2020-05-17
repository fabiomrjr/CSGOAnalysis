import unittest
import tests.scenarios.games_scenario as gs
import analyser.team_indicators as team_indicators
from analyser.team_indicators import TeamIndicators

game1 = gs.build_game_with_3maps_winning_picks()
game2 = gs.build_game_with_2maps_dont_winning_picks()
game3 = gs.build_game_with_2maps_winning_picks_team1_and_team3()

class TeamIndicatorsTests(unittest.TestCase):

    def test_get_team_confidence_teams_winning_picks(self):
        team1_confidence = team_indicators.get_team_confidence(game1.id_team1, [game1])
        team2_confidence = team_indicators.get_team_confidence(game1.id_team2, [game1])

        self.assertEqual(team1_confidence, {'Mapa 1': {'Confidence': 100.0, 'Pick': 1, 'Win': 1}})
        self.assertEqual(team2_confidence, {'Mapa 2': {'Confidence': 100.0, 'Pick': 1, 'Win': 1}})

    def test_get_team_confidence_teams_no_winning_picks(self):
        team1_confidence = team_indicators.get_team_confidence(game2.id_team1, [game2])
        team2_confidence = team_indicators.get_team_confidence(game2.id_team2, [game2])

        self.assertEqual(team1_confidence, {'Mapa 1': {'Confidence': 0.0, 'Pick': 1, 'Win': 0}})
        self.assertEqual(team2_confidence, {'Mapa 2': {'Confidence': 0.0, 'Pick': 1, 'Win': 0}})

    def test_get_average_opp_rank_by_map(self):
        average_opp_rank_by_map_team1 = team_indicators.get_average_opp_rank_by_map([game2, game3], game2.id_team1)

        self.assertEqual(2.5, average_opp_rank_by_map_team1["Mapa 1"]["average"])
        self.assertEqual(2.5, average_opp_rank_by_map_team1["Mapa 2"]["average"])
        self.assertEqual(2.0, average_opp_rank_by_map_team1["Mapa 3"]["average"])
