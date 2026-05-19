import pygame
import random
import math

from utils.paths import resource_path
from settings import *
from game.datafiles import DataFile
from game.walls import Wall

TILE_SIZE = 48


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.grid_width = math.ceil(self.width / TILE_SIZE)
        self.grid_height = math.ceil(self.height / TILE_SIZE)

        self.wall_sprites = self.load_wall_sprites()
        self.datafile_sprites = self.datafile_frames()

        self.generate_valid_map()

    # -----------------------------
    # UTIL
    # -----------------------------
    def is_border(self, x, y):
        return (
            x == 0 or y == 0 or
            x == self.grid_width - 1 or
            y == self.grid_height - 1
        )

    # -----------------------------
    # FLOOD FILL
    # -----------------------------
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

    # -----------------------------
    # SPRITES
    # -----------------------------
    def load_wall_sprites(self):
        sprites = []
        for i in range(1, 3):
            img = pygame.image.load(resource_path(f"assets/walls/wall{i}.png")).convert_alpha()
            img = pygame.transform.scale(img, (72, 72))
            sprites.append(img)
        return sprites

    def datafile_frames(self):
        frames = []
        for i in range(1, 5):
            img = pygame.image.load(resource_path(f"assets/datafile/datafile{i}.png")).convert_alpha()
            img = pygame.transform.scale(img, (32, 32))
            frames.append(img)
        return frames

    # -----------------------------
    # MAP GENERATION
    # -----------------------------
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

            # flood fill
            reachable = self.flood_fill(grid, (px, py))

            # saída
            while True:
                ex = random.randint(1, self.grid_width - 2)
                ey = random.randint(1, self.grid_height - 2)

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
                break

            # -----------------------------
            # WALLS (CORRIGIDO)
            # -----------------------------
            self.walls = []

            for y in range(self.grid_height):
                for x in range(self.grid_width):
                    if grid[y][x] == 1:
                        rect = pygame.Rect(
                            x * TILE_SIZE,
                            y * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE
                        )

                        self.walls.append(Wall(rect, self.wall_sprites))

            # -----------------------------
            # DATAFILES
            # -----------------------------
            # -----------------------------
            self.datafiles = []

            valid_positions = []

            for y in range(1, self.grid_height - 1):
                for x in range(1, self.grid_width - 1):
                    if grid[y][x] == 0:
                        valid_positions.append((x, y))

            # garante que existem pelo menos 5 posições
            if len(valid_positions) < 5:
                return self.generate_valid_map()

            random.shuffle(valid_positions)

            for i in range(5):
                dx, dy = valid_positions[i]

                rect = pygame.Rect(
                    dx * TILE_SIZE + 8,
                    dy * TILE_SIZE + 8,
                    32,
                    32
                )

                self.datafiles.append(
                    DataFile(rect.x, rect.y, self.datafile_sprites)
                )

            # -----------------------------
            # ENEMIES SPAWN
            # -----------------------------
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

            # grid final
            self.grid = grid
            return

    # -----------------------------
    # GAME CHECK
    # -----------------------------
    def all_collected(self):
        return all(df.collected for df in self.datafiles)

    # -----------------------------
    # DRAW (DEBUG ONLY)
    # -----------------------------
    def draw(self, screen):
        for wall in self.walls:
            wall.draw(screen, lambda r: r)

        color = (0, 255, 120) if self.all_collected() else (255, 80, 80)

        pygame.draw.rect(screen, color, self.exit_rect)