import pygame
import random
pygame.init()

#Screen setup

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
bg_img =  pygame.image.load("Monopoly_bg.png")

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

screen.blit(bg_img, (0,0))
pygame.display.flip()


pygame.quit()