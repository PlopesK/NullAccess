class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0

        self.width = width
        self.height = height

        self.zoom = 1.5

    def follow(self, target):
        target_x = target.rect.centerx - (self.width / self.zoom)  // 2
        target_y = target.rect.centery - (self.height / self.zoom)  // 2

        self.x += (target_x - self.x) * 0.1
        self.y += (target_y - self.y) * 0.1