import pygame
import random

from utils.paths import resource_path
from settings import *
from states.gameplay import Gameplay


class Menu:
    def __init__(self, game):
        self.game = game

        self.monitor_img = pygame.image.load(resource_path("assets/ui/logo.png")).convert_alpha()
        self.monitor_img = pygame.transform.scale(self.monitor_img, (698, 275))

        self.noise_timer = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.change_state(Gameplay(self.game))
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

    def update(self):
        self.noise_timer += 1

    # -------------------------
    # NOISE (background effect)
    # -------------------------
    def draw_noise(self, screen):
        noise = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)

        for _ in range(1500):  # reduzido pra performance
            x = random.randint(0, self.game.width - 1)
            y = random.randint(0, self.game.height - 1)

            gray = random.randint(40, 160)
            alpha = random.randint(2, 12)
            noise.fill((gray, gray, gray, alpha), (x, y, 2, 2))

        screen.blit(noise, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    # -------------------------
    # DRAW
    # -------------------------
    def draw(self, screen):
        screen.fill(BLACK)

        self.draw_noise(screen)

        # centro da tela
        screen_rect = screen.get_rect()
        monitor_rect = self.monitor_img.get_rect(center=screen_rect.center)

        cx, cy = monitor_rect.center

        # ajuste fino da "tela interna do monitor"
        screen_x = cx
        screen_y = cy - 13

        # -------------------------
        # desenha monitor
        # -------------------------
        screen.blit(self.monitor_img, monitor_rect)

        # -------------------------
        # texto dentro do monitor
        # -------------------------
        title = FONT_BIG.render("ACCESS://NULL", True, NEON_GREEN)
        title_rect = title.get_rect(center=(screen_x, screen_y - 17))
        screen.blit(title, title_rect)

        # -------------------------
        # textos fora do monitor (mas alinhados a ele)
        # -------------------------
        text = FONT_MEDIUM.render("SPACE - START / WASD - MOVE", True, WHITE)
        esc = FONT_MEDIUM.render("ESC - QUIT", True, WHITE)

        text_rect = text.get_rect(center=(screen_x, screen_y + 120))
        esc_rect = esc.get_rect(center=(screen_x, screen_y + 170))

        screen.blit(text, text_rect)
        screen.blit(esc, esc_rect)