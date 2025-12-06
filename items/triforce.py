import pygame

class Triforce:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 35
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.collected = False

        # Animatie
        self.pulse_timer = 0
        self.pulse_scale = 1.0

    def collect(self):
        """Verzamel de triforce"""
        self.collected = True

    def update(self):
        """Update animatie"""
        self.pulse_timer += 1
        # Pulserende animatie
        self.pulse_scale = 1.0 + 0.15 * abs((self.pulse_timer % 60) - 30) / 30

    def render(self, screen):
        """Teken de triforce (gouden driehoek)"""
        if self.collected:
            return

        # Gouden kleur
        gold = (255, 215, 0)
        dark_gold = (218, 165, 32)

        # Bereken gepulseerde grootte
        pulsed_width = int(self.width * self.pulse_scale)
        pulsed_height = int(self.height * self.pulse_scale)
        offset_x = (pulsed_width - self.width) // 2
        offset_y = (pulsed_height - self.height) // 2

        center_x = self.x + self.width // 2 - offset_x
        center_y = self.y + self.height // 2 - offset_y

        # Triforce bestaat uit 3 driehoeken
        triangle_size = pulsed_height // 2

        # Bovenste driehoek
        top_points = [
            (center_x + pulsed_width // 2, center_y),  # Top
            (center_x + pulsed_width // 2 - triangle_size, center_y + triangle_size),  # Links onder
            (center_x + pulsed_width // 2 + triangle_size, center_y + triangle_size)  # Rechts onder
        ]
        pygame.draw.polygon(screen, gold, top_points)
        pygame.draw.polygon(screen, dark_gold, top_points, 2)

        # Linker onderste driehoek
        left_points = [
            (center_x + pulsed_width // 2 - triangle_size, center_y + triangle_size),  # Top
            (center_x + pulsed_width // 2 - 2 * triangle_size, center_y + 2 * triangle_size),  # Links onder
            (center_x + pulsed_width // 2, center_y + 2 * triangle_size)  # Rechts onder
        ]
        pygame.draw.polygon(screen, gold, left_points)
        pygame.draw.polygon(screen, dark_gold, left_points, 2)

        # Rechter onderste driehoek
        right_points = [
            (center_x + pulsed_width // 2 + triangle_size, center_y + triangle_size),  # Top
            (center_x + pulsed_width // 2, center_y + 2 * triangle_size),  # Links onder
            (center_x + pulsed_width // 2 + 2 * triangle_size, center_y + 2 * triangle_size)  # Rechts onder
        ]
        pygame.draw.polygon(screen, gold, right_points)
        pygame.draw.polygon(screen, dark_gold, right_points, 2)
