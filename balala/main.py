import pygame

canvas = pygame.display.set_mode((640, 360))

window = pygame.display.set_mode((1280, 720))

pygame.display.set_caption("Balatreal")

clock = pygame.time.Clock()

running = True

ante = 1
chips = 0
mult = 0
blind = "SMALL"
required_chips = 300

hand_size = 8
deck = []

jokers = []
hand = []

hand_ids = [
    "HIGH_CARD",
    "PAIR",
    "TWO_PAIR",
    "THREE_OF_A_KIND",
    "FLUSH",
    "FULL_HOUSE",
    "FOUR_OF_A_KIND",
    "STRAIGHT_FLUSH",
    "FIVE_OF_A_KIND",
    "FLUSH_FIVE",
]

# 10 hands

hand_levels = [
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1
]

played_hands = [
    0, 0, 0, 0, 0,
    0, 0, 0, 0 ,0
]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    canvas.fill("#35795e")

    window.blit(pygame.transform.scale(canvas, window.get_size()))

    pygame.display.update()

    clock.tick(60)

running = False