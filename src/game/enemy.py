import pygame
import random
from utils.pathfinding import bfs

TILE_SIZE = 48

class Enemy:
    def __init__(self, x, y, map_ref):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.map = map_ref

        self.speed = 2
        self.chase_speed = 3

        self.detection_radius = 170

        self.path = []
        self.path_index = 0

        self.mode = "patrol"  # patrol | chase

        self.target_player_last_seen = None

        self.recalculate_path()

    # ----------------------------
    # utils grid
    # ----------------------------
    def world_to_grid(self, x, y):
        return (x // TILE_SIZE, y // TILE_SIZE)

    def grid_to_world(self, x, y):
        return (x * TILE_SIZE, y * TILE_SIZE)

    def distance_to_player(self, player):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        return (dx*dx + dy*dy) ** 0.5

    # ----------------------------
    # patrol BFS
    # ----------------------------
    def get_random_goal(self):
        while True:
            x = random.randint(1, len(self.map.grid[0]) - 2)
            y = random.randint(1, len(self.map.grid) - 2)

            if self.map.grid[y][x] == 0:
                return (x, y)

    def recalculate_path(self, goal=None):
        start = self.world_to_grid(self.rect.centerx, self.rect.centery)

        if goal is None:
            goal = self.get_random_goal()

        self.path = bfs(start, goal, self.map.grid)
        self.path_index = 0

    def patrol(self):
        if not self.path or self.path_index >= len(self.path):
            self.recalculate_path()
            return

        tx, ty = self.grid_to_world(*self.path[self.path_index])

        dx = tx - self.rect.x
        dy = ty - self.rect.y

        if abs(dx) > 2:
            self.rect.x += self.speed if dx > 0 else -self.speed

        if abs(dy) > 2:
            self.rect.y += self.speed if dy > 0 else -self.speed

        if abs(dx) < 5 and abs(dy) < 5:
            self.path_index += 1

    # ----------------------------
    # chase (sem BFS)
    # ----------------------------
    def chase(self, player):
        self.target_player_last_seen = (player.rect.x, player.rect.y)

        if player.rect.x > self.rect.x:
            self.rect.x += self.chase_speed
        else:
            self.rect.x -= self.chase_speed

        if player.rect.y > self.rect.y:
            self.rect.y += self.chase_speed
        else:
            self.rect.y -= self.chase_speed

    # ----------------------------
    # AI main
    # ----------------------------
    def update(self, player, world_w, world_h):
        dist = self.distance_to_player(player)

        if dist < self.detection_radius:
            self.mode = "chase"
        else:
            # se perdeu player, volta pra patrol e recalcula rota
            if self.mode == "chase":
                self.recalculate_path()
            self.mode = "patrol"

        if self.mode == "chase":
            self.chase(player)
        else:
            self.patrol()

    # ----------------------------
    # draw
    # ----------------------------
    def draw(self, screen, apply_camera):
        pygame.draw.rect(
            screen,
            (255, 50, 50),
            apply_camera(self.rect)
        )