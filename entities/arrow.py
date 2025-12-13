import pygame
import math
from constants import ARROW_SPEED, ARROW_WIDTH, ARROW_HEIGHT, ARROW_COLOR, ARROW_TIP_COLOR

class Arrow:
    """Pijl projectile afgevuurd door Archer vijanden"""
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx * ARROW_SPEED
        self.dy = dy * ARROW_SPEED

        # Bereken de hoek voor rotatie van de pijl
        self.angle = math.atan2(dy, dx)

        # Hitbox voor collision detection
        self.width = ARROW_WIDTH
        self.height = ARROW_HEIGHT
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)

    def update(self):
        """Update pijl positie"""
        self.x += self.dx
        self.y += self.dy
        self.rect.x = self.x - self.width // 2
        self.rect.y = self.y - self.height // 2

    def render(self, screen):
        """Teken de pijl als een geroteerde rechthoek met pijlpunt"""
        # Maak een surface voor de pijl
        arrow_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Teken de pijl shaft (bruin)
        pygame.draw.rect(arrow_surface, ARROW_COLOR, (0, self.height // 4, self.width - 3, self.height // 2))

        # Teken de pijlpunt (grijs driehoek)
        tip_points = [
            (self.width - 3, self.height // 2),  # Midden rechts
            (self.width, 0),  # Top rechts
            (self.width, self.height)  # Bottom rechts
        ]
        pygame.draw.polygon(arrow_surface, ARROW_TIP_COLOR, tip_points)

        # Roteer de pijl in de richting van beweging
        rotated_surface = pygame.transform.rotate(arrow_surface, -math.degrees(self.angle))
        rotated_rect = rotated_surface.get_rect(center=(int(self.x), int(self.y)))

        screen.blit(rotated_surface, rotated_rect)
