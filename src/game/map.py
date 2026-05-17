import pygame
import random
import math

from settings import *

TILE_SIZE = 48
ENEMY_BORDER_MARGIN = 200

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.grid_width = math.ceil(self.width / TILE_SIZE)
        self.grid_height = math.ceil(self.height / TILE_SIZE)

        self.generate_valid_map()

    # UTIL
    def is_border(self, x, y):
        return (
            x == 0 or y == 0 or
            x == self.grid_width - 1 or
            y == self.grid_height - 1
        )

    # FLOOD FILL (verificação jogável)
    def flood_fill(self, grid, start):
        stack = [start]
        visited = set()

        while stack:
            x, y = stack.pop()

            if (x, y) in visited:
                continue

            visited.add((x, y))

            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x + dx, y + dy

                if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                    if grid[ny][nx] == 0:
                        stack.append((nx, ny))

        return visited

    # GERA UM MAPA VÁLIDO
    def generate_valid_map(self):

        while True:
            grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]

            # bordas
            for y in range(self.grid_height):
                for x in range(self.grid_width):
                    if self.is_border(x, y):
                        grid[y][x] = 1

            # paredes aleatórias
            for _ in range(int(self.grid_width * self.grid_height * 0.15)):
                x = random.randint(1, self.grid_width - 2)
                y = random.randint(1, self.grid_height - 2)
                grid[y][x] = 1

            # player spawn
            while True:
                px = random.randint(1, self.grid_width - 2)
                py = random.randint(1, self.grid_height - 2)
                if grid[py][px] == 0:
                    self.player_spawn = (px * TILE_SIZE, py * TILE_SIZE)
                    break

            # flood fill base
            reachable = self.flood_fill(grid, (px, py))

            # saída
            ex, ey = random.randint(1, self.grid_width - 2), random.randint(1, self.grid_height - 2)

            if grid[ey][ex] == 1:
                continue

            if (ex, ey) not in reachable:
                continue

            self.exit_rect = pygame.Rect(
                ex * TILE_SIZE,
                ey * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )

            # datafiles
            datafiles = []
            temp_tiles = list(reachable)

            random.shuffle(temp_tiles)

            for (x, y) in temp_tiles:
                if len(datafiles) >= 5:
                    break

                rect = pygame.Rect(
                    x * TILE_SIZE + 10,
                    y * TILE_SIZE + 10,
                    28,
                    28
                )

                datafiles.append(type("D", (), {
                    "rect": rect,
                    "collected": False
                }))

            # garante quantidade mínima
            if len(datafiles) < 5:
                continue

            self.datafiles = datafiles

            # inimigos (opcional simples)
            self.enemies_spawns = []

            enemy_candidates = list(reachable)
            random.shuffle(enemy_candidates)

            px, py = self.player_spawn

            for (x, y) in enemy_candidates:
                wx, wy = x * TILE_SIZE, y * TILE_SIZE

                dist = ((wx - px) ** 2 + (wy - py) ** 2) ** 0.5

                if dist < 250:
                    continue

                self.enemies_spawns.append((wx, wy))

                if len(self.enemies_spawns) >= 2:
                    break

            # paredes finais
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

            # se chegou aqui → mapa válido
            self.grid = grid
            return

    # -----------------------------
    def all_collected(self):
        return all(df.collected for df in self.datafiles)

    # -----------------------------
    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, (25, 35, 55), wall)

        for df in self.datafiles:
            if not df.collected:
                pygame.draw.rect(screen, (0, 200, 255), df.rect)

        color = (0, 255, 120) if self.all_collected() else (255, 80, 80)

        pygame.draw.rect(screen, color, self.exit_rect)