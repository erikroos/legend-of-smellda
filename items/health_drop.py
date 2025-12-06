import pygame

class HealthDrop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 16
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.collected = False

        # Timer voor hoe lang het hartje blijft (4 seconden @ 60 FPS = 240 frames)
        self.lifetime = 240
        self.lifetime_max = 240

        # Knippereffect in de laatste seconde
        self.blink_threshold = 60  # Start knipperen bij laatste 1 seconde

        self.color = (255, 0, 0)  # Rood

    def update(self):
        """Update het hartje - countdown lifetime"""
        if not self.collected:
            self.lifetime -= 1

            # Als lifetime op is, markeer als collected (= verdwenen)
            if self.lifetime <= 0:
                self.collected = True

    def collect(self):
        """Verzamel het hartje"""
        self.collected = True

    def render(self, screen):
        """Teken een klein rood hartje"""
        if self.collected:
            return

        # Knippereffect in de laatste seconde
        if self.lifetime < self.blink_threshold:
            # Knipper elke 10 frames
            if (self.lifetime // 10) % 2 == 0:
                return  # Skip rendering dit frame

        # Teken hartje (vereenvoudigd hart-vorm)
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2

        # Hart bestaat uit twee ronde bovenkanten en een punt onderaan
        # Links bovenkant (cirkel)
        pygame.draw.circle(screen, self.color, (center_x - 4, center_y - 2), 4)
        # Rechts bovenkant (cirkel)
        pygame.draw.circle(screen, self.color, (center_x + 4, center_y - 2), 4)

        # Onderste driehoek (punt van het hart)
        points = [
            (center_x - 8, center_y - 2),  # Links boven
            (center_x + 8, center_y - 2),  # Rechts boven
            (center_x, center_y + 6)       # Punt onderaan
        ]
        pygame.draw.polygon(screen, self.color, points)
