import pygame
import math

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)

        self.speed = 2
        self.chase_speed = 3

        self.detection_radius = 150

        # patrulha simples
        self.points = [
            (x, y),
            (x + 200, y)
        ]
        self.current_point = 0

    def distance_to_player(self, player):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        return math.sqrt(dx*dx + dy*dy)

    def patrol(self):
        target_x, target_y = self.points[self.current_point]

        if self.rect.x < target_x:
            self.rect.x += self.speed
        elif self.rect.x > target_x:
            self.rect.x -= self.speed

        if abs(self.rect.x - target_x) < 5:
            self.current_point += 1
            if self.current_point >= len(self.points):
                self.current_point = 0

    def chase(self, player):
        if player.rect.x > self.rect.x:
            self.rect.x += self.chase_speed
        elif player.rect.x < self.rect.x:
            self.rect.x -= self.chase_speed

        if player.rect.y > self.rect.y:
            self.rect.y += self.chase_speed
        elif player.rect.y < self.rect.y:
            self.rect.y -= self.chase_speed
    
    def clamp_to_world(self, width, height):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height

    def update(self, player, world_width, world_height):
        dist = self.distance_to_player(player)

        if dist < self.detection_radius:
            self.chase(player)
        else:
            self.patrol()

        self.clamp_to_world(world_width, world_height)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 50, 50), self.rect)