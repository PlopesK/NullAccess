import pygame

from settings import *
from game.player import Player
from game.map import Map
from states.victory import Victory

class Gameplay:
    def __init__(self, game):

        self.game = game

        self.map = Map()

        self.player = Player()

        self.player.rect.x = self.map.player_spawn[0]
        self.player.rect.y = self.map.player_spawn[1]

        self.font = pygame.font.SysFont(
            "consolas",
            28
        )

        self.collected_files = 0

        self.total_files = len(
            self.map.datafiles
        )

    def handle_event(self, event):
        pass

    def collect_files(self):

        for datafile in self.map.datafiles:

            if not datafile.collected:

                if self.player.rect.colliderect(
                    datafile.rect
                ):

                    datafile.collected = True

                    self.collected_files += 1

    def update(self):

        self.player.update(
            self.map.walls
        )

        self.collect_files()

        self.check_victory()

    def check_victory(self):

        if self.collected_files == self.total_files:

            if self.player.rect.colliderect(
                self.map.exit_rect
            ):

                self.game.change_state(
                    Victory(self.game)
                )

    def draw(self, screen):

        screen.fill((15, 15, 25))

        self.map.draw(screen)

        self.player.draw(screen)

        hud = self.font.render(
            f"FILES: {self.collected_files}/{self.total_files}",
            True,
            WHITE
        )

        screen.blit(hud, (20, 20))