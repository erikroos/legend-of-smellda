import pygame
from constants import WALL_THICKNESS, EXIT_SIZE

class CaveEntrance:
    def __init__(self, x, y, width=None, height=None):
        """Een grot ingang - een zwart blok langs de rand"""
        self.x = x
        self.y = y
        self.width = width if width else EXIT_SIZE // 2  # Half zo breed als normale exit
        self.height = height if height else WALL_THICKNESS
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = (0, 0, 0)  # Zwart

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
