import pygame

class Rupee:
    """Een rupee (geld item) die de speler kan oppakken"""

    def __init__(self, x, y, value=1):
        """
        value: 1 voor groene rupee, 5 voor blauwe rupee
        """
        self.x = x
        self.y = y
        self.value = value
        self.size = 16
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.collected = False

        # Timer voor hoe lang de rupee blijft (4 seconden @ 60 FPS = 240 frames)
        self.lifetime = 240
        self.lifetime_max = 240

        # Knippereffect in de laatste seconde
        self.blink_threshold = 60  # Start knipperen bij laatste 1 seconde

        # Animatie voor glinstering
        self.animation_offset = 0
        self.animation_speed = 0.1

    def update(self):
        """Update animatie en lifetime"""
        if not self.collected:
            # Update bounce animatie
            self.animation_offset += self.animation_speed
            if self.animation_offset > 6.28:  # 2 * PI
                self.animation_offset = 0

            # Update lifetime
            self.lifetime -= 1

            # Als lifetime op is, markeer als collected (= verdwenen)
            if self.lifetime <= 0:
                self.collected = True

    def collect(self):
        """Markeer als verzameld"""
        self.collected = True

    def render(self, screen):
        """Teken de rupee"""
        if self.collected:
            return

        # Knippereffect in de laatste seconde
        if self.lifetime < self.blink_threshold:
            # Knipper elke 10 frames
            if (self.lifetime // 10) % 2 == 0:
                return  # Skip rendering dit frame

        # Bereken centrum voor rotatie effect
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2

        # Lichte bounce animatie
        bounce = int(abs(pygame.math.Vector2(0, 3).rotate(self.animation_offset * 50).y))
        adjusted_y = center_y - bounce

        # Diamant vorm (4 punten)
        points = [
            (center_x, adjusted_y - self.size // 2),  # Boven
            (center_x + self.size // 2, adjusted_y),  # Rechts
            (center_x, adjusted_y + self.size // 2),  # Onder
            (center_x - self.size // 2, adjusted_y),  # Links
        ]

        # Kleur gebaseerd op waarde
        if self.value == 1:
            # Groen-gele rupee (waarde 1)
            base_color = (100, 200, 50)
            dark_color = (50, 100, 25)
            highlight_color = (200, 255, 150)
        else:  # value == 5
            # Groen-blauwe rupee (waarde 5)
            base_color = (50, 150, 200)
            dark_color = (25, 75, 100)
            highlight_color = (150, 220, 255)

        # Teken diamant
        pygame.draw.polygon(screen, base_color, points)
        pygame.draw.polygon(screen, dark_color, points, 2)

        # Glans effect
        highlight_points = [
            (center_x - 3, adjusted_y - 3),
            (center_x + 3, adjusted_y - 3),
            (center_x, adjusted_y + 2),
        ]
        pygame.draw.polygon(screen, highlight_color, highlight_points)
