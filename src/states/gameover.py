import pygame
from settings import *
from states.menu import Menu

class GameOver:
    def __init__(self, game):

        self.game = game

        self.font_big = pygame.font.SysFont("consolas", 64)
        self.font_small = pygame.font.SysFont("consolas", 28)

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                self.game.change_state(Menu(self.game))
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

    def update(self):
        pass

    def draw(self, screen):

        screen.fill((30, 0, 0))

        title = self.font_big.render(
            "SYSTEM COMPROMISED",
            True,
            (255, 80, 80)
        )

        text = self.font_small.render(
            "SPACE - RETURN TO MENU",
            True,
            (255, 255, 255)
        )

        esc = self.font_small.render(
            "ESC - QUIT", 
            True, 
            (255, 255, 255)
        )

        screen.blit(title, (250, 280))
        screen.blit(text, (360, 380))
        screen.blit(esc, (360, 420))