class Frog:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size
        self.hunger = 0
        self.energy = 10
    
    def ribbit(self):
        print(f"{self.name} says ribbit!")
        self.hunger += 1
    
    def jump(self):
        height = ""

        if self.size.lower() == "small":
            height = "a little"
        
        elif self.size.lower() == "medium":
            height = "quite high"
        
        else:
            height = "into the stars, never to be seen again"
        
        print(f"{self.name} jumps {height}!")
        self.energy -= 2
        self.hunger += 1
    
    def eat(self, flies):
        self.hunger -= flies
        print(f"{self.name} ate {flies} flies.")
    
    def sleep(self):
        print(f"Shh... {self.name} is sleeping...")
        self.energy = 10
    
    def status(self):
        print(f"{self.name} - {self.size.upper()} {self.color.upper()} frog\nEnergy: {self.energy} | Hunger: {self.hunger}")

frog = Frog("Jim", "green", "big")

frog.status()
frog.ribbit()
frog.jump()
frog.status()
frog.eat(2)
frog.status()
frog.sleep()
frog.status()