import sys

from analyser.analysis import Analysis
from build_team import BuildTeam
from build_team import BuildGame
from db import db
from datetime import datetime as dt
from builder.team_builder import TeamBuilder
from analyser.build_data_sets import BuildDataSet


def teste():
    # db().createTables()
    # TeamBuilder().createDefaultTeams()

    # BuildTeam().fullUpdateByTeam("forZe")
    # BuildTeam().fullUpdateByTeam("Gambit Youngsters")

    # startDate = dt.now()
    # BuildTeam().fullUpdateAllTeams(15)
    # BuildTeam().checkForOneTeam("100 Thieves")
    # endDate = dt.now()
    # print("All operations. Seconds " + str((endDate - startDate).total_seconds()))
    # BuildDataSet().getDataSet()
    BuildDataSet().decision_tree_machine_learning()
    # BuildGame().check("https://www.hltv.org/matches/2340651/natus-vincere-vs-fnatic-esl-pro-league-season-11-europe")


def main(argv):
    if argv[0] == "analysis":
        team1 = argv[1] if "-" not in argv[1] else argv[1].replace("-", " ")
        team2 = argv[2] if "-" not in argv[2] else argv[2].replace("-", " ")
        Analysis().getAnalysis(team1, team2, argv[3].split(";"))
    elif argv[0] == "updateTeam":
        team1 = argv[1] if "-" not in argv[1] else argv[1].replace("-", " ")
        BuildTeam().fullUpdateByTeam(team1, int(argv[2]))
    elif argv[0] == "fullUpdateTeams":
        BuildTeam().fullUpdateAllTeams(int(argv[1]))


if __name__ == "__main__":
    teste()
    # main(sys.argv[1:])
