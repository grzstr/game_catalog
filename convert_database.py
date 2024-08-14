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
    platform = ""
    if epic >= 1:
        platform += "Epic Games Store"
    if steam >= 1:
        if platform != "":
            platform += "/"
        platform += "Steam"
    if rockstar >= 1:
        if platform != "":
            platform += "/"
        platform += "Rockstar Games Launcher"
    if gog >= 1:
        if platform != "":
            platform += "/"
        platform += "GOG"
    if bethesda >= 1:
        if platform != "":
            platform += "/"
        platform += "Bethesda Launcher"
    if ea >= 1:
        if platform != "":
            platform += "/"
        platform += "EA"
    if muve >= 1:
        if platform != "":
            platform += "/"
        platform += "Muve"
    if ubisoft >= 1:
        if platform != "":
            platform += "/"
        platform += "Ubisoft Connect"
    if android >= 1:
        if platform != "":
            platform += "/"
        platform += "Android"
    if microsoft >= 1:
        if platform != "":
            platform += "/"
        platform += "Microsoft Store"
    if other >= 1:
        if platform != "":
            platform += "/"
        platform += "Other"
    if cdaction >= 1:
        if platform != "":
            platform += "/"
        platform += "CD-Action"

    if epic == 0 and steam == 0 and rockstar == 0 and gog == 0 and bethesda == 0 and ea == 0 and muve == 0 and ubisoft == 0 and android == 0 and microsoft == 0 and other == 0 and cdaction == 0:
        return "None"

    return platform


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
    platform = convert_platform(data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17])
    subscription = convert_subscription(data[18], data[19], data[20])
    paid = convert_paid(data[21], data[22], data[23], data[24], data[25], data[26], data[27])

    base.add_game(data[0], data[1], time, status, platform, subscription, data[5], paid, "-", "-", "-")

