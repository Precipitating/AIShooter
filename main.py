import pygame
from sys import exit
import math
from settings import *
from Player import *

pygame.init()

# Create Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Impossible Shooter")
clock = pygame.time.Clock()

# Player
player = Player()

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(770, 400, 300, 300), 2)
    screen.blit(player.image, player.rect)
    player.update()
    pygame.draw.rect(screen, "green", player.hitbox_rect, 2)

    pygame.display.update()
    clock.tick(FPS)
