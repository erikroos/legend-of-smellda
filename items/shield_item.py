import pygame
from constants import SHIELD_COLOR, SHIELD_EDGE_COLOR

class ShieldItem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.collected = False

    def collect(self):
        """Verzamel het schild"""
        self.collected = True

    def update(self):
        """Update (niet meer nodig zonder animatie)"""
        pass

    def render(self, screen):
        """Teken het schild item"""
        if self.collected:
            return

        # Teken schild als een bruin schild met rand
        shield_width = 20
        shield_height = 26
        shield_x = self.x + (self.width - shield_width) // 2
        shield_y = self.y + (self.height - shield_height) // 2

        # Schild basis
        pygame.draw.rect(screen, SHIELD_COLOR, (shield_x, shield_y, shield_width, shield_height))

        # Schild rand
        pygame.draw.rect(screen, SHIELD_EDGE_COLOR, (shield_x, shield_y, shield_width, shield_height), 2)

        # Teken een klein kruis/decoratie in het midden
        center_x = shield_x + shield_width // 2
        center_y = shield_y + shield_height // 2

        # Verticale lijn
        pygame.draw.line(screen, SHIELD_EDGE_COLOR,
                        (center_x, shield_y + 6),
                        (center_x, shield_y + shield_height - 6), 2)
        # Horizontale lijn
        pygame.draw.line(screen, SHIELD_EDGE_COLOR,
                        (shield_x + 5, center_y),
                        (shield_x + shield_width - 5, center_y), 2)
