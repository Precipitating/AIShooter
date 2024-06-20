import math

import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.transform.rotozoom(pygame.image.load("img/player.png").convert_alpha(), 0, PLAYER_SIZE)
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.speed = PLAYER_SPEED

    def user_input(self):

        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if not self.pos.y < 370:
                self.velocity_y = -self.speed
        if keys[pygame.K_s]:
            if not self.pos.y > 580:
                self.velocity_y = self.speed
        if keys[pygame.K_a]:
            if not self.pos.x < 750:
                self.velocity_x = -self.speed
        if keys[pygame.K_d]:
            if not self.pos.x > 960:
                self.velocity_x = self.speed

        # fix diagonal speed increase
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)



    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)

    def update(self):
        self.user_input()
        self.move()
