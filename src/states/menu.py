import pygame
from settings import *
from states.gameplay import Gameplay

class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("consolas", 40)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.change_state(Gameplay(self.game))

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(BLACK)

        title = self.font.render("ACCESS://NULL", True, NEON_GREEN)
        text = self.font.render("SPACE - START / WASD - MOVE", True, WHITE)

        screen.blit(title, (450, 250))
        screen.blit(text, (350, 350))