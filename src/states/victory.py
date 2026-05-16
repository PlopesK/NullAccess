import pygame

from settings import *

class Victory:
    def __init__(self, game):

        self.game = game

        self.font_big = pygame.font.SysFont(
            "consolas",
            64
        )

        self.font_small = pygame.font.SysFont(
            "consolas",
            28
        )

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                from states.menu import Menu

                self.game.change_state(
                    Menu(self.game)
                )

    def update(self):
        pass

    def draw(self, screen):

        screen.fill((10, 20, 10))

        title = self.font_big.render(
            "SYSTEM BREACHED",
            True,
            NEON_GREEN
        )

        text = self.font_small.render(
            "SPACE - RETURN TO MENU",
            True,
            WHITE
        )

        screen.blit(title, (320, 280))
        screen.blit(text, (410, 380))