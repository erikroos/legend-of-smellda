import pygame
from world.fire import Fire
from constants import (
    GAME_WIDTH, GAME_HEIGHT, HUD_HEIGHT, WALL_THICKNESS,
    WALL_COLOR, CAVE_EXIT_COLOR, CAVE_BACKGROUND_COLOR
)

class BaseCaveRoom:
    def __init__(self):
        self.screen_width = GAME_WIDTH
        self.screen_height = GAME_HEIGHT
        self.wall_thickness = WALL_THICKNESS

        # Zwarte achtergrond
        self.background_color = CAVE_BACKGROUND_COLOR

        # Center posities
        self.center_x = GAME_WIDTH // 2
        self.center_y = HUD_HEIGHT + GAME_HEIGHT // 2

        # Vuren aan weerszijden van de oude man
        self.fires = [
            Fire(self.center_x - 60, self.center_y - 40),
            Fire(self.center_x + 40, self.center_y - 40)
        ]

        # Exit onderaan (smal)
        self.has_exit = True

    def update(self):
        # Update fire animations
        for fire in self.fires:
            fire.update()

    def render(self, screen, hud_height=HUD_HEIGHT):
        # Zwarte achtergrond
        game_area = pygame.Rect(0, hud_height, self.screen_width, self.screen_height)
        pygame.draw.rect(screen, self.background_color, game_area)

        # Teken stenen muren rondom
        # Bovenmuur (volledig)
        pygame.draw.rect(screen, WALL_COLOR,
                        (0, hud_height, self.screen_width, self.wall_thickness))

        # Ondermuur met smalle exit in het midden
        pygame.draw.rect(screen, WALL_COLOR,
                        (0, hud_height + self.screen_height - self.wall_thickness,
                         self.screen_width // 2 - 25, self.wall_thickness))
        pygame.draw.rect(screen, WALL_COLOR,
                        (self.screen_width // 2 + 25, hud_height + self.screen_height - self.wall_thickness,
                         self.screen_width // 2 - 25, self.wall_thickness))

        # Exit (zwart blok in het midden onderaan)
        pygame.draw.rect(screen, CAVE_EXIT_COLOR,
                        (self.screen_width // 2 - 25, hud_height + self.screen_height - self.wall_thickness,
                         50, self.wall_thickness))

        # Linkermuur
        pygame.draw.rect(screen, WALL_COLOR,
                        (0, hud_height, self.wall_thickness, self.screen_height))

        # Rechtermuur
        pygame.draw.rect(screen, WALL_COLOR,
                        (self.screen_width - self.wall_thickness, hud_height,
                         self.wall_thickness, self.screen_height))

        # Render fires
        for fire in self.fires:
            fire.render(screen)

        # Render specifieke cave content (override in subclasses)
        self.render_content(screen)

    def render_content(self, screen):
        """Override this method in subclasses to render specific content"""
        pass
