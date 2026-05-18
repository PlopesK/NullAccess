import pygame
from settings import *
from states.gameplay import Gameplay

class Menu:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.change_state(Gameplay(self.game))
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(BLACK)

        title = FONT_BIG.render("ACCESS://NULL", True, NEON_GREEN)
        text = FONT_MEDIUM.render("SPACE - START / WASD - MOVE", True, WHITE)
        esc = FONT_MEDIUM.render("ESC - QUIT", True, WHITE)

        screen.blit(title, (450, 250))
        screen.blit(text, (350, 350))
        screen.blit(esc, (350, 400))