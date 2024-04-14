import sqlite3
import random
import uuid

class RPGGame:
    def __init__(self, db_path='game_data.db'):
        self.db_path = db_path
        self.player_id = None
        self.setup_database()

    def setup_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS Players (
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
            )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS Items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                effect TEXT NOT NULL,
                value INTEGER
            )''')

    def run(self):
        while True:
            if self.player_id:
                self.show_menu()
            else:
                self.show_initial_menu()

    def show_initial_menu(self):
        print("\nWelcome to the RPG Game. What would you like to do?")
        print("1. Create Character\n2. Exit Game")
        choice = input("Choose an option: ")
        if choice == '1':
            self.create_character()
        elif choice == '2':
            exit()

    def show_menu(self):
        print("\n1. Start Adventure\n2. Show Inventory\n3. Visit Shop\n4. Exit Game")
        choice = input("Choose an option: ")
        if choice == '1':
            self.start_adventure()
        elif choice == '2':
            self.show_inventory()
        elif choice == '3':
            self.visit_shop()
        elif choice == '4':
            exit()

    def create_character(self):
        name = input("Enter your character's name: ")
        print("Choose your class:\n1. Warrior\n2. Mage\n3. Rogue")
        classes = {'1': 'Warrior', '2': 'Mage', '3': 'Rogue'}
        class_choice = input("Enter the number of your class: ")
        player_class = classes.get(class_choice, 'Warrior')
        player_id = str(uuid.uuid4())
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''INSERT INTO Players (player_id, player_name, player_class)
                            VALUES (?, ?, ?)''', (player_id, name, player_class))
        self.player_id = player_id
        print(f"Character created successfully! Name: {name}, Class: {player_class}, ID: {player_id}")

    def start_adventure(self):
        event = random.choice(['monster', 'treasure', 'nothing'])
        if event == 'monster':
            print("A wild monster appears!")
            # Here you would implement the combat logic
        elif event == 'treasure':
            print("You found a hidden treasure chest!")
            # Logic to add gold or items to the player's inventory
        else:
            print("It's a quiet day in the forest.")

    def show_inventory(self):
        with sqlite3.connect(self.db_path) as conn:
            player_info = conn.execute('SELECT gold FROM Players WHERE player_id = ?', (self.player_id,)).fetchone()
        print(f"You currently have {player_info[0]} gold.")

    def visit_shop(self):
        print("Welcome to the shop. What would you like to do?")
        print("1. Buy Items\n2. Sell Items\n3. Exit Shop")
        choice = input("Choose an option: ")
        if choice == '1':
            self.buy_items()
        elif choice == '2':
            self.sell_items()
        elif choice == '3':
            return

    def buy_items(self):
        with sqlite3.connect(self.db_path) as conn:
            items = conn.execute('SELECT item_id, name, effect, value FROM Items').fetchall()
            for item in items:
                print(f"{item[0]}: {item[1]} - {item[2]} (Cost: {item[3]} gold)")
            item_id = int(input("Enter the ID of the item you want to buy: "))
            item = conn.execute('SELECT name, value FROM Items WHERE item_id = ?', (item_id,)).fetchone()
            player_gold = conn.execute('SELECT gold FROM Players WHERE player_id = ?', (self.player_id,)).fetchone()[0]
            if player_gold >= item[1]:
                conn.execute('UPDATE Players SET gold = gold - ? WHERE player_id = ?', (item[1], self.player_id))
                print(f"You purchased {item[0]} for {item[1]} gold.")
            else:
                print("You do not have enough gold to purchase this item.")

    def sell_items(self):
        # Implement selling items logic here
        pass

if __name__ == "__main__":
    game = RPGGame()
    game.run()
