import pygame
from constants import BLOCK_COLOR, BLOCK_LINE_COLOR, TILE_SIZE

class PushableBlock:
    def __init__(self, x, y, size=TILE_SIZE):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)

        self.color = BLOCK_COLOR
        self.has_been_pushed = False  # Track of blok al geduwd is

    def can_be_pushed(self, player_rect, player_facing, obstacles):
        """Check of het blok geduwd kan worden in de richting waar speler naar kijkt"""
        # Als blok al geduwd is, kan het niet meer bewegen
        if self.has_been_pushed:
            return False

        # Bereken nieuwe positie als het blok wordt geduwd
        push_distance = TILE_SIZE  # Een hele tile
        new_x = self.x
        new_y = self.y

        if player_facing == 'up':
            new_y = self.y - push_distance
        elif player_facing == 'down':
            new_y = self.y + push_distance
        elif player_facing == 'left':
            new_x = self.x - push_distance
        elif player_facing == 'right':
            new_x = self.x + push_distance
        else:
            return False

        # Maak tijdelijke rect voor nieuwe positie
        new_rect = pygame.Rect(new_x, new_y, self.size, self.size)

        # Check of nieuwe positie niet buiten bounds is (rekening houdend met muren)
        wall_thickness = 40
        hud_height = 60
        screen_width = 800
        screen_height = 600

        if (new_x < wall_thickness or
            new_x + self.size > screen_width - wall_thickness or
            new_y < hud_height + wall_thickness or
            new_y + self.size > hud_height + screen_height - wall_thickness):
            return False

        # Check of er geen obstakels in de weg staan
        for obstacle in obstacles:
            # Check of obstacle een Rect is of een object met .rect attribuut
            obstacle_rect = obstacle if isinstance(obstacle, pygame.Rect) else obstacle.rect
            if new_rect.colliderect(obstacle_rect):
                return False

        return True

    def push(self, direction):
        """Duw het blok in de gegeven richting"""
        push_distance = 50  # Een hele tile

        if direction == 'up':
            self.y -= push_distance
        elif direction == 'down':
            self.y += push_distance
        elif direction == 'left':
            self.x -= push_distance
        elif direction == 'right':
            self.x += push_distance

        # Update rect
        self.rect.x = self.x
        self.rect.y = self.y

        # Markeer dat blok geduwd is
        self.has_been_pushed = True

    def render(self, screen):
        # Teken het blok zelf
        pygame.draw.rect(screen, self.color, self.rect)

        # Teken kleiner vierkant in het midden met schuine lijnen naar hoeken
        line_color = BLOCK_LINE_COLOR

        # Bereken het kleinere vierkant in het midden (60% van de grootte)
        inner_size = int(self.size * 0.6)
        offset = (self.size - inner_size) // 2

        inner_left = self.x + offset
        inner_right = self.x + offset + inner_size
        inner_top = self.y + offset
        inner_bottom = self.y + offset + inner_size

        # Teken het kleinere vierkant in het midden
        pygame.draw.rect(screen, line_color,
                        (inner_left, inner_top, inner_size, inner_size), 2)

        # Teken schuine lijnen van binnenste naar buitenste hoeken
        # Linksboven naar linksboven
        pygame.draw.line(screen, line_color,
                        (inner_left, inner_top), (self.x + 2, self.y + 2), 2)
        # Rechtsboven naar rechtsboven
        pygame.draw.line(screen, line_color,
                        (inner_right, inner_top), (self.x + self.size - 2, self.y + 2), 2)
        # Linksonder naar linksonder
        pygame.draw.line(screen, line_color,
                        (inner_left, inner_bottom), (self.x + 2, self.y + self.size - 2), 2)
        # Rechtsonder naar rechtsonder
        pygame.draw.line(screen, line_color,
                        (inner_right, inner_bottom), (self.x + self.size - 2, self.y + self.size - 2), 2)
