import pygame
from constants import STAIRS_DARK_COLOR, STAIRS_STEP_COLOR, TILE_SIZE

class HiddenStairs:
    def __init__(self, x, y, size=TILE_SIZE):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.revealed = False
        self.reveal_timer = 0  # Timer om te tracken hoe lang geleden de trap onthuld is
        self.reveal_delay = 90  # Aantal frames voordat je de trap in kan (90 frames = 1.5 seconden bij 60 FPS)

        # Trap kleuren
        self.dark_color = STAIRS_DARK_COLOR
        self.step_color = STAIRS_STEP_COLOR

    def reveal(self):
        """Onthul de trap"""
        if not self.revealed:
            self.revealed = True
            self.reveal_timer = 0  # Reset timer bij eerste reveal

    def update(self):
        """Update de reveal timer"""
        if self.revealed and self.reveal_timer < self.reveal_delay:
            self.reveal_timer += 1

    def can_enter(self):
        """Check of de speler de trap in mag (genoeg tijd verstreken)"""
        return self.revealed and self.reveal_timer >= self.reveal_delay

    def render(self, screen):
        """Render de trap alleen als deze onthuld is"""
        if not self.revealed:
            return

        # Teken achtergrond (donker gat)
        pygame.draw.rect(screen, self.dark_color, self.rect)

        # Teken treden (3 horizontale lijnen)
        step_height = self.size // 4
        for i in range(3):
            step_y = self.y + (i + 1) * step_height
            pygame.draw.rect(screen, self.step_color,
                           (self.x + 5, step_y, self.size - 10, step_height - 2))
