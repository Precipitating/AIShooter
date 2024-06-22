import pygame
from sys import exit
import math
from settings import *
from Player import *
from Enemy import *
from groups import *

pygame.init()
comic_sans = pygame.font.SysFont('Comic Sans MS', 100)

# Create Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Impossible Shooter")
clock = pygame.time.Clock()

player = None
enemies = None


def reset():
    player_group.empty()
    all_sprites_group.empty()
    bullet_group.empty()
    enemy_group.empty()

    # Player
    global player
    player = Player()
    global enemies
    # Enemies
    enemies = [Enemy() for _ in range(ENEMY_COUNT)]

    all_sprites_group.add(player)
    player_group.add(player)

    # setup enemy circle positioning & unique shoot delay
    delay_offset = 100
    for i in range(len(enemies)):
        x, y = position_in_circle(CIRCLE_RADIUS, i)
        enemies[i].pos.x += x * 250
        enemies[i].pos.y += y * 250
        enemies[i].shoot_delay += delay_offset
        delay_offset += 100
        all_sprites_group.add(enemies[i])
        enemy_group.add(enemies[i])


reset()
# Game State
game_over = False
win = False
while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                if game_over or win:
                    reset()
                    game_over = False
                    win = False
    # if dead
    if len(player_group) == 0 and not game_over:
        game_over = True
    # if win
    if len(player_group) == 1 and len(enemy_group) == 0:
        win = True

    screen.fill((0, 0, 0))

    if game_over:
        text_surface = comic_sans.render('Game Over', True, (255, 255, 255))
        screen.blit(text_surface, (650, 300))
        text_surface = comic_sans.render('Press Enter to restart', True, (255, 255, 255))
        screen.blit(text_surface, (450, 500))
    elif win:
        text_surface = comic_sans.render('You Won!', True, (255, 255, 255))
        screen.blit(text_surface, (650, 300))
        text_surface = comic_sans.render('Press Enter to restart', True, (255, 255, 255))
        screen.blit(text_surface, (450, 500))
    else:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(770, 400, 300, 300), 2)
        pygame.draw.rect(screen, "green", player.hitbox_rect, 2)

        all_sprites_group.draw(screen)
        all_sprites_group.update()

        # Enemy Update
        for enemy in enemies:
            pygame.draw.rect(screen, "green", enemy.hitbox_rect, 2)
            enemy.face_player(playerPos=player.rect)

    pygame.display.update()
    clock.tick(FPS)
