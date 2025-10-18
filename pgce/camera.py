import pygame
import pygame.camera
import os

pygame.init()
pygame.camera.init()

cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])

cam.start()

window = pygame.display.set_mode((1280, 720), pygame.NOFRAME)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                image = cam.get_image()
                filename = len(os.listdir())
                pygame.image.save(image, f"capture{filename}.png")
    
    camera_frame = cam.get_image()

    window.blit(camera_frame, (0, 0))

    pygame.display.update()