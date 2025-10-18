import json
import os
import random

def menu_info():
    print("""
1. Show Inventory
2. Add A Game
3. Remove A Game
4. Make Sale
5. Check Availability
6. Save to inventory.json
7. Quit
          """.strip())
    
    ch = input("? ").strip()

    if ch.isdigit():
        return int(ch)
    
    else:
        print(f"{ch} is not a viable choice.")

running = True
choice = 0
sale_multiplier = 0.75

class Console:
    def __init__(self, name, company, release_year, uuid):
        self.name = name
        self.company = company
        self.year = release_year
        self.uuid = uuid

class Game:
    def __init__(self, title, publisher, release_year, console: Console, price, onsale = False):
        self.title = title
        self.publisher = publisher
        self.year = release_year
        self.console = console
        self.price = price
        self.onsale = onsale
    
    def info(self):
        print(f"{self.title}: released {self.year} by {self.publisher} on {self.console.name} (Price is ${str(self.price * (sale_multiplier if self.onsale else 1)).zfill(2)})")
    
    def serialize(self):
        return {
            "title": self.title,
            "publisher": self.publisher,
            "year": self.year,
            "console": self.console.uuid,
            "price": self.price,
            "onsale": self.onsale
        }

consoles = {
    "wii": Console("Wii", "Nintendo", 2006, "wii"),
    "ps3": Console("PlayStation 3", "Sony", 2006, "ps3"),
    "ds": Console("DS", "Nintendo", 2004, "ds"),
    "360": Console("XBOX 360", "Microsoft", 2005, "360"),
    "psp": Console("PlayStation Portable", "Sony", 2005, "psp")
}

def add_game():
    title = input("Title: ").strip()
    publisher = input("Publisher: ").strip()
    year = input("Year: ").strip()

    if year.isdigit():
        year = int(year)
    
    else:
        print(f"Error: invalid year {year}")
        return None
    
    console = ""

    while not console in consoles.keys():
        print("Available consoles:")

        for i in consoles.keys():
            print(f"{i} : {consoles[i].name}")

        print("Type what coes BEFORE the colon (:) character.")

        console = input("? ").strip()
    
    console = consoles[console]
    
    price = input("Price: ")

    try:
        price = float(price)
    
    except:
        print(f"Error: invalid price {price}")
        return None

    return Game(title, publisher, year, console, price)

inventory = []

serialzed = []

if os.path.exists("inventory.json"):
    with open("inventory.json") as file:
        serialzed = json.load(file)
    
    for i in serialzed:
        game = Game(
            i["title"],
            i["publisher"],
            i["year"],
            consoles[i["console"]],
            i["price"],
            i["onsale"]
        )

        inventory.append(game)

inventory = sorted(inventory, key=lambda x: x.title)

while running:
    choice = menu_info()

    if choice == 1:
        for i in inventory:
            i.info()

    if choice == 2: # Show inventory
        inventory.append(add_game())
        inventory = sorted(inventory, key=lambda x: x.title)
    
    if choice == 3: # Remove a game
        to_remove = input("? ").strip()
        buffer = inventory.copy()

        for i in inventory:
            if i.title.lower() == to_remove.lower():
                print(f"Removing {i.title} ({i.console.name})")
                buffer.remove(i)
        
        inventory = buffer.copy()
        inventory = sorted(inventory, key=lambda x: x.title)
    
    if choice == 4: # Make random sale
        games = input("How many games do you want to put on sale? ").strip()

        try:
            games = int(games)
        
        except:
            print(f"{games} is not a valid number.")
            continue

        for i in inventory:
            i.onsale = False

        buffer = inventory.copy()
        games_onsale = 0

        if games > len(inventory):
            games = len(inventory)

        put_onsale = []

        while games_onsale < games:
            index = random.randint(0, len(inventory) - 1)

            if not buffer[index].onsale:
                buffer[index].onsale = True
                put_onsale.append(index)
                games_onsale += 1
        
        inventory = buffer.copy()
        inventory = sorted(inventory, key=lambda x: x.title)

        for i in put_onsale:
            inventory[i].info()

    elif choice == 5: # check availability
        check = input("? ").strip().lower()

        for i in inventory:
            if check in i.title.lower():
                i.info()
                continue

            if check in i.publisher.lower():
                i.info()
                continue

            if check in i.console.name.lower():
                i.info()
                continue

    elif choice == 6: # Serialize
        serialzed = []

        inventory = sorted(inventory, key=lambda x: x.title)

        for i in inventory:
            serialzed.append(i.serialize())

        with open("inventory.json", "w") as file:
            json.dump(serialzed, file)
        
        print("Dumped!")

    elif choice == 7:
        running = False
        break
