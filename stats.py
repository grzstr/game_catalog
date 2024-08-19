from manage_database import database
import pandas as pd

class games_stats():
    def __init__(self):
        self.base = database()

    def convert_time(self, time):
        if isinstance(time, str):
            if time == "-":
                return 0
            elif len(time.split(":")) == 3:
                splited_time = time.split(":")
                seconds = int(splited_time[0])*3600
                seconds += int(splited_time[1])*60
                seconds += int(splited_time[2])
                return seconds
            else: 
                return 0
        elif isinstance(time, int):
            return time
        else:
            print("Wrong time format!")
            return 0

    def get_games_time(self):
        games = self.base.show_games()
        games_time = []
        for game in games:
            games_time.append(self.convert_time(game[3]))

        return games_time
    
    def total_playing_time(self):
        total_time_sec = 0
        for game_time in self.get_games_time():
            total_time_sec += game_time
        
        total_time_min = total_time_sec/60
        total_time_hours = total_time_min/60
        total_time_days = total_time_hours/24
        total_time_years = total_time_days/360

        return total_time_years, total_time_days, total_time_hours, total_time_min, total_time_sec


    def convert_time_to_string(self, time):
        if isinstance(time, int):
            hours = str(time/3600).split(".")[0]
            if len(hours) == 1:
                hours = "0" + hours

            minutes = str(float("0." + str(time/3600).split(".")[1])*60).split(".")[0]
            if len(minutes) == 1:
                minutes = "0" + minutes
            elif len(minutes) > 2:
                minutes = minutes[0:2]
            
            seconds = str(int(str(float("0." + str(time/3600).split(".")[1])*60).split(".")[1])*60)
            if len(seconds) == 1:
                seconds = "0" + seconds
            elif len(seconds) > 2:
                seconds = seconds[0:2]

            return hours + ":" + minutes + ":" + seconds
        else:
            print("Wrong time format!")
            return "0:0:0"

    def the_longest_playing_time(self):
        games_time = self.get_games_time()
        max_value = max(games_time)
        max_index = games_time.index(max_value)
        time = self.convert_time_to_string(max_value)
        
        return time, max_index
    
    def the_shortest_playing_time(self):
        games_time = self.get_games_time()
        min_value = min(games_time)
        min_index = games_time.index(min_value)
        time = self.convert_time_to_string(min_value)
        
        return time, min_index

    def get_started_games(self):
        games = self.base.show_games()
        pass