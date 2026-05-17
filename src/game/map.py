import pygame
import random
import math
from settings import *

TILE_SIZE = 48
ENEMY_BORDER_MARGIN = 200

class Map:
    def __init__(self, width, height):
        self.walls = []
        self.datafiles = []
        self.enemies_spawns = []

        self.exit_rect = None
        self.player_spawn = (0, 0)

        self.width = width
        self.height = height

        self.grid_width = math.ceil(self.width / TILE_SIZE)
        self.grid_height = math.ceil(self.height / TILE_SIZE)

        self.generate()

    # -----------------------------
    # util
    # -----------------------------
    def is_border(self, x, y):
        return x == 0 or y == 0 or x == self.grid_width - 1 or y == self.grid_height - 1

    def generate(self):

        grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]

        # 1. bordas = paredes
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.is_border(x, y):
                    grid[y][x] = 1

        # 2. paredes aleatórias internas
        for _ in range(int(self.grid_width * self.grid_height * 0.15)):
            x = random.randint(1, self.grid_width - 2)
            y = random.randint(1, self.grid_height - 2)
            grid[y][x] = 1

        # 3. spawn seguro do player
        while True:
            px = random.randint(1, self.grid_width - 2)
            py = random.randint(1, self.grid_height - 2)

            if grid[py][px] == 0:
                self.player_spawn = (px * TILE_SIZE, py * TILE_SIZE)
                break

        # 4. saída (longe do player)
        while True:
            ex = random.randint(1, self.grid_width - 2)
            ey = random.randint(1, self.grid_height - 2)

            if grid[ey][ex] == 0:
                self.exit_rect = pygame.Rect(
                    ex * TILE_SIZE,
                    ey * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )
                break

        # 5. datafiles
        self.datafiles = []

        for _ in range(5):
            while True:
                dx = random.randint(1, self.grid_width - 2)
                dy = random.randint(1, self.grid_height - 2)

                if grid[dy][dx] == 0:
                    rect = pygame.Rect(
                        dx * TILE_SIZE + 10,
                        dy * TILE_SIZE + 10,
                        28,
                        28
                    )

                    self.datafiles.append(type("D", (), {"rect": rect, "collected": False}))
                    break

        # 6. inimigos (até 2)
        self.enemies_spawns = []

        min_distance_player = 250
        enemy_min_distance = 200

        for _ in range(2):
            while True:
                margin_tiles = ENEMY_BORDER_MARGIN // TILE_SIZE

                ex = random.randint(
                    margin_tiles,
                    self.grid_width - margin_tiles - 1
                )

                ey = random.randint(
                    margin_tiles,
                    self.grid_height - margin_tiles - 1
                )

                x = ex * TILE_SIZE
                y = ey * TILE_SIZE

                # precisa ser chão
                if grid[ey][ex] != 0:
                    continue

                # distância do player
                px, py = self.player_spawn
                dist_player = ((x - px) ** 2 + (y - py) ** 2) ** 0.5

                if dist_player < min_distance_player:
                    continue

                # distância de outros inimigos
                too_close = False
                for sx, sy in self.enemies_spawns:
                    dist_enemy = ((x - sx) ** 2 + (y - sy) ** 2) ** 0.5
                    if dist_enemy < enemy_min_distance:
                        too_close = True
                        break

                if too_close:
                    continue

                self.enemies_spawns.append((x, y))
                break

        # 7. construir paredes
        self.walls = []

        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if grid[y][x] == 1:
                    self.walls.append(
                        pygame.Rect(
                            x * TILE_SIZE,
                            y * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE
                        )
                    )

    def all_collected(self):
        return all(df.collected for df in self.datafiles)

    def draw(self, screen):

        for wall in self.walls:
            pygame.draw.rect(screen, (25, 35, 55), wall)

        for df in self.datafiles:
            if not df.collected:
                pygame.draw.rect(screen, (0, 200, 255), df.rect)

        # COR DA SAÍDA
        if self.all_collected():
            color = (0, 255, 120)  # verde (liberada)
        else:
            color = (255, 80, 80)  # vermelho (bloqueada)

        pygame.draw.rect(screen, color, self.exit_rect)