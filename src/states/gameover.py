import pygame
from settings import *
from states.menu import Menu

class GameOver:
    def __init__(self, game):

        self.game = game

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                self.game.change_state(Menu(self.game))
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit

    def update(self):
        pass

    def draw(self, screen):

        screen.fill((30, 0, 0))

        title = FONT_BIG.render(
            "SYSTEM COMPROMISED",
            True,
            (255, 80, 80)
        )

        text = FONT_MEDIUM.render(
            "SPACE - RETURN TO MENU",
            True,
            (255, 255, 255)
        )

        esc = FONT_MEDIUM.render(
            "ESC - QUIT", 
            True, 
            (255, 255, 255)
        )

        screen.blit(title, (250, 280))
        screen.blit(text, (360, 380))
        screen.blit(esc, (360, 420))