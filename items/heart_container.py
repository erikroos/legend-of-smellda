import pygame

class HeartContainer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.collected = False

    def collect(self):
        """Verzamel de heart container"""
        self.collected = True

    def update(self):
        """Update (niet meer nodig zonder animatie)"""
        pass

    def render(self, screen):
        """Teken de heart container met witte outline en rode vulling"""
        if self.collected:
            return

        # Kleuren
        red = (255, 50, 50)
        white = (255, 255, 255)

        # Positie centers
        left_circle_center = (self.x + self.width // 4, self.y + self.height // 3)
        right_circle_center = (self.x + (3 * self.width // 4) + 1, self.y + self.height // 3)

        # Driehoek punten
        triangle_points = [
            (self.x, self.y + self.height // 3),  # Links
            (self.x + self.width, self.y + self.height // 3),  # Rechts
            (self.x + self.width // 2, self.y + self.height)  # Punt
        ]

        # Stap 1: Teken eerst de witte outline (volledige cirkels en driehoek)
        pygame.draw.circle(screen, white, left_circle_center, self.width // 4)
        pygame.draw.circle(screen, white, right_circle_center, self.width // 4)
        pygame.draw.polygon(screen, white, triangle_points)

        # Stap 2: Teken rode vulling eroverheen (iets kleiner voor outline effect)
        pygame.draw.circle(screen, red, left_circle_center, self.width // 4 - 2)
        pygame.draw.circle(screen, red, right_circle_center, self.width // 4 - 2)
        # Driehoek iets kleiner voor outline
        triangle_points_inner = [
            (self.x + 2, self.y + self.height // 3),  # Links
            (self.x + self.width - 2, self.y + self.height // 3),  # Rechts
            (self.x + self.width // 2, self.y + self.height - 2)  # Punt
        ]
        pygame.draw.polygon(screen, red, triangle_points_inner)
