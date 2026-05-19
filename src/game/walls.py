import random

class Wall:
    def __init__(self, rect, sprites):
        self.rect = rect
        self.sprites = sprites

        self.image = random.choice(self.sprites)

        self.timer = 0
        self.change_rate = 100

    def update(self, alert_level=0):
        self.timer += 1

        rate = 10 if alert_level > 0 else self.change_rate

        if self.timer >= rate:
            self.timer = 0
            self.image = random.choice(self.sprites)

    def draw(self, screen, apply_camera):
        screen.blit(self.image, apply_camera(self.rect))