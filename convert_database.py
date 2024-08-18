from manage_database import database
import pandas as pd


def convert_time(time):
    if time == "-":
        return time
    else:
        time = float(time)
        hours = str(time).split(".")[0]
        if len(hours) == 1:
            hours = "0" + hours

        minutes = str(float("0." + str(time).split(".")[1])*60).split(".")[0]
        if len(minutes) == 1:
            minutes = "0" + minutes
        elif len(minutes) > 2:
            minutes = minutes[0:2]
        
        seconds = str(int(str(float("0." + str(time).split(".")[1])*60).split(".")[1])*60)
        if len(seconds) == 1:
            seconds = "0" + seconds
        elif len(seconds) > 2:
            seconds = seconds[0:2]

        return hours + ":" + minutes + ":" + seconds

def convert_status(started, finished):
    if started == 1:
        return "Started"
    elif finished == 1:
        return "Finished"
    else:
        return "Not started"
    
def convert_platform(epic, steam, rockstar, gog, bethesda, ea, muve, ubisoft, android, microsoft, other, cdaction):
    if epic >=1 or steam >= 1 or rockstar >= 1 or gog >= 1 or bethesda >= 1 or ea >= 1 or muve >= 1 or ubisoft >= 1 or microsoft >= 1 or other >= 1 or cdaction >= 1:
        return "PC"
    elif android >= 1:
        return "Android"
    else:
        return "PC"

def convert_games_store(epic, steam, rockstar, gog, bethesda, ea, muve, ubisoft, android, microsoft, other, cdaction):
    games_store = ""
    if epic >= 1:
        games_store += "Epic Games Store"
    if steam >= 1:
        if games_store != "":
            games_store += "/"
        games_store += "Steam"
    if rockstar >= 1:
        if games_store != "":
            games_store += "/"
        games_store += "Rockstar Games Launcher"
    if gog >= 1:
        if games_store != "":
            games_store += "/"
        games_store += "GOG"
    if bethesda >= 1:
        if games_store != "":
            games_store += "/"
        games_store += "Bethesda Launcher"
    if ea >= 1:
        if games_store != "":
            games_store += "/"
        games_store += "EA"
    if muve >= 1:
        if games_store != "":
            games_store += "/"
        games_store += "Muve"
    if ubisoft >= 1:
        if games_store != "":
            games_store += "/"
        games_store += "Ubisoft Connect"
    if android >= 1:
        if games_store != "":
            games_store += "/"
        games_store += "Google Play"
    if microsoft >= 1:
        if games_store != "":
            games_store += "/"
        games_store += "Microsoft Store"
    if other >= 1:
        if games_store != "":
            games_store += "/"
        games_store += "Other"
    if cdaction >= 1:
        if games_store != "":
            games_store += "/"
        games_store += "CD-Action"

    if epic == 0 and steam == 0 and rockstar == 0 and gog == 0 and bethesda == 0 and ea == 0 and muve == 0 and ubisoft == 0 and android == 0 and microsoft == 0 and other == 0 and cdaction == 0:
        return "None"

    return games_store


def convert_subscription(xbox, ea, ubisoft):
    subscription = ""
    if xbox >= 1:
        subscription += "Xbox Game Pass"
    if ea >= 1:
        if subscription != "":
            subscription += "/"
        subscription += "EA Play"
    if ubisoft >= 1:
        if subscription != "":
            subscription += "/"
        subscription += "Ubisoft+"
    if subscription >= "":
        return "None"
    
    return subscription

def convert_paid(epic, gog, steam, ea, rockstar, microsoft, ubisoft):
    if epic == 1 or gog == 1 or steam == 1 or ea == 1 or rockstar == 1 or microsoft == 1 or ubisoft == 1:
        return 0
    else:
        return 1

excel = pd.read_excel("databases/database.xlsx")
base = database()

for data in excel._values:
    time = convert_time(data[2])
    status = convert_status(data[3], data[4])
    games_store = convert_games_store(data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17])
    subscription = convert_subscription(data[18], data[19], data[20])
    paid = convert_paid(data[21], data[22], data[23], data[24], data[25], data[26], data[27])
    platform = convert_platform(data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17])

    base.add_game(data[0], data[1], time, status, platform, games_store, subscription, data[5], paid, "-", "-", "-")

wishlist = pd.read_excel("databases/wishlist.xlsx")

for data in wishlist._values:
    base.add_game_to_wishlist(data[0], data[1], data[2], data[3])
