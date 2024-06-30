from Bullet import *
import pygame
from settings import *



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("img/player.png").convert_alpha(), 0, PLAYER_SIZE)
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.base_player_img = self.image
        self.hitbox_rect = self.base_player_img.get_rect(center=self.pos)
        self.rect = self.hitbox_rect.copy()
        self.speed = PLAYER_SPEED
        self.rot = 0
        self.shoot = False
        self.shoot_delay = 0
        self.bullets_shot = 0
        self.previous_rotation = 0

    def is_shooting(self):
        if self.shoot_delay <= 0:
            self.previous_rotation = self.rot
            self.bullets_shot += 1
            self.shoot_delay = PLAYER_SHOOT_COOLDOWN
            spawned_bullet_pos = self.pos
            self.bullet = Bullet(spawned_bullet_pos[0], spawned_bullet_pos[1], self.rot, Owner.PLAYER)
            bullet_group.add(self.bullet)
            all_sprites_group.add(self.bullet)

    def player_rotation(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rot -= ROTATE_SPEED
            self.image = pygame.transform.rotate(self.base_player_img, self.rot)
            self.rect = self.image.get_rect(center=self.hitbox_rect.center)

        if keys[pygame.K_LEFT]:
            self.rot += ROTATE_SPEED
            self.image = pygame.transform.rotate(self.base_player_img, self.rot)
            self.rect = self.image.get_rect(center=self.hitbox_rect.center)

    def user_input(self):

        keys = pygame.key.get_pressed()

        self.velocity_x = 0
        self.velocity_y = 0

        if keys[pygame.K_w]:
            if not self.pos.y < 420:
                self.velocity_y = -self.speed
        if keys[pygame.K_s]:
            if not self.pos.y > 655:
                self.velocity_y = self.speed
        if keys[pygame.K_a]:
            if not self.pos.x < 800:
                self.velocity_x = -self.speed
        if keys[pygame.K_d]:
            if not self.pos.x > 1040:
                self.velocity_x = self.speed

        # fix diagonal speed increase
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        # shoot
        if keys[pygame.K_SPACE]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False

    def ai_input(self, left=False, right=False, up=False, down=False, shoot=False):
        self.velocity_x = 0
        self.velocity_y = 0

        if up:
            if not self.pos.y < 420:
                self.velocity_y = -self.speed
        if down:
            if not self.pos.y > 655:
                self.velocity_y = self.speed
        if left:
            if not self.pos.x < 800:
                self.velocity_x = -self.speed
        if right:
            if not self.pos.x > 1040:
                self.velocity_x = self.speed

        # fix diagonal speed increase
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        # shoot
        if shoot:
            self.shoot = True
            self.is_shooting()



        else:
            self.shoot = False

    def ai_rotation(self, left=False, right=False):
        if left:
            self.rot -= ROTATE_SPEED
            self.image = pygame.transform.rotate(self.base_player_img, self.rot)
            self.rect = self.image.get_rect(center=self.hitbox_rect.center)

        if right:
            self.rot += ROTATE_SPEED
            self.image = pygame.transform.rotate(self.base_player_img, self.rot)
            self.rect = self.image.get_rect(center=self.hitbox_rect.center)

        self.rot %= 360


    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def update(self):
        self.ai_input()
        self.ai_rotation()
        self.move()
        if self.shoot_delay > 0:
            self.shoot_delay -= 1
