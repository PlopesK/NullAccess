import pygame

from settings import *
from game.datafiles import DataFile

TILE_SIZE = 64

MAP = [
    "####################",
    "#....D............E#",
    "#..######..........#",
    "#..#......D........#",
    "#..#.....P.........#",
    "#.........D...######",
    "####################"
]

class Map:
    def __init__(self):
        self.walls = []

        self.datafiles = []

        self.exit_rect = None

        self.player_spawn = (300, 300)

        self.generate_map()

    def generate_map(self):

        for row_index, row in enumerate(MAP):

            for col_index, tile in enumerate(row):

                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if tile == "#":

                    wall = pygame.Rect(
                        x,
                        y,
                        TILE_SIZE,
                        TILE_SIZE
                    )

                    self.walls.append(wall)

                elif tile == "D":

                    datafile = DataFile(
                        x + 16,
                        y + 16
                    )

                    self.datafiles.append(datafile)

                elif tile == "E":

                    self.exit_rect = pygame.Rect(
                        x,
                        y,
                        TILE_SIZE,
                        TILE_SIZE
                    )

                elif tile == "P":

                    self.player_spawn = (
                        x + 12,
                        y + 12
                    )

    def draw(self, screen):

        for wall in self.walls:

            pygame.draw.rect(
                screen,
                (25, 35, 55),
                wall
            )

        for datafile in self.datafiles:
            datafile.draw(screen)

        color = (255, 50, 50)

        all_collected = all(
            datafile.collected
            for datafile in self.datafiles
        )

        if all_collected:
            color = (0, 255, 120)

        pygame.draw.rect(
            screen,
            color,
            self.exit_rect
        )