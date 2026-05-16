import pygame
from settings import *

class Player:
    def __init__(self):
        self.width = 30
        self.height = 30

        self.speed = 5

        self.rect = pygame.Rect(
            0,
            0,
            self.width,
            self.height
        )

    def movement(self, walls):
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy = -self.speed

        if keys[pygame.K_s]:
            dy = self.speed

        if keys[pygame.K_a]:
            dx = -self.speed

        if keys[pygame.K_d]:
            dx = self.speed

        # Movimento horizontal
        self.rect.x += dx

        for wall in walls:
            if self.rect.colliderect(wall):

                if dx > 0:
                    self.rect.right = wall.left

                if dx < 0:
                    self.rect.left = wall.right

        # Movimento vertical
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall):

                if dy > 0:
                    self.rect.bottom = wall.top

                if dy < 0:
                    self.rect.top = wall.bottom

    def update(self, walls):
        self.movement(walls)

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            NEON_GREEN,
            self.rect
        )