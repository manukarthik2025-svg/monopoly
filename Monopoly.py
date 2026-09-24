import pygame
import random
pygame.init()
#Screen setup
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

bg_img = pygame.image.load("images/Monopoly_bg.png")
screen.blit(bg_img, (0,0))