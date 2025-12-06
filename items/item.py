import pygame
from constants import ITEM_WIDTH, ITEM_HEIGHT, HEALTH_POTION_COLOR, HEALTH_POTION_ACCENT, POTION_CAP_COLOR

class Item:
    def __init__(self, x, y, item_type='health_potion'):
        self.x = x
        self.y = y
        self.width = ITEM_WIDTH
        self.height = ITEM_HEIGHT
        self.type = item_type
        self.rect = pygame.Rect(x + 10, y + 10, self.width, self.height)  # Centered in tile
        self.collected = False

        # Kleuren gebaseerd op type
        if item_type == 'health_potion':
            self.color = HEALTH_POTION_COLOR
            self.accent_color = HEALTH_POTION_ACCENT

    def collect(self):
        """Markeer item als gecollecteerd"""
        self.collected = True

    def render(self, screen):
        if self.collected:
            return

        # Teken een flesje-vorm voor health potion
        if self.type == 'health_potion':
            # Fles body
            body_rect = pygame.Rect(self.rect.x + 8, self.rect.y + 10, 14, 16)
            pygame.draw.rect(screen, self.color, body_rect, border_radius=3)

            # Fles neck (hals)
            neck_rect = pygame.Rect(self.rect.x + 11, self.rect.y + 6, 8, 6)
            pygame.draw.rect(screen, self.color, neck_rect)

            # Fles cap (dop)
            cap_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 4, 10, 4)
            pygame.draw.rect(screen, POTION_CAP_COLOR, cap_rect)

            # Highlight (glans)
            highlight_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 12, 4, 8)
            pygame.draw.rect(screen, self.accent_color, highlight_rect)
