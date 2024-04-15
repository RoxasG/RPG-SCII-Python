import sqlite3
import random
import uuid

class DatabaseManager:
    def __init__(self, db_path='game_data.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.setup_database()

    def setup_database(self):
        queries = [
            '''CREATE TABLE IF NOT EXISTS Players (
                player_id TEXT PRIMARY KEY,
                player_name TEXT NOT NULL,
                player_class TEXT NOT NULL,
                health INTEGER,
                mana INTEGER,
                strength INTEGER,
                agility INTEGER,
                intelligence INTEGER,
                experience INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                gold INTEGER DEFAULT 100
            )''',
            '''CREATE TABLE IF NOT EXISTS Items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                effect TEXT NOT NULL,
                value INTEGER
            )''',
            '''CREATE TABLE IF NOT EXISTS Inventory (
                player_id TEXT NOT NULL,
                item_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                FOREIGN KEY(player_id) REFERENCES Players(player_id),
                FOREIGN KEY(item_id) REFERENCES Items(item_id)
            )'''
        ]
        for query in queries:
            self.conn.execute(query)

    def execute_query(self, query, params=None):
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor

    def commit(self):
        self.conn.commit()

    def __del__(self):
        self.conn.close()

class RPGGame:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.player_id = None

    def create_character(self):
        name = input("Enter your character's name: ")
        print("Choose your class:\n1. Warrior\n2. Mage\n3. Rogue")
        classes = {'1': 'Warrior', '2': 'Mage', '3': 'Rogue'}
        class_choice = input("Enter the number of your class: ")
        player_class = classes.get(class_choice, 'Warrior')
        player_id = str(uuid.uuid4())
        self.db_manager.execute_query('''INSERT INTO Players (player_id, player_name, player_class)
                                         VALUES (?, ?, ?)''', (player_id, name, player_class))
        self.db_manager.commit()
        self.player_id = player_id
        print(f"Character created successfully! Name: {name}, Class: {player_class}, ID: {player_id}")

    def run(self):
        # Placeholder for the game loop
        pass

if __name__ == "__main__":
    db_manager = DatabaseManager()
    game = RPGGame(db_manager)
    game.run()
