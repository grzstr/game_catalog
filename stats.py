from manage_database import database

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

        sorted_time = []
        for time in games_time:
            if time != 0:
                sorted_time.append(time)
        if sorted_time == []:
            sorted_time.append(0)

        min_value = min(sorted_time)
        min_index = games_time.index(min_value)
        time = self.convert_time_to_string(min_value)
        
        return time, min_index

    def total_games_summary(self, atribute):
        if atribute == "Owned":
            total = len(self.base.show_owned_games())
            finished = len(self.base.show_owned_games("Finished"))
            not_started = len(self.base.show_owned_games("Not started"))
            started = len(self.base.show_owned_games("Started"))
        elif atribute == "Subscribed":
            total = len(self.base.show_subscription_games())
            finished = len(self.base.show_subscription_games("Finished"))
            not_started = len(self.base.show_subscription_games("Not started"))
            started = len(self.base.show_subscription_games("Started"))
        elif atribute == "Digital":
            total = len(self.base.show_digital_games())
            finished = len(self.base.show_digital_games("Finished"))
            not_started = len(self.base.show_digital_games("Not started"))
            started = len(self.base.show_digital_games("Started"))
        elif atribute == "CD-Action":
            total = len(self.base.show_games_store_games("CD-Action"))
            finished = len(self.base.show_games_store_games("CD-Action", "Finished"))
            not_started = len(self.base.show_games_store_games("CD-Action", "Not started"))
            started = len(self.base.show_games_store_games("CD-Action", "Started"))
        elif atribute == "Box + CD-Action":
            total = len(self.base.show_games_store_games("CD-Action")) + len(self.base.show_box_games())
            finished = len(self.base.show_games_store_games("CD-Action", "Finished")) + len(self.base.show_box_games("Finished"))
            not_started = len(self.base.show_games_store_games("CD-Action", "Not started")) + len(self.base.show_box_games("Not started"))
            started = len(self.base.show_games_store_games("CD-Action", "Started")) + len(self.base.show_box_games("Started"))
        elif atribute == "Box":
            total = len(self.base.show_box_games())
            finished = len(self.base.show_box_games("Finished"))
            not_started = len(self.base.show_box_games("Not started"))
            started = len(self.base.show_box_games("Started"))
        elif atribute == "Free":
            total = len(self.base.show_free_games())
            finished = len(self.base.show_free_games("Finished"))
            not_started = len(self.base.show_free_games("Not started"))
            started = len(self.base.show_free_games("Started"))
        elif atribute == "Purchased":
            total = len(self.base.show_purchased_games())
            finished = len(self.base.show_purchased_games("Finished"))
            not_started = len(self.base.show_purchased_games("Not started"))
            started = len(self.base.show_purchased_games("Started"))
        else:
            total = 0
            finished = 0
            not_started = 0
            started = 0

        return total, finished, not_started, started
