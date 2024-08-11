import sqlite3
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class database():
    def __init__(self):
        self.database_name = "databases/games_database.db"

    def exist(self):
        if os.path.exists(self.database_name):
            return True
        else:
            return False


    def connect(self):
        try:
            conn = sqlite3.connect(self.database_name)
            return conn
        except:
            print("Error in connection")
            return None
    
    def configure_tables(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()

        #STATUS TABLE
        for status in ("Finished", "Started", "Unstarted"):
            cursor.execute(f"""
            INSERT INTO status (status_name) VALUES ("{status}")
            """)

        #PLATFORM TABLE
        for platform in ("Epic Games Store", "Steam", "GOG", "Ubisoft Connect", "Microsoft Store"):
            cursor.execute(f"""
            INSERT INTO platform (platform_name) VALUES ("{platform}")
            """)
        conn.commit()
        conn.close()

        #SUBSCRIPTION TABLE
        for subscription, platform in zip(("Xbox Game Pass", "Ubisoft+"),("Microsoft Store", "Ubisoft Connect")):
            platform_id = self.get_platform_id(platform)
            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO subscription (subscription_name, platform_id) VALUES (:subscription, :platform_id)", {"subscription": subscription, "platform_id":platform_id})
            conn.commit()
            conn.close()

    def create_tables(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            number_of_copies INTEGER,
            game_time REAL,
            status_id INTEGER,
            platform_id INTEGER,
            subscription_id INTEGER,
            paid INTEGER,
            publisher TEXT,
            developer TEXT,
            series_id INTEGER,
            FOREIGN KEY (status_id) REFERENCES status(id),
            FOREIGN KEY (platform_id) REFERENCES platform(id),
            FOREIGN KEY (subscription_id) REFERENCES subscription(id),
            FOREIGN KEY (series_id) REFERENCES series(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS platform (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform_name TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status_name TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscription (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subscription_name TEXT,
            platform_id INTEGER,
            FOREIGN KEY (platform_id) REFERENCES platform(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS series (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_name TEXT
        )
        """)

        conn.commit()
        conn.close()

    def get_platform_id(self, platform):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM platform WHERE platform_name = :platform", {"platform": platform})
        platform_id = cursor.fetchone()
        if platform_id is None:
            cursor.execute("INSERT INTO platform (platform_name) VALUES (:platform)", {"platform": platform})
            conn.commit()
            cursor.execute("SELECT id FROM platform WHERE platform_name = :platform", {"platform": platform})
            platform_id = cursor.fetchone()
        conn.close()
        return platform_id[0]

    def get_platform_name(self, id):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT platform_name FROM platform WHERE id = :platform_id", {"platform_id": id})
        platform_name = cursor.fetchone()
        conn.close()
        return platform_name[0]       

    def get_status_name(self, id):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT status_name FROM status WHERE id = :status_id", {"status_id": id})
        status_name = cursor.fetchone()
        conn.close()
        return status_name[0]       
       
    def get_series_name(self, id):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT series_name FROM series WHERE id = :series_id", {"series_id": id})
        series_name = cursor.fetchone()
        conn.close()
        return series_name[0]      
    
    def get_subscription_name(self, id):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT subscription_name FROM subscription WHERE id = :subscription_id", {"subscription_id": id})
        subscription_name = cursor.fetchone()
        conn.close()
        return subscription_name[0]     

    def check_status(self, status):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT status_name FROM status WHERE id = :status", {"status": status})
        status_id = cursor.fetchone()
        conn.close()
        if status_id is None:
            return 3
        else:
            return status_id[0]
        
    def get_subscription_id(self, subscription, platform_id):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM subscription WHERE subscription_name = :subscription", {"subscription": subscription})
        subscription_id = cursor.fetchone()
        if subscription_id is None:
            cursor.execute("INSERT INTO subscription VALUES (:subscription, :platform_id)", {"subscription": subscription})
            conn.commit()
            cursor.execute("SELECT id FROM subscription WHERE subscription_name = :subscription", {"subscription": subscription, "platform_id": platform_id})
            subscription_id = cursor.fetchone()
        conn.close()
        return subscription_id[0]

    def check_paid(self, paid):
        if paid == 1 or paid == 0:
            return paid
        else:
            return 1

    def get_series_id(self, series):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM series WHERE series_name = :series", {"series": series})
        series_id = cursor.fetchone()
        if series_id is None:
            cursor.execute("INSERT INTO series (series_name) VALUES (:series)", {"series": series})
            conn.commit()
            cursor.execute("SELECT id FROM series WHERE series_name = :series", {"series": series})
            series_id = cursor.fetchone()
        conn.close()
        return series_id[0]

    def add_platform(self, platform):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO platform (platform_name) VALUES (:platform)", {"platform": platform})
        conn.commit()
        conn.close()

    def add_subscription(self, subscription, platform):
        platform_id = self.get_platform_id(platform)
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO subscription (subscription_name, platform_id) VALUES (:subscription, :platform_id)", {"subscription": subscription, "platform_id":platform_id})
        conn.commit()
        conn.close()

    def add_game(self, title, number_of_copies, game_time, status, platform, subscription, paid, publisher, developer, series):
        platform_id = self.get_platform_id(platform)
        status_id = self.check_status(status)
        subscription_id = self.get_subscription_id(subscription, platform_id)
        paid = self.check_paid(paid)
        series_id = self.get_series_id(series)

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO games (
            title,
            number_of_copies,
            game_time,
            status_id,
            platform_id,
            subscription_id,
            paid,
            publisher,
            developer,
            series_id
        ) VALUES (
            :title,
            :number_of_copies,
            :game_time,
            :status_id,
            :platform_id,
            :subscription_id,
            :paid,
            :publisher,
            :developer,
            :series_id
        )
        """, {
            "title": title,
            "number_of_copies": number_of_copies,
            "game_time": game_time,
            "status_id": status_id,
            "platform_id": platform_id,
            "subscription_id": subscription_id,
            "paid": paid,
            "publisher": publisher,
            "developer": developer,
            "series_id": series_id
        })
        conn.commit()
        conn.close()

    def delete_game(self, title):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM games WHERE title = :title", {"title": title})
        conn.commit()
        conn.close()

    def show_games(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM games")
        games = cursor.fetchall()
        conn.close()
        return games
    
    def show_platform(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM platform")
        platform = cursor.fetchall()
        conn.close()
        return platform
    
    def show_subscription(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subscription")
        subscription = cursor.fetchall()
        conn.close()
        return subscription