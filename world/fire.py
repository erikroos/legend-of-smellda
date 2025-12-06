import pygame
import random
from constants import FIRE_COLOR_1, FIRE_COLOR_2, FIRE_COLOR_3

class Fire:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 25
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Animatie
        self.animation_timer = 0
        self.flicker_offset = random.randint(0, 10)

    def update(self):
        self.animation_timer += 1

    def render(self, screen):
        # Simpel vuur effect met kleuren die flikkeren
        base_y = self.y + 15

        # Flikkerende hoogte gebaseerd op timer
        flicker = (self.animation_timer + self.flicker_offset) % 20
        height_offset = 5 if flicker < 10 else 0

        # Vuurkleuren
        colors = [
            FIRE_COLOR_1,  # Oranje-rood
            FIRE_COLOR_2,  # Donker oranje
            FIRE_COLOR_3   # Goud
        ]

        # Teken meerdere vlammen voor effect
        for i, color in enumerate(colors):
            flame_height = 15 - (i * 3) + height_offset
            flame_width = 16 - (i * 4)
            flame_x = self.x + (self.width - flame_width) // 2
            flame_y = base_y - flame_height

            pygame.draw.ellipse(screen, color,
                              (flame_x, flame_y, flame_width, flame_height))
