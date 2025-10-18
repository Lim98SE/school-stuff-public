import pygame
import random

from advisors import *

window = pygame.display.set_mode((960, 540))
clock = pygame.time.Clock()

G_mult = 1
G_bonus = 0

class Advisor:
    def __init__(self, name, ability, config = {}):
        self.name = name
        self.ability = ability
        self.vars = config
    
    def calculate(self):
        output = {}
        global G_mult
        global G_bonus
        G_mult += 0 if output.get("mult") == None else output.get("mult")
        G_mult *= 0 if output.get("xmult") == None else output.get("xmult")

advisors = [
    Advisor("Cool Guy", basic_advisor, {})
]

class Stock:
    def __init__(self, index, name):
        self.id = index
        self.name = name
        self.price = 500
        self.trend = 0
        self.reroll()
        self.calculate()
    
    def calculate(self):
        self.price += self.trend
    
    def sell(self):
        global G_mult
        global G_bonus

        sell_price = self.price
        
        G_mult = 1
        G_bonus = 0
        
        for i in advisors:
            i.calculate()
        
        return (G_bonus + sell_price) * G_mult
    
    def reroll(self):
        spike = random.randint(0, 10) == 0
        super_spike = (random.randint(0, 10) == 0) and spike

        self.trend = random.randint(-50, 50)

        if spike:
            self.trend *= 10
        
        if super_spike:
            self.trend *= 10

stocks = []

for i in range(5):
    stocks.append(Stock(i, f"${i}"))

for i in stocks:
    print(i.name, i.price)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill("#000000")

    pygame.display.update()

    clock.tick(60)

pygame.quit()