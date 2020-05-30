import numpy as np
import pandas as pd
import tensorflow as tf
import analyser.team_indicators as team_indicators

from dao.game_dao import GameDAO
from dao.team_dao import TeamDAO
from analyser.team_indicators import TeamIndicators
from dao.player_map_stats_dao import PlayerMapStatsDAO

number_maps_to_consider = 8


class BuildSimplifiedDataSet:
    def __init__(self):
        pass

    def get_data_set(self):
        # df = pd.DataFrame(columns=['Team1Confidence', 'Team1WinPercentage', 'Team1Rank', 'Team1AverageOppRank',
        #                           'Team1PlayersPlusMinos', 'Team1RoundsPlusMinos',
        #                           'Team2Confidence', 'Team2WinPercentage', 'Team2Rank', 'Team2AverageOppRank',
        #                           'Team2PlayersPlusMinos', 'Team2RoundsPlusMinos', 'Team1Winner'])

        df = pd.DataFrame(columns=['Team1Rank', 'Team1WinRankAverage', 'Team1LoseRankAverage', 'Team2Rank',
                                   'Team2WinRankAverage', 'Team2LoseRankAverage'])

        games = GameDAO().list_last_games()
        counter = 0
        for game in games:
            # if counter == 500:
            #    break

            team1_last_10_games = GameDAO().list_team_last_maps_games(game.id_game, game.id_team1, number_maps_to_consider)
            team2_last_10_games = GameDAO().list_team_last_maps_games(game.id_game, game.id_team2, number_maps_to_consider)

            if len(team1_last_10_games) < number_maps_to_consider or len(team2_last_10_games) < number_maps_to_consider:
                continue
            if game.team1_picks_maps == "" and game.team2_picks_maps == "":
                continue

            team1_average_win_rank, team1_average_lose_rank = team_indicators.get_team_win_lose_rank_average(team1_last_10_games, game.id_team1)
            team2_average_win_rank, team2_average_lose_rank = team_indicators.get_team_win_lose_rank_average(team2_last_10_games, game.id_team2)

            df.loc[counter, 'Team1Rank'] = game.team1_rank
            df.loc[counter, 'Team1WinRankAverage'] = team1_average_win_rank
            df.loc[counter, 'Team1LoseRankAverage'] = team1_average_lose_rank
            df.loc[counter, 'Team2Rank'] = game.team2_rank
            df.loc[counter, 'Team2WinRankAverage'] = team2_average_win_rank
            df.loc[counter, 'Team2LoseRankAverage'] = team2_average_lose_rank

            df.loc[counter, 'Team1Winner'] = 1 if game.team1_score > game.team2_score else 0

            counter = counter + 1
        print(df)
        df.to_csv(r'C:\Users\fabio\Documents\Projetos\CSGOAnalysis\dataframe_simplified.csv', index=True)
        return df

    def randon_forest_machine_learning(self):

        dataset = pd.read_csv("dataframe_simplified.csv")
        # dataset = dataset.drop(['Map3'], axis=1)
        # dummies = pd.get_dummies(dataset, columns=['Map1', 'Map2'])

        y = dataset.iloc[:, 7].values
        X1 = dataset.drop(['Team1Winner'], axis=1).values
        X = X1[:, 1:7]

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

        # Feature Scaling
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)

        # Training the Random Forest Classification model on the Training set
        from sklearn.ensemble import RandomForestClassifier
        classifier = RandomForestClassifier(n_estimators=30, criterion='entropy', random_state=0)
        classifier.fit(X_train, y_train)

        # Predicting the Test set results
        y_pred = classifier.predict(X_test)

        # Making the Confusion Matrix
        from sklearn.metrics import confusion_matrix, accuracy_score
        cm = confusion_matrix(y_test, y_pred)
        ac = accuracy_score(y_test, y_pred)
        print(cm)
        print(ac)

    def decision_tree_machine_learning(self):

        dataset = pd.read_csv("dataframe_simplified.csv")
        # dataset = dataset.drop(['Map3'], axis=1)
        # dummies = pd.get_dummies(dataset, columns=['Map1', 'Map2'])

        y = dataset.iloc[:, 7].values
        X1 = dataset.drop(['Team1Winner'], axis=1).values
        X = X1[:, 1:7]


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
        from sklearn.metrics import confusion_matrix, accuracy_score
        cm = confusion_matrix(y_test, y_pred)
        ac = accuracy_score(y_test, y_pred)
        print(cm)
        print(ac)
        return classifier

    def knn_machine_learning(self):

        dataset = pd.read_csv("dataframe_simplified.csv")
        # dataset = dataset.drop(['Map3'], axis=1)
        # dummies = pd.get_dummies(dataset, columns=['Map1', 'Map2'])

        y = dataset.iloc[:, 7].values
        X1 = dataset.drop(['Team1Winner'], axis=1).values
        X = X1[:, 1:7]

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

        # Feature Scaling
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)

        # Training the K-NN model on the Training set
        from sklearn.neighbors import KNeighborsClassifier
        classifier = KNeighborsClassifier(n_neighbors=3, metric='minkowski', p=2)
        classifier.fit(X_train, y_train)

        # Predicting the Test set results
        y_pred = classifier.predict(X_test)

        # Making the Confusion Matrix
        from sklearn.metrics import confusion_matrix, accuracy_score
        cm = confusion_matrix(y_test, y_pred)
        ac = accuracy_score(y_test, y_pred)
        print(cm)
        print(ac)

    def ann_machine_learning(self):

        dataset = pd.read_csv("dataframe_simplified.csv")
        # dataset = dataset.drop(['Map3'], axis=1)
        # dummies = pd.get_dummies(dataset, columns=['Map1', 'Map2'])

        y = dataset.iloc[:, 7].values
        X1 = dataset.drop(['Team1Winner'], axis=1).values
        X = X1[:, 1:7]

        # Encoding categorical data
        # Label Encoding the "Gender" column
        #from sklearn.preprocessing import LabelEncoder
        #le = LabelEncoder()
        #X[:, 2] = le.fit_transform(X[:, 2])
        #print(X)
        # One Hot Encoding the "Geography" column
        #from sklearn.compose import ColumnTransformer
        #from sklearn.preprocessing import OneHotEncoder
        #ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1])], remainder='passthrough')
        #X = np.array(ct.fit_transform(X))
        #print(X)

        # Feature Scaling
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X = sc.fit_transform(X)
        print(X)

        # Splitting the dataset into the Training set and Test set
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        # Part 2 - Building the ANN

        # Initializing the ANN
        ann = tf.keras.models.Sequential()

        # Adding the input layer and the first hidden layer
        ann.add(tf.keras.layers.Dense(units=6, activation='relu'))

        # Adding the second hidden layer
        ann.add(tf.keras.layers.Dense(units=6, activation='relu'))

        #ann.add(tf.keras.layers.Dense(units=10, activation='relu'))

        # Adding the output layer
        ann.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

        # Part 3 - Training the ANN

        # Compiling the ANN
        ann.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        # Training the ANN on the Training set
        ann.fit(X_train, y_train, batch_size=32, epochs=300)

        # Part 4 - Making the predictions and evaluating the model

        # Predicting the Test set results
        y_pred = ann.predict(X_test)
        y_pred = (y_pred > 0.5)
        print(np.concatenate((y_pred.reshape(len(y_pred), 1), y_test.reshape(len(y_test), 1)), 1))

        # Making the Confusion Matrix
        from sklearn.metrics import confusion_matrix, accuracy_score
        cm = confusion_matrix(y_test, y_pred)
        ac = accuracy_score(y_test, y_pred)
        print(cm)
        print(ac)

    def predict_result(self, classifier, df_to_predict):
        import pandas as pd
        X = df_to_predict.drop(['Team1Winner'], axis=1).values
        #X = X1[:, 1:95]
        y_pred = classifier.predict(X)

        return y_pred