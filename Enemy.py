import math
import pygame
from settings import *
from groups import *
from Bullet import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("img/enemy.png").convert_alpha(), 0, PLAYER_SIZE)
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.base_player_img = self.image
        self.hitbox_rect = self.base_player_img.get_rect(center=self.pos)
        self.rect = self.hitbox_rect.copy()
        self.rot = 0
        self.shoot_delay = 0
        self.shoot = True
        self.idx = 0

    def face_player(self, playerPos):
        # angle between enemy -> player pos
        angle = math.degrees(math.atan2(-(playerPos.y - self.rect.y), playerPos.x - self.rect.x))
        self.rot = angle
        self.image = pygame.transform.rotate(self.base_player_img, self.rot)

    def update(self):
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center
        self.is_shooting()

        if self.shoot_delay > 0:
            self.shoot_delay -= 1

    def is_shooting(self):
        if self.shoot_delay <= 0:
            self.shoot_delay = ENEMY_SHOOT_COOLDOWN
            spawned_bullet_pos = self.pos
            self.bullet = Bullet(spawned_bullet_pos[0], spawned_bullet_pos[1], self.rot, Owner.ENEMY)
            bullet_group.add(self.bullet)
            all_sprites_group.add(self.bullet)


def position_in_circle(radius, index):
    angle = CIRCLE_RADIUS * math.pi * index / ENEMY_COUNT
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    return x, y
