import pygame
from constants import (
    OLD_MAN_ROBE_COLOR, OLD_MAN_SKIN_COLOR,
    OLD_MAN_BEARD_COLOR, OLD_MAN_TEXT_COLOR
)

class OldMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.visible = True

        # Kleuren
        self.robe_color = OLD_MAN_ROBE_COLOR
        self.skin_color = OLD_MAN_SKIN_COLOR
        self.beard_color = OLD_MAN_BEARD_COLOR

        # Tekst boven zijn hoofd
        self.text = "IT'S DANGEROUS TO GO ALONE!"
        self.text2 = "TAKE THIS."

    def render(self, screen):
        if not self.visible:
            return

        # Teken oude man (simpele vorm)
        # Mantel/lichaam
        pygame.draw.rect(screen, self.robe_color, (self.x + 5, self.y + 15, 30, 25))

        # Hoofd
        pygame.draw.circle(screen, self.skin_color, (self.x + 20, self.y + 12), 10)

        # Baard
        pygame.draw.rect(screen, self.beard_color, (self.x + 12, self.y + 15, 16, 12))

        # Teken tekst boven zijn hoofd
        try:
            font = pygame.font.Font(None, 20)
            text_surface = font.render(self.text, True, OLD_MAN_TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(self.x + 20, self.y - 30))
            screen.blit(text_surface, text_rect)

            text_surface2 = font.render(self.text2, True, OLD_MAN_TEXT_COLOR)
            text_rect2 = text_surface2.get_rect(center=(self.x + 20, self.y - 15))
            screen.blit(text_surface2, text_rect2)
        except:
            pass
