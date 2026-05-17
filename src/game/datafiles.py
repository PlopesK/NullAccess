import pygame

class DataFile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)

        self.collected = False

    def draw(self, screen, apply_camera):
        if not self.collected:

            pygame.draw.rect(
                screen,
                (0, 200, 255),
                apply_camera(self.rect)
            )