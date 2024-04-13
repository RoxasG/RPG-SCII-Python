import sqlite3
import random
import uuid

def print_ascii_art(player_class):
    art = {
        'Warrior': '''
        ,dM
        dMMP
       dMMM'
       \\MM/
       dMMm.
      dMMP'_\\---
     _| _  p ;88;`.
    ,db; p >  ;8P|  `.
   (``T8b,__,'dP |   |
   |   `Y8b..dP  ;_  |
   |    |`T88P_ /  `\\;
   :_.-~|d8P'`Y/    /
        \\_   TP    \\
         \\;:   \\    |
         \\|   |     \\
         ;   |      \\
        /    |       \\
       |_____|       `._________
       |    :|        |_________>
       |    :|        |
       |_____|        |
       ;-----;        |
       |    -|        |
       |_____|        |
       |    :|        |
       |_____|        |''',
        'Mage': '''
           _
         /\\_,-\\\\
       /\\_)   _\\
      /\\_)    \\
     /\\_)    -\\
    (___)   -\\)
            \\)\\)
           /,-'
          // \\\\
         ((   ))
          \\\\ // 
           `-''',
        'Rogue': '''
         .-.
        |o,o|
       /)__)  -"--"-
        " "''',
    }
    print(art.get(player_class, "Class not found"))

class RPGGame:
    def __init__(self):
        self.db_path = 'game_data.db'
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Players (
                player_id TEXT PRIMARY KEY,
                player_name TEXT NOT NULL,
                player_class TEXT NOT NULL,
                health INTEGER,
                mana INTEGER,
                strength INTEGER,
                agility INTEGER,
                intelligence INTEGER,
                experience INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1
            )
        ''')
        conn.commit()
        conn.close()

    def create_player(self, name, player_class):
        player_id = str(uuid.uuid4())
        class_attributes = {
            'Warrior': {'health': 200, 'mana': 50, 'strength': 10, 'agility': 5, 'intelligence': 3},
            'Mage': {'health': 100, 'mana': 150, 'strength': 3, 'agility': 5, 'intelligence': 10},
            'Rogue': {'health': 150, 'mana': 100, 'strength': 7, 'agility': 10, 'intelligence': 5}
        }
        attributes = class_attributes[player_class]
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Players (player_id, player_name, player_class, health, mana, strength, agility, intelligence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (player_id, name, player_class, attributes['health'], attributes['mana'], attributes['strength'], attributes['agility'], attributes['intelligence']))
            return player_id

    def character_creation(self):
        print("Welcome to the character creation wizard!\n")
        player_name = input("Enter your character's name: ")
        print("\nChoose your class:")
        print("1. Warrior\n2. Mage\n3. Rogue")
        class_choice = input("\nEnter the number of your class: ")
        classes = {'1': 'Warrior', '2': 'Mage', '3': 'Rogue'}
        player_class = classes.get(class_choice, 'Warrior')
        print_ascii_art(player_class)
        player_id = self.create_player(player_name, player_class)
        print(f"\nCharacter created successfully! Name: {player_name}, Class: {player_class}, ID: {player_id}")
        return player_id

    def play_level(self, player_id):
        xp_gain = random.randint(20, 50)  # Random XP gain for playing a level
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE Players SET experience = experience + ? WHERE player_id = ?', (xp_gain, player_id))
            cursor.execute('SELECT player_id, player_name, level, experience FROM Players WHERE player_id = ?', (player_id,))
            player_info = cursor.fetchone()
            print(f"\nPlayer {player_info[1]} (ID: {player_info[0]}) played a level and gained {xp_gain} XP.")
            print(f"Total Experience: {player_info[3]}, Level: {player_info[2]}")

def main():
    game = RPGGame()
    player_id = game.character_creation()
    while True:
        action = input("\nChoose an action ('play' to play a level, 'exit' to quit): ")
        if action == 'play':
            game.play_level(player_id)
        elif action == 'exit':
            print("Exiting game.")
            break

if __name__ == "__main__":
    main()
