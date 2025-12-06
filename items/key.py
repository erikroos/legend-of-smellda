import pygame
from constants import KEY_COLOR, KEY_DARK_COLOR

class Key:
    def __init__(self, x, y, size=30):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.collected = False

        # Key kleuren (goudgeel)
        self.color = KEY_COLOR
        self.dark_color = KEY_DARK_COLOR

    def collect(self):
        self.collected = True

    def render(self, screen):
        if self.collected:
            return

        # Teken sleutel vorm
        # Hoofd van de sleutel (cirkel)
        head_radius = self.size // 3
        head_center = (self.x + head_radius, self.y + head_radius)
        pygame.draw.circle(screen, self.color, head_center, head_radius)
        pygame.draw.circle(screen, self.dark_color, head_center, head_radius // 2)

        # Steel van de sleutel
        shaft_start = (self.x + head_radius, self.y + head_radius * 2)
        shaft_end = (self.x + head_radius, self.y + self.size)
        pygame.draw.line(screen, self.color, shaft_start, shaft_end, 4)

        # Tanden van de sleutel (2 kleine rechthoeken aan de rechterkant)
        tooth_width = 6
        tooth_height = 4
        tooth1_y = self.y + self.size - 10
        tooth2_y = self.y + self.size - 5

        pygame.draw.rect(screen, self.color,
                        (self.x + head_radius, tooth1_y, tooth_width, tooth_height))
        pygame.draw.rect(screen, self.color,
                        (self.x + head_radius, tooth2_y, tooth_width, tooth_height))
