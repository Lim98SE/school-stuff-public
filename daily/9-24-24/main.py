class Pumpkin:
    def __init__(self, color, weight):
        self.color = color
        self.weight = weight
    
    def status(self):
        print(f"{self.color} {self.weight}lbs pumpkin")