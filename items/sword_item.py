import pygame
from constants import SWORD_BLADE_COLOR, SWORD_HANDLE_COLOR

class SwordItem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 12
        self.height = 30
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.collected = False

    def render(self, screen):
        if self.collected:
            return

        # Teken zwaard verticaal (kling omhoog)
        # Kling
        blade_rect = pygame.Rect(self.x + 2, self.y, 8, 22)
        pygame.draw.rect(screen, SWORD_BLADE_COLOR, blade_rect)

        # Handvat
        handle_rect = pygame.Rect(self.x, self.y + 22, 12, 8)
        pygame.draw.rect(screen, SWORD_HANDLE_COLOR, handle_rect)
