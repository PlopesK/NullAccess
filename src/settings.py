import pygame
from utils.paths import resource_path

pygame.font.init()

FONT_PATH = "assets/fonts/CyberpunkCraftpixPixel.otf"

def get_font(size):
    return pygame.font.Font(resource_path(FONT_PATH), size)

FPS = 60

TITLE = "ACCESS://NULL"

FONT_SMALL = get_font(18)
FONT_MEDIUM = get_font(28)
FONT_BIG = get_font(60)

BLACK = (10, 10, 15)
WHITE = (240, 240, 240)
NEON_GREEN = (0, 255, 120)
RED = (255, 60, 60)