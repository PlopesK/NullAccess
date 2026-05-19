import pygame

from settings import *

class Victory:
    def __init__(self, game):

        self.game = game

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                from states.menu import Menu
                self.game.change_state(Menu(self.game))
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit

    def update(self):
        pass

    def draw(self, screen):

        screen.fill((10, 20, 10))

        title = FONT_BIG.render(
            "SYSTEM BREACHED",
            True,
            NEON_GREEN
        )

        text = FONT_MEDIUM.render(
            "SPACE - RETURN TO MENU",
            True,
            WHITE
        )

        esc = FONT_MEDIUM.render(
            "ESC - QUIT",
            True,
            WHITE
        )

        screen.blit(title, (320, 280))
        screen.blit(text, (410, 380))
        screen.blit(esc, (410, 420))