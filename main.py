import sys

from analyser.analysis import Analysis
from build_team import BuildTeam
from build_team import BuildGame
from db import db
from datetime import datetime as dt
from builder.team_builder import TeamBuilder
from analyser.team_indicators import TeamIndicators
from analyser.build_data_sets import BuildDataSet
from analyser.build_simplified_data_sets import BuildSimplifiedDataSet


def funcao1():
    # db().createTables()
    # TeamBuilder().createDefaultTeams()
    # df, df2 = TeamIndicators().win_rank_matrix()
    # print(df)
    # BuildDataSet().get_data_set()
    #decision_tree_classifier = BuildDataSet().decision_tree_machine_learning()
    #randon_forest_tree_classifier = BuildDataSet().randon_forest_machine_learning()
    #knn_tree_classifier = BuildDataSet().knn_machine_learning()
    #ann_tree_classifier = BuildDataSet().ann_machine_learning()

    #BuildSimplifiedDataSet().get_data_set()
    #decision_tree_classifier = BuildSimplifiedDataSet().decision_tree_machine_learning()
    #randon_forest_tree_classifier = BuildSimplifiedDataSet().randon_forest_machine_learning()
    #knn_tree_classifier = BuildSimplifiedDataSet().knn_machine_learning()
    ann_tree_classifier = BuildSimplifiedDataSet().ann_machine_learning()

    # df = BuildDataSet().get_predict_game_data_set("Furia", "Mibr", ["Vertigo", "Train"])
    # y = BuildDataSet().predict_result(decision_tree_classifier, df)
    # print(y)

    # BuildGame().check("https://www.hltv.org/matches/2340651/natus-vincere-vs-fnatic-esl-pro-league-season-11-europe")


def main(argv):
    if argv[0] == "analysis":
        team1 = argv[1] if "-" not in argv[1] else argv[1].replace("-", " ")
        team2 = argv[2] if "-" not in argv[2] else argv[2].replace("-", " ")
        Analysis().get_analysis(team1, team2, argv[3].split(";"))
    elif argv[0] == "updateTeam":
        team1 = argv[1] if "-" not in argv[1] else argv[1].replace("-", " ")
        BuildTeam().full_update_by_team(team1, int(argv[2]))
    elif argv[0] == "fullUpdateTeams":
        BuildTeam().full_update_all_teams(int(argv[1]))
    elif argv[0] == "updateTeamsMatches":
        BuildTeam().update_matches_all_teams(int(argv[1]))
    elif argv[0] == "createDefaultTeams":
        TeamBuilder().createDefaultTeams()


if __name__ == "__main__":
    # funcao1()
    main(sys.argv[1:])
