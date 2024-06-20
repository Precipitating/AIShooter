import math
import pygame
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("img/enemy.png").convert_alpha(), 0, PLAYER_SIZE)
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.base_player_img = self.image
        self.hitbox_rect = self.base_player_img.get_rect(center=self.pos)
        self.rect = self.hitbox_rect.copy()
        self.rot = 0

    def face_player(self, playerPos):
        # angle between enemy -> player pos
        angle = math.degrees(math.atan2(playerPos.x - self.rect.x, -(playerPos.y - self.rect.y)))
        self.rot = -angle
        self.image = pygame.transform.rotate(self.base_player_img, self.rot)

    def update(self):
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center


def position_in_circle(radius, index):
    angle = CIRCLE_RADIUS * math.pi * index / ENEMY_COUNT
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    return x, y
