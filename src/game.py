import pygame
from settings import *
from states.menu import Menu
from states.gameplay import Gameplay

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.state = Menu(self)

    def change_state(self, new_state):
        self.state = new_state

    def run(self):
        running = True

        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.state.handle_event(event)

            self.state.update()
            self.state.draw(self.screen)

            pygame.display.update()