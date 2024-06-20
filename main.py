import pygame
from sys import exit
import math
from settings import *
from Player import *
from Enemy import *

pygame.init()

# Create Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Impossible Shooter")
clock = pygame.time.Clock()

# Player
player = Player()
# Enemies
enemies = [Enemy() for _ in range(ENEMY_COUNT)]

for i in range(len(enemies)):
    x, y = position_in_circle(CIRCLE_RADIUS, i)
    enemies[i].pos.x += x * 250
    enemies[i].pos.y += y * 250

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

    # Enemy Update
    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect)
        pygame.draw.rect(screen, "green", enemy.hitbox_rect, 2)
        enemy.face_player(playerPos=player.rect)
        enemy.update()

    pygame.display.update()
    clock.tick(FPS)
