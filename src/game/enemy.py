import pygame
import random
from utils.pathfinding import bfs
from utils.paths import resource_path

TILE_SIZE = 48

class Enemy:
    def __init__(self, x, y, map_ref):

        self.rect = pygame.Rect(x, y, 40, 40)

        self.map = map_ref

        self.speed = 2
        self.chase_speed = 3

        self.detection_radius = 170

        # -------------------------
        # animação
        # -------------------------

        self.frames = [
            pygame.image.load(resource_path("assets/enemy/enemy1.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/enemy/enemy2.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/enemy/enemy1.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/enemy/enemy3.png")).convert_alpha()
        ]

        self.frames = [
            pygame.transform.scale(img, (50, 50))
            for img in self.frames
        ]

        self.frame_index = 0
        self.animation_speed = 0.12

        self.image = self.frames[0]

        # -------------------------
        # pathfinding
        # -------------------------

        self.path = []
        self.path_index = 0

        self.mode = "patrol"

        self.recalculate_path()

    # -------------------------
    # animação
    # -------------------------

    def animate(self):

        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    # -------------------------
    # utils
    # -------------------------

    def world_to_grid(self, x, y):
        return (x // TILE_SIZE, y // TILE_SIZE)

    def grid_to_world(self, x, y):
        return (x * TILE_SIZE, y * TILE_SIZE)

    def distance_to_player(self, player):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y

        return (dx * dx + dy * dy) ** 0.5

    # -------------------------
    # pathfinding
    # -------------------------

    def get_random_goal(self):

        while True:

            x = random.randint(
                1,
                len(self.map.grid[0]) - 2
            )

            y = random.randint(
                1,
                len(self.map.grid) - 2
            )

            if self.map.grid[y][x] == 0:
                return (x, y)

    def recalculate_path(self, goal=None):

        start = self.world_to_grid(
            self.rect.centerx,
            self.rect.centery
        )

        if goal is None:
            goal = self.get_random_goal()

        self.path = bfs(
            start,
            goal,
            self.map.grid
        )

        self.path_index = 0

    # -------------------------
    # patrol
    # -------------------------

    def patrol(self):

        if not self.path or self.path_index >= len(self.path):
            self.recalculate_path()
            return

        tx, ty = self.grid_to_world(
            *self.path[self.path_index]
        )

        dx = tx - self.rect.x
        dy = ty - self.rect.y

        if abs(dx) > 2:
            self.rect.x += self.speed if dx > 0 else -self.speed

        if abs(dy) > 2:
            self.rect.y += self.speed if dy > 0 else -self.speed

        if abs(dx) < 5 and abs(dy) < 5:
            self.path_index += 1

    # -------------------------
    # chase
    # -------------------------

    def chase(self, player):

        if player.rect.x > self.rect.x:
            self.rect.x += self.chase_speed
        else:
            self.rect.x -= self.chase_speed

        if player.rect.y > self.rect.y:
            self.rect.y += self.chase_speed
        else:
            self.rect.y -= self.chase_speed

    # -------------------------
    # update
    # -------------------------

    def update(self, player, world_w, world_h):

        self.animate()

        dist = self.distance_to_player(player)

        if dist < self.detection_radius:
            self.mode = "chase"
        else:

            if self.mode == "chase":
                self.recalculate_path()

            self.mode = "patrol"

        if self.mode == "chase":
            self.chase(player)
        else:
            self.patrol()

    # -------------------------
    # draw
    # -------------------------

    def draw(self, screen, apply_camera):

        screen.blit(
            self.image,
            apply_camera(self.rect)
        )