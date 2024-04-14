import sqlite3
import random
import uuid

def print_ascii_art(player_class):
    art = {
        'Warrior': """
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
       |_____|        |""",
        'Mage': """
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
           `-''""",
        'Rogue': """
         .-.
        |o,o|
       /)__)  -"--"-
        " " """
    }
    print(art.get(player_class, "Class not found"))

def origin_story(player_class):
    stories = {
        'Warrior': "Born in the mountains, you have always been a fighter...",
        'Mage': "From a young age, you were fascinated by the arcane arts...",
        'Rogue': "Growing up on the streets, you learned how to survive in the shadows..."
    }
    return stories.get(player_class, "No story available for this class")

class RPGGame:
    def __init__(self):
        self.db_path = 'game_data.db'
        self.setup_database()
        self.menu()

    def setup_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS Players (player_id TEXT PRIMARY KEY, player_name TEXT NOT NULL, player_class TEXT NOT NULL, health INTEGER, mana INTEGER, strength INTEGER, agility INTEGER, intelligence INTEGER, experience INTEGER DEFAULT 0, level INTEGER DEFAULT 1)''')

    def create_player(self, name, player_class):
        player_id = str(uuid.uuid4())
        attributes = {
            'Warrior': {'health': 200, 'mana': 50, 'strength': 10, 'agility': 5, 'intelligence': 3},
            'Mage': {'health': 100, 'mana': 150, 'strength': 3, 'agility': 5, 'intelligence': 10},
            'Rogue': {'health': 150, 'mana': 100, 'strength': 7, 'agility': 10, 'intelligence': 5}
        }[player_class]
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('INSERT INTO Players (player_id, player_name, player_class, health, mana, strength, agility, intelligence) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (player_id, name, player_class, attributes['health'], attributes['mana'], attributes['strength'], attributes['agility'], attributes['intelligence']))
        return player_id

    def menu(self):
        print("\nWelcome to the RPG Game. What would you like to do?")
        while True:
            print("\n1. Create Character\n2. Play Level\n3. Exit Game")
            choice = input("Choose an option: ")
            if choice == '1':
                self.character_creation()
            elif choice == '2':
                player_id = input("Enter your character's ID: ")
                self.play_level(player_id)
            elif choice == '3':
                self.exit_game()

    def character_creation(self):
        print("Welcome to the character creation wizard!\n")
        player_name = input("Enter your character's name: ")
        print("\nChoose your class:")
        classes = {'1': 'Warrior', '2': 'Mage', '3': 'Rogue'}
        for number, name in classes.items():
            print(f"{number}. {name}")
        class_choice = input("\nEnter the number of your class: ")
        player_class = classes.get(class_choice, 'Warrior')
        print("\nYour Origin Story:")
        print(origin_story(player_class))
        print("\nYour character's ASCII Art:")
        print_ascii_art(player_class)
        player_id = self.create_player(player_name, player_class)
        print(f"\nCharacter created successfully! Name: {player_name}, Class: {player_class}, ID: {player_id}")

    def play_level(self, player_id):
        xp_gain = random.randint(20, 100)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('UPDATE Players SET experience = experience + ? WHERE player_id = ?', (xp_gain, player_id))
            player_info = conn.execute('SELECT player_id, player_name, level, experience FROM Players WHERE player_id = ?', (player_id,)).fetchone()
            print(f"\nPlayer {player_info[1]} (ID: {player_info[0]}) played a level and gained {xp_gain} XP. Congratulations!")
            print(f"Total Experience: {player_info[3]}, Level: {player_info[2]}")

    def exit_game(self):
        # Centralized exit point for the game
        print("Exiting game. Thanks for playing!")
        exit()

if __name__ == "__main__":
    RPGGame()
