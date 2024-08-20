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
        for status in ("Finished", "Started", "Not started"):
            cursor.execute(f"""
            INSERT INTO status (status_name) VALUES ("{status}")
            """)

        #GAMES STORE TABLE
        for games_store in ("None", "Other", "Epic Games Store", "Steam", "GOG", "Ubisoft Connect", "Microsoft Store"):
            cursor.execute(f"""
            INSERT INTO games_store (games_store_name) VALUES ("{games_store}")
            """)

        #PLATFORM TABLE
        for platform in ("Other", "PC", "Google Play", "iOS", "PlayStation", "Xbox", "Nintendo"):
            cursor.execute(f"""
            INSERT INTO platform (platform_name) VALUES ("{platform}")
            """)

        conn.commit()
        conn.close()

        #SUBSCRIPTION TABLE
        for subscription, games_store in zip(("None", "Xbox Game Pass", "Ubisoft+"),("None", "Microsoft Store", "Ubisoft Connect")):
            games_store_id = self.get_games_store_id(games_store)
            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO subscription (subscription_name, games_store_id) VALUES (:subscription, :games_store_id)", {"subscription": subscription, "games_store_id":games_store_id})
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
            games_store_id INTEGER,
            subscription_id INTEGER,
            box INTEGER,
            paid INTEGER,
            publisher_id INTEGER,
            developer_id INTEGER,
            series_id INTEGER,
            FOREIGN KEY (status_id) REFERENCES status(id),
            FOREIGN KEY (platform_id) REFERENCES platform(id),
            FOREIGN KEY (games_store_id) REFERENCES games_store(id),
            FOREIGN KEY (subscription_id) REFERENCES subscription(id),
            FOREIGN KEY (publisher_id) REFERENCES publisher(id),
            FOREIGN KEY (developer_id) REFERENCES developer(id),
            FOREIGN KEY (series_id) REFERENCES series(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS wishlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            platform_id INTEGER,
            publisher_id INTEGER,
            developer_id INTEGER,
            FOREIGN KEY (platform_id) REFERENCES platform(id),
            FOREIGN KEY (publisher_id) REFERENCES publisher(id),
            FOREIGN KEY (developer_id) REFERENCES developer(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS games_store (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            games_store_name TEXT
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
        CREATE TABLE IF NOT EXISTS developer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            developer_name TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS publisher (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            publisher_name TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscription (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subscription_name TEXT,
            games_store_id INTEGER,
            FOREIGN KEY (games_store_id) REFERENCES games_store(id)
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

    def convert_yes_no(self, answer):
        if answer == "Yes" or answer == "yes":
            return 1
        else:
            return 0

    def get_status_id(self, status_name):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM status WHERE status_name = :status_name", {"status_name": status_name})
        status_id = cursor.fetchone()
        conn.close()
        return status_id[0]  

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

    def get_games_store_id(self, games_store):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM games_store WHERE games_store_name = :games_store", {"games_store": games_store})
        games_store_id = cursor.fetchone()
        if games_store_id is None:
            cursor.execute("INSERT INTO games_store (games_store_name) VALUES (:games_store)", {"games_store": games_store})
            conn.commit()
            cursor.execute("SELECT id FROM games_store WHERE games_store_name = :games_store", {"games_store": games_store})
            games_store_id = cursor.fetchone()
        conn.close()
        return games_store_id[0]

    def get_subscription_id(self, subscription, games_store_id=1):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM subscription WHERE subscription_name = :subscription", {"subscription": subscription})
        subscription_id = cursor.fetchone()
        if subscription_id is None:
            cursor.execute("INSERT INTO subscription VALUES (:subscription, :games_store_id)", {"subscription": subscription})
            conn.commit()
            cursor.execute("SELECT id FROM subscription WHERE subscription_name = :subscription", {"subscription": subscription, "games_store_id": games_store_id})
            subscription_id = cursor.fetchone()
        conn.close()
        return subscription_id[0]

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

    def get_publisher_id(self, publisher):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM publisher WHERE publisher_name = :publisher", {"publisher": publisher})
        publisher_id = cursor.fetchone()
        if publisher_id is None:
            cursor.execute("INSERT INTO publisher (publisher_name) VALUES (:publisher)", {"publisher": publisher})
            conn.commit()
            cursor.execute("SELECT id FROM publisher WHERE publisher_name = :publisher", {"publisher": publisher})
            publisher_id = cursor.fetchone()
        conn.close()
        return publisher_id[0]

    def get_developer_id(self, developer):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM developer WHERE developer_name = :developer", {"developer": developer})
        developer_id = cursor.fetchone()
        if developer_id is None:
            cursor.execute("INSERT INTO developer (developer_name) VALUES (:developer)", {"developer": developer})
            conn.commit()
            cursor.execute("SELECT id FROM developer WHERE developer_name = :developer", {"developer": developer})
            developer_id = cursor.fetchone()
        conn.close()
        return developer_id[0]

    def get_platform_name(self, id):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT platform_name FROM platform WHERE id = :platform_id", {"platform_id": id})
        platform_name = cursor.fetchone()
        conn.close()
        return platform_name[0]       

    def get_games_store_name(self, id):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT games_store_name FROM games_store WHERE id = :games_store_id", {"games_store_id": id})
        games_store_name = cursor.fetchone()
        conn.close()
        return games_store_name[0]       

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

    def get_publisher_name(self, id):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT publisher_name FROM publisher WHERE id = :publisher_id", {"publisher_id": id})
        publisher_name = cursor.fetchone()
        conn.close()
        return publisher_name[0]

    def get_developer_name(self, id):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT developer_name FROM developer WHERE id = :developer_id", {"developer_id": id})
        developer_name = cursor.fetchone()
        conn.close()
        return developer_name[0]    

    def check_status(self, status):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM status WHERE status_name = :status", {"status": status})
        status_id = cursor.fetchone()
        conn.close()
        if status_id is None:
            return 3
        else:
            return status_id[0]

    def check_paid(self, paid):
        if paid == 1 or paid == 0:
            return paid
        else:
            return 1

    def check_box(self, box):
        if box == 1 or box == 0:
            return box
        else:
            return 0

    def add_games_store(self, games_store):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO games_store (games_store_name) VALUES (:games_store)", {"games_store": games_store})
        conn.commit()
        conn.close()

    def add_platform(self, platform):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO platform (platform_name) VALUES (:platform)", {"platform": platform})
        conn.commit()
        conn.close()

    def add_series(self, series):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO series (series_name) VALUES (:series)", {"series": series})
        conn.commit()
        conn.close()

    def add_publisher(self, publisher):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO publisher (publisher_name) VALUES (:publisher)", {"publisher": publisher})
        conn.commit()
        conn.close()

    def add_developer(self, developer):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO developer (developer_name) VALUES (:developer)", {"developer": developer})
        conn.commit()
        conn.close()

    def add_subscription(self, subscription, games_store):
        games_store_id = self.get_games_store_id(games_store)
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO subscription (subscription_name, games_store_id) VALUES (:subscription, :games_store_id)", {"subscription": subscription, "games_store_id":games_store_id})
        conn.commit()
        conn.close()

    def add_game_to_wishlist(self, title, platform, publisher, developer):
            platform_id = self.get_platform_id(platform)
            publisher_id = self.get_publisher_id(publisher)
            developer_id = self.get_developer_id(developer)

            conn = sqlite3.connect(self.database_name)
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO wishlist (
                title,
                platform_id,
                publisher_id,
                developer_id
            ) VALUES (
                :title,
                :platform_id,
                :publisher_id,
                :developer_id
            )
            """, {
                "title": title,
                "platform_id": platform_id,
                "publisher_id": publisher_id,
                "developer_id": developer_id
            })
            conn.commit()
            conn.close()

    def add_game(self, title, number_of_copies, game_time, status, platform, games_store, subscription, box, paid, publisher, developer, series):
        platform_id = self.get_platform_id(platform)
        games_store_id = self.get_games_store_id(games_store)
        status_id = self.check_status(status)
        subscription_id = self.get_subscription_id(subscription, games_store_id)
        paid = self.check_paid(paid)
        box = self.check_box(box)
        series_id = self.get_series_id(series)
        publisher_id = self.get_publisher_id(publisher)
        developer_id = self.get_developer_id(developer)

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO games (
            title,
            number_of_copies,
            game_time,
            status_id,
            platform_id,
            games_store_id,
            subscription_id,
            box,
            paid,
            publisher_id,
            developer_id,
            series_id
        ) VALUES (
            :title,
            :number_of_copies,
            :game_time,
            :status_id,
            :platform_id,
            :games_store_id,
            :subscription_id,
            :box,
            :paid,
            :publisher_id,
            :developer_id,
            :series_id
        )
        """, {
            "title": title,
            "number_of_copies": number_of_copies,
            "game_time": game_time,
            "status_id": status_id,
            "platform_id": platform_id,
            "games_store_id": games_store_id,
            "subscription_id": subscription_id,
            "box": box,
            "paid": paid,
            "publisher_id": publisher_id,
            "developer_id": developer_id,
            "series_id": series_id
        })
        conn.commit()
        conn.close()

    def modify_game(self, id, title, number_of_copies, game_time, status, platform, games_store, subscription, box, paid, publisher, developer, series):
        platform_id = self.get_platform_id(platform)
        games_store_id = self.get_games_store_id(games_store)
        status_id = self.check_status(status)
        subscription_id = self.get_subscription_id(subscription, games_store_id)
        paid = self.check_paid(paid)
        box = self.check_box(box)
        series_id = self.get_series_id(series)
        publisher_id = self.get_publisher_id(publisher)
        developer_id = self.get_developer_id(developer)

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE games SET
            title = ?,
            number_of_copies = ?,
            game_time = ?,
            status_id = ?,
            platform_id = ?,
            games_store_id = ?,
            subscription_id = ?,
            box = ?,
            paid = ?,
            publisher_id = ?,
            developer_id = ?,
            series_id = ?
        WHERE id = ?
        """, (title,
              number_of_copies,
              game_time,
              status_id,
              platform_id,
              games_store_id,
              subscription_id,
              box,
              paid,
              publisher_id,
              developer_id,
              series_id,
              id
        ))
        conn.commit()
        conn.close()

    def delete_subscription(self, subscription_name):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subscription WHERE subscription_name = :subscription_name", {"subscription_name": subscription_name})
        conn.commit()
        conn.close()

    def delete_developer(self, developer_name):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM developer WHERE developer_name = :developer_name", {"developer_name": developer_name})
        conn.commit()
        conn.close()

    def delete_series(self, series_name):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM series WHERE series_name = :series_name", {"series_name": series_name})
        conn.commit()
        conn.close()

    def delete_platform(self, platform_name):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM platform WHERE platform_name = :platform_name", {"platform_name": platform_name})
        conn.commit()
        conn.close()

    def delete_games_store(self, games_store_name):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM games_store WHERE games_store_name = :games_store_name", {"games_store_name": games_store_name})
        conn.commit()
        conn.close()

    def delete_publisher(self, publisher_name):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM publisher WHERE publisher_name = :publisher_name", {"publisher_name": publisher_name})
        conn.commit()
        conn.close()

    def delete_game(self, title):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM games WHERE title = :title", {"title": title})
        conn.commit()
        conn.close()

    def delete_wishlist_game(self, title):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM wishlist WHERE title = :title", {"title": title})
        conn.commit()
        conn.close()

    def show_games(self, find=None, sort=None):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()

        command = "SELECT * FROM games"
        if find != None:
            command += f" WHERE title LIKE '%{find}%'"
        
        if sort != None:
            if "=" in sort:
                if find == None:
                    command += f" WHERE {sort}"
                else:
                    command += f" AND {sort}"
        
        if sort != None and "=" not in sort:
            command += f" ORDER BY {sort}"

        cursor.execute(command)    
        games = cursor.fetchall()
        conn.close()
        return games

    def check_wishlist_atribute(self, sort):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(wishlist)")     
        columns_info = cursor.fetchall()
        column_names = [column[1] for column in columns_info]
        if sort[:-1] in column_names:
            return True
        else:
            return False

    def show_wishlist_games(self, find=None, sort=None):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()

        command = "SELECT * FROM wishlist"
        if find != None:
            command += f" WHERE title LIKE '%{find}%'"
        
        if sort != None:
            if "=" in sort and self.check_wishlist_atribute(sort.split("=")[0]):
                if find == None:
                    command += f" WHERE {sort}"
                else:
                    command += f" AND {sort}"
        
        if sort != None and "=" not in sort:
            command += f" ORDER BY {sort}"

        cursor.execute(command)    
        games = cursor.fetchall()
        conn.close()
        return games
    
    def show_owned_games(self, status = None):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        command = f"SELECT * FROM games WHERE subscription_id = {self.get_subscription_id("None", self.get_games_store_id("Other"))}"
        if status != None:
            command += f" AND status_id = {self.get_status_id(status)}"
        cursor.execute(command)
        games = cursor.fetchall()
        conn.close()
        return games
    
    def show_subscription_games(self, status = None):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        command = f"SELECT * FROM games WHERE subscription_id <> {self.get_subscription_id("None", self.get_games_store_id("Other"))}"
        if status != None:
            command += f" AND status_id = {self.get_status_id(status)}"
        cursor.execute(command)
        games = cursor.fetchall()
        conn.close()
        return games

    def show_purchased_games(self, status = None):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        command = f"SELECT * FROM games WHERE paid = 1"
        if status != None:
            command += f" AND status_id = {self.get_status_id(status)}"
        cursor.execute(command)
        games = cursor.fetchall()
        conn.close()
        return games
    
    def show_purchased_games_by_games_store(self, games_store):
        games_store_id = self.get_games_store_id(games_store)
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM games WHERE paid = :paid AND games_store_id = :games_store_id", {"paid": 1, "games_store_id": games_store_id})
        games = cursor.fetchall()
        conn.close()
        return games

    def show_free_games_by_games_store(self, games_store):
        games_store_id = self.get_games_store_id(games_store)
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM games WHERE paid = :paid AND games_store_id = :games_store_id", {"paid": 0, "games_store_id": games_store_id})
        games = cursor.fetchall()
        conn.close()
        return games

    def show_free_games(self, status = None):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        command = "SELECT * FROM games WHERE paid = 0"
        if status != None:
            command += f" AND status_id = {self.get_status_id(status)}"
        cursor.execute(command)
        games = cursor.fetchall()
        conn.close()
        return games

    def show_games_store_games(self, games_store, status = None):
        games_store_id = self.get_games_store_id(games_store)
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        command = f"SELECT * FROM games WHERE games_store_id = {games_store_id}"
        if status != None:
            command += f" AND status_id = {self.get_status_id(status)}"
        cursor.execute(command)
        games = cursor.fetchall()
        conn.close()
        return games

    def show_box_games(self, status = None):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        command = "SELECT * FROM games WHERE box = 1"
        if status != None:
            command += f" AND status_id = {self.get_status_id(status)}"
        cursor.execute(command)
        games = cursor.fetchall()
        conn.close()
        return games

    def show_digital_games(self, status = None):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        command = "SELECT * FROM games WHERE box = 0"
        if status != None:
            command += f" AND status_id = {self.get_status_id(status)}"
        cursor.execute(command)
        games = cursor.fetchall()
        conn.close()
        return games

    def show_wishlist_game(self, title):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM wishlist WHERE title = :title", {"title": title})
        game = cursor.fetchall()
        conn.close()
        return game

    def show_game(self, title):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM games WHERE title = :title", {"title": title})
        game = cursor.fetchall()
        conn.close()
        return game
    
    def show_games_store(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM games_store")
        games_store = cursor.fetchall()
        conn.close()
        return games_store
    
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
    
    def show_series(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM series")
        series = cursor.fetchall()
        conn.close()
        return series
    
    def show_publisher(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM publisher")
        publisher = cursor.fetchall()
        conn.close()
        return publisher

    def show_developer(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM developer")
        developer = cursor.fetchall()
        conn.close()
        return developer
    
