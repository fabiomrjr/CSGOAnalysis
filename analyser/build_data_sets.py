import pandas as pd
import analyser.team_indicators as team_indicators

from dao.game_dao import GameDAO
from analyser.team_indicators import TeamIndicators
from dao.player_map_stats_dao import PlayerMapStatsDAO

number_maps_to_consider = 30


class BuildDataSet:
    def __init__(self):
        pass

    def get_data_set(self):
        # df = pd.DataFrame(columns=['Team1Confidence', 'Team1WinPercentage', 'Team1Rank', 'Team1AverageOppRank',
        #                           'Team1PlayersPlusMinos', 'Team1RoundsPlusMinos',
        #                           'Team2Confidence', 'Team2WinPercentage', 'Team2Rank', 'Team2AverageOppRank',
        #                           'Team2PlayersPlusMinos', 'Team2RoundsPlusMinos', 'Team1Winner'])

        df = pd.DataFrame(columns=['Map1', 'Map2', 'Map3', 'Team1Rank', 'Team2Rank',
                                   'Team1WinPercentageMirage', 'Team1WinPercentageDust2', 'Team1WinPercentageNuke',
                                   'Team1WinPercentageOverpass', 'Team1WinPercentageInferno',
                                   'Team1WinPercentageVertigo', 'Team1WinPercentageTrain', 'Team1WinPercentageCache',
                                   'Team2WinPercentageMirage', 'Team2WinPercentageDust2', 'Team2WinPercentageNuke',
                                   'Team2WinPercentageOverpass', 'Team2WinPercentageInferno',
                                   'Team2WinPercentageVertigo', 'Team2WinPercentageTrain', 'Team2WinPercentageCache',

                                   'Team1ConfidencePickMirage', 'Team1ConfidencePickDust2', 'Team1ConfidencePickNuke',
                                   'Team1ConfidencePickOverpass', 'Team1ConfidencePickInferno',
                                   'Team1ConfidencePickVertigo', 'Team1ConfidencePickTrain', 'Team1ConfidencePickCache',
                                   'Team2ConfidencePickMirage', 'Team2ConfidencePickDust2', 'Team2ConfidencePickNuke',
                                   'Team2ConfidencePickOverpass', 'Team2ConfidencePickInferno',
                                   'Team2ConfidencePickVertigo', 'Team2ConfidencePickTrain', 'Team2ConfidencePickCache',

                                   'Team1AverageOppRankMirage', 'Team1AverageOppRankDust2', 'Team1AverageOppRankNuke',
                                   'Team1AverageOppRankOverpass', 'Team1AverageOppRankInferno',
                                   'Team1AverageOppRankVertigo', 'Team1AverageOppRankTrain', 'Team1AverageOppRankCache',
                                   'Team2AverageOppRankMirage', 'Team2AverageOppRankDust2', 'Team2AverageOppRankNuke',
                                   'Team2AverageOppRankOverpass', 'Team2AverageOppRankInferno',
                                   'Team2AverageOppRankVertigo', 'Team2AverageOppRankTrain', 'Team2AverageOppRankCache',

                                   'Team1PlayersPlusMinosMirage', 'Team1PlayersPlusMinosDust2',
                                   'Team1PlayersPlusMinosNuke', 'Team1PlayersPlusMinosOverpass',
                                   'Team1PlayersPlusMinosInferno',
                                   'Team1PlayersPlusMinosVertigo', 'Team1PlayersPlusMinosTrain',
                                   'Team1PlayersPlusMinosCache',
                                   'Team2PlayersPlusMinosMirage', 'Team2PlayersPlusMinosDust2',
                                   'Team2PlayersPlusMinosNuke', 'Team2PlayersPlusMinosOverpass',
                                   'Team2PlayersPlusMinosInferno',
                                   'Team2PlayersPlusMinosVertigo', 'Team2PlayersPlusMinosTrain',
                                   'Team2PlayersPlusMinosCache',

                                   'Team1RoundsPlusMinosMirage', 'Team1RoundsPlusMinosDust2',
                                   'Team1RoundsPlusMinosNuke', 'Team1RoundsPlusMinosOverpass',
                                   'Team1RoundsPlusMinosInferno',
                                   'Team1RoundsPlusMinosVertigo', 'Team1RoundsPlusMinosTrain',
                                   'Team1RoundsPlusMinosCache',
                                   'Team2RoundsPlusMinosMirage', 'Team2RoundsPlusMinosDust2',
                                   'Team2RoundsPlusMinosNuke', 'Team2RoundsPlusMinosOverpass',
                                   'Team2RoundsPlusMinosInferno',
                                   'Team2RoundsPlusMinosVertigo', 'Team2RoundsPlusMinosTrain',
                                   'Team2RoundsPlusMinosCache',
                                   'Team1Winner'])

        games = GameDAO().list_last_games()
        # counter = 0
        for game in games:
            # if counter == 500:
            #    break

            team1_last_10_games = GameDAO().listTeamLastMapsGames(game.id_game, game.id_team1, number_maps_to_consider)
            team2_last_10_games = GameDAO().listTeamLastMapsGames(game.id_game, game.id_team2, number_maps_to_consider)

            if len(team1_last_10_games) < number_maps_to_consider or len(team2_last_10_games) < number_maps_to_consider:
                continue

            team1_confidence = team_indicators.get_team_confidence(team1_last_10_games, game.id_team1)
            team2_confidence = team_indicators.get_team_confidence(team2_last_10_games, game.id_team2)

            win_percentage_team1 = TeamIndicators().win_lost_percentage_by_rank_window_and_maps(game.id_team1,
                                                                                                team1_last_10_games)
            win_percentage_team2 = TeamIndicators().win_lost_percentage_by_rank_window_and_maps(game.id_team2,
                                                                                                team2_last_10_games)

            win_percentage_team1_by_map = TeamIndicators().get_win_percentage_by_maps_and_opp_rank_dictionary(
                win_percentage_team1, game.team2_rank,
                ["Dust2", "Inferno", "Overpass", "Vertigo", "Nuke", "Mirage", "Train", "Cache"])
            win_percentage_team2_by_map = TeamIndicators().get_win_percentage_by_maps_and_opp_rank_dictionary(
                win_percentage_team2, game.team1_rank,
                ["Dust2", "Inferno", "Overpass", "Vertigo", "Nuke", "Mirage", "Train", "Cache"])

            average_opp_rank_team1 = team_indicators.get_average_opp_rank_by_map(team1_last_10_games, game.id_team1)
            average_opp_rank_team2 = team_indicators.get_average_opp_rank_by_map(team2_last_10_games, game.id_team2)

            plus_minos_rounds_team1 = team_indicators.get_plus_minos_rounds_team(team1_last_10_games, game.id_team1)
            plus_minos_rounds_team2 = team_indicators.get_plus_minos_rounds_team(team2_last_10_games, game.id_team2)

            gamesWithTeam1PlayersStats = GameDAO().listTeamLastGamesWithPlayersStats(game.id_game, game.id_team1,
                                                                                     15 * number_maps_to_consider)
            gamesWithTeam2PlayersStats = GameDAO().listTeamLastGamesWithPlayersStats(game.id_game, game.id_team2,
                                                                                     15 * number_maps_to_consider)

            plus_minos_players_team1 = team_indicators.get_plus_minos_players_team(gamesWithTeam1PlayersStats)
            plus_minos_players_team2 = team_indicators.get_plus_minos_players_team(gamesWithTeam2PlayersStats)

            df.loc[counter, 'Team1Rank'] = game.team1_rank
            df.loc[counter, 'Team2Rank'] = game.team2_rank
            df.loc[counter, 'Map1'] = game.team1_picks_maps
            df.loc[counter, 'Map2'] = game.team2_picks_maps
            df.loc[counter, 'Map3'] = game.map_left

            df.loc[counter, 'Team1WinPercentageMirage'] = win_percentage_team1_by_map["Mirage"]
            df.loc[counter, 'Team1WinPercentageDust2'] = win_percentage_team1_by_map["Dust2"]
            df.loc[counter, 'Team1WinPercentageNuke'] = win_percentage_team1_by_map["Nuke"]
            df.loc[counter, 'Team1WinPercentageOverpass'] = win_percentage_team1_by_map["Overpass"]
            df.loc[counter, 'Team1WinPercentageInferno'] = win_percentage_team1_by_map["Inferno"]
            df.loc[counter, 'Team1WinPercentageVertigo'] = win_percentage_team1_by_map["Vertigo"]
            df.loc[counter, 'Team1WinPercentageTrain'] = win_percentage_team1_by_map["Train"]
            df.loc[counter, 'Team1WinPercentageCache'] = win_percentage_team1_by_map["Cache"]
            df.loc[counter, 'Team2WinPercentageMirage'] = win_percentage_team2_by_map["Mirage"]
            df.loc[counter, 'Team2WinPercentageDust2'] = win_percentage_team2_by_map["Dust2"]
            df.loc[counter, 'Team2WinPercentageNuke'] = win_percentage_team2_by_map["Nuke"]
            df.loc[counter, 'Team2WinPercentageOverpass'] = win_percentage_team2_by_map["Overpass"]
            df.loc[counter, 'Team2WinPercentageInferno'] = win_percentage_team2_by_map["Inferno"]
            df.loc[counter, 'Team2WinPercentageVertigo'] = win_percentage_team2_by_map["Vertigo"]
            df.loc[counter, 'Team2WinPercentageTrain'] = win_percentage_team2_by_map["Train"]
            df.loc[counter, 'Team2WinPercentageCache'] = win_percentage_team2_by_map["Cache"]

            df.loc[counter, 'Team1ConfidencePickMirage'] = team1_confidence["Mirage"]["Confidence"]
            df.loc[counter, 'Team1ConfidencePickDust2'] = team1_confidence["Dust2"]["Confidence"]
            df.loc[counter, 'Team1ConfidencePickNuke'] = team1_confidence["Nuke"]["Confidence"]
            df.loc[counter, 'Team1ConfidencePickOverpass'] = team1_confidence["Overpass"]["Confidence"]
            df.loc[counter, 'Team1ConfidencePickInferno'] = team1_confidence["Inferno"]["Confidence"]
            df.loc[counter, 'Team1ConfidencePickVertigo'] = team1_confidence["Vertigo"]["Confidence"]
            df.loc[counter, 'Team1ConfidencePickTrain'] = team1_confidence["Train"]["Confidence"]
            df.loc[counter, 'Team1ConfidencePickCache'] = team1_confidence["Cache"]["Confidence"]
            df.loc[counter, 'Team2ConfidencePickMirage'] = team2_confidence["Mirage"]["Confidence"]
            df.loc[counter, 'Team2ConfidencePickDust2'] = team2_confidence["Dust2"]["Confidence"]
            df.loc[counter, 'Team2ConfidencePickNuke'] = team2_confidence["Nuke"]["Confidence"]
            df.loc[counter, 'Team2ConfidencePickOverpass'] = team2_confidence["Overpass"]["Confidence"]
            df.loc[counter, 'Team2ConfidencePickInferno'] = team2_confidence["Inferno"]["Confidence"]
            df.loc[counter, 'Team2ConfidencePickVertigo'] = team2_confidence["Vertigo"]["Confidence"]
            df.loc[counter, 'Team2ConfidencePickTrain'] = team2_confidence["Train"]["Confidence"]
            df.loc[counter, 'Team2ConfidencePickCache'] = team2_confidence["Cache"]["Confidence"]

            df.loc[counter, 'Team1AverageOppRankMirage'] = average_opp_rank_team1["Mirage"]["average"] if \
                average_opp_rank_team1.get("Mirage") is not None else 0.0
            df.loc[counter, 'Team1AverageOppRankDust2'] = average_opp_rank_team1["Dust2"]["average"] if \
                average_opp_rank_team1.get("Dust2") is not None else 0.0
            df.loc[counter, 'Team1AverageOppRankNuke'] = average_opp_rank_team1["Nuke"]["average"] if \
                average_opp_rank_team1.get("Nuke") is not None else 0.0
            df.loc[counter, 'Team1AverageOppRankOverpass'] = average_opp_rank_team1["Overpass"]["average"] if \
                average_opp_rank_team1.get("Overpass") is not None else 0.0
            df.loc[counter, 'Team1AverageOppRankInferno'] = average_opp_rank_team1["Inferno"]["average"] if \
                average_opp_rank_team1.get("Inferno") is not None else 0.0
            df.loc[counter, 'Team1AverageOppRankVertigo'] = average_opp_rank_team1["Vertigo"]["average"] if \
                average_opp_rank_team1.get("Vertigo") is not None else 0.0
            df.loc[counter, 'Team1AverageOppRankTrain'] = average_opp_rank_team1["Train"]["average"] if \
                average_opp_rank_team1.get("Train") is not None else 0.0
            df.loc[counter, 'Team1AverageOppRankCache'] = average_opp_rank_team1["Cache"]["average"] if \
                average_opp_rank_team1.get("Cache") is not None else 0.0
            df.loc[counter, 'Team2AverageOppRankMirage'] = average_opp_rank_team2["Mirage"]["average"] if \
                average_opp_rank_team2.get("Mirage") is not None else 0.0
            df.loc[counter, 'Team2AverageOppRankDust2'] = average_opp_rank_team2["Dust2"]["average"] if \
                average_opp_rank_team2.get("Dust2") is not None else 0.0
            df.loc[counter, 'Team2AverageOppRankNuke'] = average_opp_rank_team2["Nuke"]["average"] if \
                average_opp_rank_team2.get("Nuke") is not None else 0.0
            df.loc[counter, 'Team2AverageOppRankOverpass'] = average_opp_rank_team2["Overpass"]["average"] if \
                average_opp_rank_team2.get("Overpass") is not None else 0.0
            df.loc[counter, 'Team2AverageOppRankInferno'] = average_opp_rank_team2["Inferno"]["average"] if \
                average_opp_rank_team2.get("Inferno") is not None else 0.0
            df.loc[counter, 'Team2AverageOppRankVertigo'] = average_opp_rank_team2["Vertigo"]["average"] if \
                average_opp_rank_team2.get("Vertigo") is not None else 0.0
            df.loc[counter, 'Team2AverageOppRankTrain'] = average_opp_rank_team2["Train"]["average"] if \
                average_opp_rank_team2.get("Train") is not None else 0.0
            df.loc[counter, 'Team2AverageOppRankCache'] = average_opp_rank_team2["Cache"]["average"] if \
                average_opp_rank_team2.get("Cache") is not None else 0.0

            df.loc[counter, 'Team1PlayersPlusMinosMirage'] = plus_minos_players_team1["Mirage"]["plusMinosPlayers"]
            df.loc[counter, 'Team1PlayersPlusMinosDust2'] = plus_minos_players_team1["Dust2"]["plusMinosPlayers"]
            df.loc[counter, 'Team1PlayersPlusMinosNuke'] = plus_minos_players_team1["Nuke"]["plusMinosPlayers"]
            df.loc[counter, 'Team1PlayersPlusMinosOverpass'] = plus_minos_players_team1["Overpass"]["plusMinosPlayers"]
            df.loc[counter, 'Team1PlayersPlusMinosInferno'] = plus_minos_players_team1["Inferno"]["plusMinosPlayers"]
            df.loc[counter, 'Team1PlayersPlusMinosVertigo'] = plus_minos_players_team1["Vertigo"]["plusMinosPlayers"]
            df.loc[counter, 'Team1PlayersPlusMinosTrain'] = plus_minos_players_team1["Train"]["plusMinosPlayers"]
            df.loc[counter, 'Team1PlayersPlusMinosCache'] = plus_minos_players_team1["Cache"]["plusMinosPlayers"]
            df.loc[counter, 'Team2PlayersPlusMinosMirage'] = plus_minos_players_team2["Mirage"]["plusMinosPlayers"]
            df.loc[counter, 'Team2PlayersPlusMinosDust2'] = plus_minos_players_team2["Dust2"]["plusMinosPlayers"]
            df.loc[counter, 'Team2PlayersPlusMinosNuke'] = plus_minos_players_team2["Nuke"]["plusMinosPlayers"]
            df.loc[counter, 'Team2PlayersPlusMinosOverpass'] = plus_minos_players_team2["Overpass"]["plusMinosPlayers"]
            df.loc[counter, 'Team2PlayersPlusMinosInferno'] = plus_minos_players_team2["Inferno"]["plusMinosPlayers"]
            df.loc[counter, 'Team2PlayersPlusMinosVertigo'] = plus_minos_players_team2["Vertigo"]["plusMinosPlayers"]
            df.loc[counter, 'Team2PlayersPlusMinosTrain'] = plus_minos_players_team2["Train"]["plusMinosPlayers"]
            df.loc[counter, 'Team2PlayersPlusMinosCache'] = plus_minos_players_team2["Cache"]["plusMinosPlayers"]

            df.loc[counter, 'Team1RoundsPlusMinosMirage'] = plus_minos_rounds_team1["Mirage"]["plusMinosRounds"]
            df.loc[counter, 'Team1RoundsPlusMinosDust2'] = plus_minos_rounds_team1["Dust2"]["plusMinosRounds"]
            df.loc[counter, 'Team1RoundsPlusMinosNuke'] = plus_minos_rounds_team1["Nuke"]["plusMinosRounds"]
            df.loc[counter, 'Team1RoundsPlusMinosOverpass'] = plus_minos_rounds_team1["Overpass"]["plusMinosRounds"]
            df.loc[counter, 'Team1RoundsPlusMinosInferno'] = plus_minos_rounds_team1["Inferno"]["plusMinosRounds"]
            df.loc[counter, 'Team1RoundsPlusMinosVertigo'] = plus_minos_rounds_team1["Vertigo"]["plusMinosRounds"]
            df.loc[counter, 'Team1RoundsPlusMinosTrain'] = plus_minos_rounds_team1["Train"]["plusMinosRounds"]
            df.loc[counter, 'Team1RoundsPlusMinosCache'] = plus_minos_rounds_team1["Cache"]["plusMinosRounds"]
            df.loc[counter, 'Team2RoundsPlusMinosMirage'] = plus_minos_rounds_team2["Mirage"]["plusMinosRounds"]
            df.loc[counter, 'Team2RoundsPlusMinosDust2'] = plus_minos_rounds_team2["Dust2"]["plusMinosRounds"]
            df.loc[counter, 'Team2RoundsPlusMinosNuke'] = plus_minos_rounds_team2["Nuke"]["plusMinosRounds"]
            df.loc[counter, 'Team2RoundsPlusMinosOverpass'] = plus_minos_rounds_team2["Overpass"]["plusMinosRounds"]
            df.loc[counter, 'Team2RoundsPlusMinosInferno'] = plus_minos_rounds_team2["Inferno"]["plusMinosRounds"]
            df.loc[counter, 'Team2RoundsPlusMinosVertigo'] = plus_minos_rounds_team2["Vertigo"]["plusMinosRounds"]
            df.loc[counter, 'Team2RoundsPlusMinosTrain'] = plus_minos_rounds_team2["Train"]["plusMinosRounds"]
            df.loc[counter, 'Team2RoundsPlusMinosCache'] = plus_minos_rounds_team2["Cache"]["plusMinosRounds"]

            df.loc[counter, 'Team1Winner'] = 1 if game.team1_score > game.team2_score else 0

            counter = counter + 1
        print(df)

    def decision_tree_machine_learning(self):
        # Decision Tree Classification

        # Importing the libraries
        import numpy as np
        import matplotlib.pyplot as plt
        import pandas as pd

        # Importing the dataset
        dataset = pd.read_csv("dataframe.csv")
        X = dataset.iloc[:, 1:13].values
        y = dataset.iloc[:, 13].values

        # Splitting the dataset into the Training set and Test set
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

        # Feature Scaling
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)

        # Fitting Decision Tree Classification to the Training set
        from sklearn.tree import DecisionTreeClassifier
        classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
        classifier.fit(X_train, y_train)

        # Predicting the Test set results
        y_pred = classifier.predict(X_test)

        # Making the Confusion Matrix
        from sklearn.metrics import confusion_matrix
        cm = confusion_matrix(y_test, y_pred)

        print(cm)
