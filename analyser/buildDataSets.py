import pandas as pd
from dao.game_dao import GameDAO
from dao.player_map_stats_dao import PlayerMapStatsDAO

class BuildDataSet():
    def __init__(self):
        pass

    def getPickConfidence(self, lastGames, team_id):
        d = {}
        wins = 0
        picks = 0
        for game in lastGames:
            if game.id_team1 == team_id:
                for map in game.maps:
                    if map.map_name == game.team1_picks_maps:
                        if d.get(map.map_name) == None:
                            d2 = {map.map_name: {"Pick": 1, "Win": 0, "Confidence": 0.0}}
                            if map.team1_total_rounds > map.team2_total_rounds:
                                d2[map.map_name]["Win"] = 1
                            else:
                                d2[map.map_name]["Win"] = 0
                            d.update(d2)
                        else:
                            d[map.map_name]["Pick"] = d[map.map_name]["Pick"] + 1
                            if map.team1_total_rounds > map.team2_total_rounds:
                                d[map.map_name]["Win"] = d[map.map_name]["Win"] + 1
            elif game.id_team2 == team_id:
                for map in game.maps:
                    if map.map_name == game.team2_picks_maps:
                        if d.get(map.map_name) == None:
                            d2 = {map.map_name: {"Pick": 1, "Win": 0, "Confidence": 0.0}}
                            if map.team2_total_rounds > map.team1_total_rounds:
                                d2[map.map_name]["Win"] = 1
                            else:
                                d2[map.map_name]["Win"] = 0
                            d.update(d2)
                        else:
                            d[map.map_name]["Pick"] = d[map.map_name]["Pick"] + 1
                            if map.team2_total_rounds > map.team1_total_rounds:
                                d[map.map_name]["Win"] = d[map.map_name]["Win"] + 1
        for item in d:
            wins = wins + int(d[item]["Win"])
            picks = picks + int(d[item]["Pick"])

        return 100 * wins / picks

    def getWinPercentage(self, lastGames, team_id):
        wins = 0
        lost = 0
        for game in lastGames:
            if game.id_team1 == team_id:
                for map in game.maps:
                    if map.team1_total_rounds > map.team2_total_rounds:
                        wins = wins + 1
                    else:
                        lost = lost + 1
            elif game.id_team2 == team_id:
                for map in game.maps:
                    if map.team2_total_rounds > map.team1_total_rounds:
                        wins = wins + 1
                    else:
                        lost = lost + 1

        return 100 * wins / (wins + lost)

    def getAverageOppRank(self, lastGames, team_id):
        rankSum = 0
        for game in lastGames:
            if game.id_team1 == team_id:
                rankSum = rankSum + game.team2_rank
            elif game.id_team2 == team_id:
                rankSum = rankSum + game.team1_rank

        return 100 * rankSum / len(lastGames)

    def getPlusMinosPlayersTeam(self, games):
        sumPlusMinos = 0
        for game in games:
            for map in game.maps:
                for playerStats in map.player_map_stats:
                    sumPlusMinos = sumPlusMinos + playerStats.plus_minos

        return sumPlusMinos

    def getPlusMinosRoundsTeam(self, games, team_id):
        sumPlusMinos = 0
        for game in games:
            if game.id_team1 == team_id:
                for map in game.maps:
                    sumPlusMinos = sumPlusMinos + map.team1_total_rounds - map.team2_total_rounds
            else:
                for map in game.maps:
                    sumPlusMinos = sumPlusMinos + map.team2_total_rounds - map.team1_total_rounds

        return sumPlusMinos

    def getDataSet(self):
        df = pd.DataFrame(columns=['Team1Confidence', 'Team1WinPercentage', 'Team1Rank', 'Team1AverageOppRank', 'Team1PlayersPlusMinos', 'Team1RoundsPlusMinos',
                                   'Team2Confidence', 'Team2WinPercentage', 'Team2Rank', 'Team2AverageOppRank', 'Team2PlayersPlusMinos', 'Team2RoundsPlusMinos', 'Team1Winner'])

        df = pd.DataFrame(columns=['Map1', 'Map2', 'Map3', 'Team1Rank', 'Team2Rank',
                                   'Team1WinPercentageMirage', 'Team1WinPercentageDust2', 'Team1WinPercentageNuke', 'Team1WinPercentageOverpass', 'Team1WinPercentageInferno',
                                   'Team1WinPercentageVertigo', 'Team1WinPercentageTrain', 'Team1WinPercentageCache',
                                   'Team2WinPercentageMirage', 'Team2WinPercentageDust2', 'Team2WinPercentageNuke', 'Team2WinPercentageOverpass', 'Team2WinPercentageInferno',
                                   'Team2WinPercentageVertigo', 'Team2WinPercentageTrain', 'Team2WinPercentageCache',
                                   'Team1ConfidencePickMirage', 'Team1ConfidencePickDust2', 'Team1ConfidencePickNuke', 'Team1ConfidencePickOverpass', 'Team1ConfidencePickInferno',
                                   'Team1ConfidencePickVertigo', 'Team1ConfidencePickTrain', 'Team1ConfidencePickCache',
                                   'Team2ConfidencePickMirage', 'Team2ConfidencePickDust2', 'Team2ConfidencePickNuke', 'Team2ConfidencePickOverpass', 'Team2ConfidencePickInferno',
                                   'Team2ConfidencePickVertigo', 'Team2ConfidencePickTrain', 'Team2ConfidencePickCache',
                                   'Team1AverageOppRankMirage', 'Team1AverageOppRankDust2', 'Team1AverageOppRankNuke', 'Team1AverageOppRankOverpass', 'Team1AverageOppRankInferno',
                                   'Team1AverageOppRankVertigo', 'Team1AverageOppRankTrain', 'Team1AverageOppRankCache',
                                   'Team2AverageOppRankMirage', 'Team2AverageOppRankDust2', 'Team2AverageOppRankNuke', 'Team2AverageOppRankOverpass', 'Team2AverageOppRankInferno',
                                   'Team2AverageOppRankVertigo', 'Team2AverageOppRankTrain', 'Team2AverageOppRankCache',
                                   'Team1PlayersPlusMinosMirage', 'Team1PlayersPlusMinosDust2', 'Team1PlayersPlusMinosNuke', 'Team1PlayersPlusMinosOverpass', 'Team1PlayersPlusMinosInferno',
                                   'Team1PlayersPlusMinosVertigo', 'Team1PlayersPlusMinosTrain', 'Team1PlayersPlusMinosCache',
                                   'Team2PlayersPlusMinosMirage', 'Team2PlayersPlusMinosDust2', 'Team2PlayersPlusMinosNuke', 'Team2PlayersPlusMinosOverpass', 'Team2PlayersPlusMinosInferno',
                                   'Team2PlayersPlusMinosVertigo', 'Team2PlayersPlusMinosTrain', 'Team2PlayersPlusMinosCache',
                                   'Team1RoundsPlusMinosMirage', 'Team1RoundsPlusMinosDust2', 'Team1RoundsPlusMinosNuke', 'Team1RoundsPlusMinosOverpass', 'Team1RoundsPlusMinosInferno',
                                   'Team1RoundsPlusMinosVertigo', 'Team1RoundsPlusMinosTrain', 'Team1RoundsPlusMinosCache',
                                   'Team2RoundsPlusMinosMirage', 'Team2RoundsPlusMinosDust2', 'Team2RoundsPlusMinosNuke', 'Team2RoundsPlusMinosOverpass', 'Team2RoundsPlusMinosInferno',
                                   'Team2RoundsPlusMinosVertigo', 'Team2RoundsPlusMinosTrain', 'Team2RoundsPlusMinosCache'
                                   ])
        games = GameDAO().listLastGames()
        counter = 0
        for game in games:
            if counter == 500:
                break

            team1LastGames = GameDAO().listTeamLastMapsGames(game.id_game, game.id_team1, 10)
            team2LastGames = GameDAO().listTeamLastMapsGames(game.id_game, game.id_team2, 10)

            if len(team1LastGames) < 10 or len(team2LastGames) < 10:
                continue

            team1Confidence = self.getPickConfidence(team1LastGames, game.id_team1)
            team2Confidence = self.getPickConfidence(team2LastGames, game.id_team2)

            winPercentageTeam1 = self.getWinPercentage(team1LastGames, game.id_team1)
            winPercentageTeam2 = self.getWinPercentage(team2LastGames, game.id_team2)

            game.team1_rank
            game.team2_rank

            averageOppRankTeam1 = self.getAverageOppRank(team1LastGames, game.id_team1)
            averageOppRankTeam2 = self.getAverageOppRank(team2LastGames, game.id_team2)

            gamesWithTeam1PlayersStats = GameDAO().listTeamLastGamesWithPlayersStats(game.id_game, game.id_team1, 150)
            gamesWithTeam2PlayersStats = GameDAO().listTeamLastGamesWithPlayersStats(game.id_game, game.id_team2, 150)

            plusMinosPlayersTeam1 = self.getPlusMinosPlayersTeam(gamesWithTeam1PlayersStats)
            plusMinosPlayersTeam2 = self.getPlusMinosPlayersTeam(gamesWithTeam2PlayersStats)

            plusMinosRoundsTeam1 = self.getPlusMinosRoundsTeam(team1LastGames, game.id_team1)
            plusMinosRoundsTeam2 = self.getPlusMinosRoundsTeam(team2LastGames, game.id_team2)

            df.loc[counter, 'Team1Confidence'] = team1Confidence
            df.loc[counter, 'Team2Confidence'] = team2Confidence
            df.loc[counter, 'Team1WinPercentage'] = winPercentageTeam1
            df.loc[counter, 'Team2WinPercentage'] = winPercentageTeam2
            df.loc[counter, 'Team1Rank'] = game.team1_rank
            df.loc[counter, 'Team2Rank'] = game.team2_rank
            df.loc[counter, 'Team1AverageOppRank'] = averageOppRankTeam1
            df.loc[counter, 'Team2AverageOppRank'] = averageOppRankTeam2
            df.loc[counter, 'Team1PlayersPlusMinos'] = plusMinosPlayersTeam1
            df.loc[counter, 'Team2PlayersPlusMinos'] = plusMinosPlayersTeam2
            df.loc[counter, 'Team1RoundsPlusMinos'] = plusMinosRoundsTeam1
            df.loc[counter, 'Team2RoundsPlusMinos'] = plusMinosRoundsTeam2
            df.loc[counter, 'Team1Winner'] = 1 if game.team1_score > game.team2_score else 0

            counter = counter + 1
        print(df)

    def decisionTreeML(self):
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