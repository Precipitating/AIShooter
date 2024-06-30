from sys import exit
from Player import *
from Enemy import *
from groups import *
import neat
import time


class Game:
    def __init__(self):
        pygame.init()
        self.comic_sans = pygame.font.SysFont('Comic Sans MS', 100)

        # Create Window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Impossible Shooter")
        self.clock = pygame.time.Clock()

        self.player = None
        self.enemies = None
        self.game_over = False
        self.win = False
        self.start_time = time.time()

        self.reset()

    # initialize default variables
    def reset(self):
        player_group.empty()
        all_sprites_group.empty()
        bullet_group.empty()
        enemy_group.empty()
        enemies_killed_list.clear()

        # Player
        self.player = Player()
        # Enemies
        self.enemies = [Enemy() for _ in range(ENEMY_COUNT)]

        all_sprites_group.add(self.player)
        player_group.add(self.player)

        # setup enemy circle positioning & unique shoot delay
        delay_offset = ENEMY_DELAY
        for i in range(len(self.enemies)):
            x, y = position_in_circle(CIRCLE_RADIUS, i)
            self.enemies[i].pos.x += x * 250
            self.enemies[i].pos.y += y * 250
            self.enemies[i].idx = i
            self.enemies[i].shoot_delay += delay_offset
            delay_offset += ENEMY_DELAY
            all_sprites_group.add(self.enemies[i])
            enemy_group.add(self.enemies[i])

    def calculate_fitness(self, genome1):
        end_time = time.time()
        current_enemy_idx = 0
        correct_kill_increase = 50

        # if nothing done, negate fitness
        if len(enemies_killed_list) == 0:
            genome1.fitness += -100
            if self.player.rot == 0 and self.player.bullets_shot == 0:
                genome1.fitness += -100

        # time survived
        genome1.fitness += (end_time - self.start_time)


        # check if killed in correct order, else negate the enemy idx from target idx
        for kill_idx in enemies_killed_list:
            if kill_idx == current_enemy_idx:
                current_enemy_idx += 1
                genome1.fitness += correct_kill_increase
                correct_kill_increase += 50
            else:
                genome1.fitness += (current_enemy_idx - kill_idx) * 2

        # accuracy
        if self.player.bullets_shot > 0:
            genome1.fitness += len(enemies_killed_list) / self.player.bullets_shot

        genome1.fitness = round(genome1.fitness, 1)

        print(genome1.fitness)

    def train_ai(self, genome1, config):
        start_time = time.time()
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        run = True

        # Game State
        while run:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        if self.game_over or self.win:
                            self.reset()
                            self.game_over = False
                            self.win = False

            enemy_pos_x = 0
            enemy_pos_y = 0
            angle = 0
            for enemy in enemy_group:
                enemy_pos_x = enemy.pos.x
                enemy_pos_y = enemy.pos.y

                math.atan2(-(self.player.pos.y - enemy.pos.y), -(self.player.pos.x - enemy.pos.x))
                angle -= self.player.rot
                angle %= 360
                break

            output = net1.activate((self.player.pos.x, self.player.pos.y, self.player.rot, len(enemy_group),
                                    enemy_pos_x, enemy_pos_y, self.player.bullets_shot, angle))

            decision = output.index(max(output))
            if decision == 0:
                pass
            elif decision == 1:
                self.player.ai_rotation(left=True)
            elif decision == 2:
                self.player.ai_rotation(right=True)
            elif decision == 3:
                self.player.ai_rotation(left=True)
                self.player.ai_input(shoot=True)
            elif decision == 4:
                self.player.ai_rotation(right=True)
                self.player.ai_input(shoot=True)
            else:
                self.player.ai_input(shoot=True)

            self.check_status()
            self.screen.fill((0, 0, 0))

            # GAME LOOP
            if self.game_over:
                self.game_over_screen()
                self.calculate_fitness(genome1)
                break
            elif self.win:
                self.win_screen()
                self.calculate_fitness(genome1)
                break
            else:
                # MAIN LOOP
                pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(770, 400, 300, 300), 2)
                pygame.draw.rect(self.screen, "green", self.player.hitbox_rect, 2)

                all_sprites_group.draw(self.screen)
                all_sprites_group.update()

                # Enemy face player
                for enemy in self.enemies:
                    pygame.draw.rect(self.screen, "green", enemy.hitbox_rect, 2)
                    enemy.face_player(playerPos=self.player.rect)

            pygame.display.update()
            self.clock.tick(FPS)

    def play(self):
        # Game State
        while True:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        if self.game_over or self.win:
                            self.reset()
                            self.game_over = False
                            self.win = False

            self.check_status()
            self.screen.fill((0, 0, 0))

            # GAME LOOP
            if self.game_over:
                self.game_over_screen()
            elif self.win:
                self.win_screen()
            else:
                # MAIN LOOP
                pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(770, 400, 300, 300), 2)
                pygame.draw.rect(self.screen, "green", self.player.hitbox_rect, 2)

                all_sprites_group.draw(self.screen)
                all_sprites_group.update()

                # Enemy face player
                for enemy in self.enemies:
                    pygame.draw.rect(self.screen, "green", enemy.hitbox_rect, 2)
                    enemy.face_player(playerPos=self.player.rect)

            pygame.display.update()
            self.clock.tick(FPS)

    def game_over_screen(self):
        text_surface = self.comic_sans.render('Game Over', True, (255, 255, 255))
        self.screen.blit(text_surface, (650, 300))
        text_surface = self.comic_sans.render('Press Enter to restart', True, (255, 255, 255))
        self.screen.blit(text_surface, (450, 500))

    def win_screen(self):
        text_surface = self.comic_sans.render('You Won!', True, (255, 255, 255))
        self.screen.blit(text_surface, (650, 300))
        text_surface = self.comic_sans.render('Press Enter to restart', True, (255, 255, 255))
        self.screen.blit(text_surface, (450, 500))

    def check_status(self):
        # if dead
        if len(player_group) == 0 and not self.game_over:
            self.game_over = True
        # if win
        if len(player_group) == 1 and len(enemy_group) == 0:
            self.win = True

    def render(self):

        all_sprites_group.draw(self.screen)

    def update(self):
        # if dead
        if len(player_group) == 0 and not self.game_over:
            self.game_over = True
        # if win
        if len(player_group) == 1 and len(enemy_group) == 0:
            self.win = True

        # GAME LOOP
        if self.game_over:
            text_surface = self.comic_sans.render('Game Over', True, (255, 255, 255))
            self.screen.blit(text_surface, (650, 300))
            text_surface = self.comic_sans.render('Press Enter to restart', True, (255, 255, 255))
            self.screen.blit(text_surface, (450, 500))
        elif self.win:
            text_surface = self.comic_sans.render('You Won!', True, (255, 255, 255))
            self.screen.blit(text_surface, (650, 300))
            text_surface = self.comic_sans.render('Press Enter to restart', True, (255, 255, 255))
            self.screen.blit(text_surface, (450, 500))
        else:
            # MAIN LOOP
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(770, 400, 300, 300), 2)
            pygame.draw.rect(self.screen, "green", self.player.hitbox_rect, 2)
        all_sprites_group.update()
