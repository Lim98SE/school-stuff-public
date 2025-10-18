class GardenBox:
    def __init__(self):
        self.plants = 0
    
    def plant(self):
        self.plants += 1
    
    def water(self):
        print(f"Watered {self.plants} plants.")
    
    def harvest(self):
        self.plants -= 1

box = GardenBox()
box.plant()
box.plant()
box.plant()
box.water()
box.harvest()
box.water()


