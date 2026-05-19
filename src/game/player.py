import pygame

from utils.paths import resource_path

class Player:
    def __init__(self):

        self.rect = pygame.Rect(100, 100, 28, 28)

        self.speed = 5

        # -------------------------
        # animações
        # -------------------------

        self.spawn_frames = [
            pygame.image.load(resource_path("assets/player/spawn/spawn1.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/player/spawn/spawn2.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/player/spawn/spawn3.png")).convert_alpha()
        ]

        self.idle_frames = [
            pygame.image.load(resource_path("assets/player/idle/idle1.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/player/idle/idle2.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/player/idle/idle3.png")).convert_alpha(),
            pygame.image.load(resource_path("assets/player/idle/idle2.png")).convert_alpha()
        ]

        # resize
        self.spawn_frames = [
            pygame.transform.scale(img, (40, 40))
            for img in self.spawn_frames
        ]

        self.idle_frames = [
            pygame.transform.scale(img, (40, 40))
            for img in self.idle_frames
        ]

        # -------------------------
        # estado atual
        # -------------------------

        self.state = "spawn"

        self.frame_index = 0
        self.animation_speed = 0.08

        self.image = self.spawn_frames[0]

        self.spawn_finished = False

    # -------------------------
    # animações
    # -------------------------

    def animate(self):

        # SPAWN
        if self.state == "spawn":

            self.frame_index += self.animation_speed

            if self.frame_index >= len(self.spawn_frames):

                self.state = "idle"

                self.frame_index = 0

            else:
                self.image = self.spawn_frames[int(self.frame_index)]

        # IDLE
        elif self.state == "idle":

            self.frame_index += 0.08

            if self.frame_index >= len(self.idle_frames):
                self.frame_index = 0

            self.image = self.idle_frames[int(self.frame_index)]

    # -------------------------
    # movimento
    # -------------------------

    def movement(self, walls):

        # trava player durante spawn
        if self.state == "spawn":
            return

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= self.speed

        if keys[pygame.K_s]:
            dy += self.speed

        if keys[pygame.K_a]:
            dx -= self.speed

        if keys[pygame.K_d]:
            dx += self.speed

        self.rect.x += dx

        for wall in walls:
            if self.rect.colliderect(wall.rect):

                if dx > 0:
                    self.rect.right = wall.rect.left

                if dx < 0:
                    self.rect.left = wall.rect.right

        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):

                if dy > 0:
                    self.rect.bottom = wall.rect.top

                if dy < 0:
                    self.rect.top = wall.rect.bottom

    # -------------------------
    # update
    # -------------------------

    def update(self, walls):

        self.animate()

        self.movement(walls)

    # -------------------------
    # draw
    # -------------------------

    def draw(self, screen, apply_camera):

        screen.blit(
            self.image,
            apply_camera(self.rect)
        )