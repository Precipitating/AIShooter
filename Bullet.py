import pygame
import math
from settings import *
from groups import *
from enum import Enum


class Owner(Enum):
    NONE = 0
    PLAYER = 1
    ENEMY = 2


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, owner):
        super().__init__()
        self.owner = owner
        self.image = pygame.image.load("img/bullet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.speed = BULLET_SPEED
        self.angle = angle
        self.x_vel = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
        self.y_vel = -math.sin(self.angle * (2 * math.pi / 360)) * self.speed
        self.bullet_lifetime = BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks()  # get creation time of bullet spawn

    def bullet_move(self):
        self.x += self.x_vel
        self.y += self.y_vel

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

    def bullet_hit(self):
        if self.owner == Owner.PLAYER:
            if pygame.sprite.spritecollide(self, enemy_group, True):
                self.kill()
        elif self.owner == Owner.ENEMY:
            if pygame.sprite.spritecollide(self, player_group, True):
                self.kill()

    def update(self):
        self.bullet_move()
        self.bullet_hit()
