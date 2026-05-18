import pygame

class DataFile:
    def __init__(self, x, y, frames):
        self.rect = pygame.Rect(x, y, 32, 32)

        self.frames = frames
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 10

        self.collected = False
        self.sprite_size = (45, 45)

    def update(self):
        if self.collected:
            return

        self.frame_timer += 1

        if self.frame_timer >= self.frame_speed:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

    def draw(self, screen, apply_camera):
        if self.collected:
            return

        image = self.frames[self.frame_index]
        image = pygame.transform.scale(image, self.sprite_size)

        pos = apply_camera(self.rect)

        pos.x -= (self.sprite_size[0] - self.rect.width) // 2
        pos.y -= (self.sprite_size[1] - self.rect.height) // 2

        screen.blit(image, pos)