import pygame
import random

from settings import *
from game.player import Player
from game.map import Map
from states.victory import Victory
from game.enemy import Enemy
from camera import Camera

class Gameplay:
    def __init__(self, game):

        self.game = game

        self.map = Map(self.game.width, self.game.height)

        self.player = Player()

        self.player.rect.x = self.map.player_spawn[0]
        self.player.rect.y = self.map.player_spawn[1]

        self.camera = Camera(self.game.width, self.game.height)

        self.enemies = []

        for spawn in self.map.enemies_spawns:
            self.enemies.append(Enemy(spawn[0], spawn[1]))

        self.font = pygame.font.SysFont(
            "consolas",
            28
        )

        self.collected_files = 0

        self.total_files = len(
            self.map.datafiles
        )

        self.alert_level = 0

    def handle_event(self, event):
        _ = event
        pass

    def collect_files(self):

        for datafile in self.map.datafiles:

            if not datafile.collected:

                if self.player.rect.colliderect(
                    datafile.rect
                ):

                    datafile.collected = True

                    self.collected_files += 1

    #Câmera
    def apply_camera(self, rect, glitch=(0, 0)):
        return pygame.Rect(
            (rect.x - self.camera.x) * self.camera.zoom + glitch[0],
            (rect.y - self.camera.y) * self.camera.zoom + glitch[1],
            rect.width * self.camera.zoom,
            rect.height * self.camera.zoom
        )
    
    #Efeito de glitch
    def get_glitch_offset(self):
        if self.alert_level == 0:
            return 0, 0

        intensity = 5
        return random.randint(-intensity, intensity), random.randint(-intensity, intensity)

    def update(self):
        self.player.update(self.map.walls)

        self.camera.follow(self.player)

        self.alert_level = 0

        for enemy in self.enemies:
            enemy.update(self.player, self.map.width, self.map.height)

            if enemy.distance_to_player(self.player) < enemy.detection_radius:
                self.alert_level = 1

        self.collect_files()

        self.check_victory()

        self.check_death()

    #Checagem de morte
    def check_death(self):
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):

                from states.gameover import GameOver
                self.game.change_state(GameOver(self.game))
                return

    #Checagem de vitória
    def check_victory(self):
        if self.collected_files == self.total_files:

            if self.player.rect.colliderect(
                self.map.exit_rect
            ):
                self.game.change_state(Victory(self.game))

    def draw(self, screen):

        screen.fill((15, 15, 25))
        glitch_x, glitch_y = self.get_glitch_offset()

        if self.alert_level > 0:
            vignette = pygame.Surface((self.game.width, self.game.height))
            vignette.set_alpha(120)
            vignette.fill((0, 0, 0))

            screen.blit(vignette, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        for wall in self.map.walls:
            pygame.draw.rect(screen, (25, 35, 55), self.apply_camera(wall, (glitch_x, glitch_y)))

        for df in self.map.datafiles:
            if not df.collected:
                self.apply_camera(df.rect, (glitch_x, glitch_y))

        color = (0, 255, 120) if self.map.all_collected() else (255, 80, 80)

        pygame.draw.rect(screen, color, self.apply_camera(self.map.exit_rect, (glitch_x, glitch_y)))

        self.player.draw(screen, lambda r: self.apply_camera(r, (glitch_x, glitch_y)))

        for enemy in self.enemies:
            pygame.draw.circle(
                screen,
                (255, 0, 0),
                self.apply_camera(enemy.rect).center,
                200,
                1
            )

            enemy.draw(screen, lambda r: self.apply_camera(r, (glitch_x, glitch_y)))

        hud = self.font.render(
            f"FILES: {self.collected_files}/{self.total_files}",
            True,
            WHITE
        )

        screen.blit(hud, (20, 20))