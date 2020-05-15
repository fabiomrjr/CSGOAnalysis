from datetime import datetime as dt


def get_month_by_abreviation(month):

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


def get_date_time_by_day_and_time(day_game, start_time):

    day_game_splitted = day_game.split(" ")
    start_time_splitted = start_time.split(":")

    year = int(day_game_splitted[3])
    month = get_month_by_abreviation(day_game_splitted[2])
    day = int(day_game_splitted[0][:-2])
    hour = int(start_time_splitted[0])
    minutes = int(start_time_splitted[1])

    return dt(year, month, day, hour, minutes, 0, 0)