from datetime import datetime as dt

class util():
    def __init__(self):
        pass

    def getMonthByAbreviation(self, month):

        switcher = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }
        return switcher.get(month, "Invalid month")

    def getDateTimeByDayAndTime(self, dayGame, startTime):

        dayGameSplitted = dayGame.split(" ")
        startTimeSplitted = startTime.split(":")

        year = int(dayGameSplitted[3])
        month = self.getMonthByAbreviation(dayGameSplitted[2])
        day = int(dayGameSplitted[0][:-2])
        hour = int(startTimeSplitted[0])
        minutes = int(startTimeSplitted[1])

        return dt(year, month, day, hour, minutes, 0, 0)
