import pygame
from settings import *

class Gameplay:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_state(None)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((20, 20, 30))