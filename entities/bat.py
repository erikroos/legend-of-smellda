import pygame
import random
from constants import (
    HUD_HEIGHT, WALL_THICKNESS,
    BAT_BODY_COLOR, BAT_WING_COLOR, BAT_EYE_COLOR
)

class Bat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.alive = True
        self.health = 1  # 1 slag en ze zijn dood

        # Beweging - vleermuizen bewegen sneller en meer chaotisch
        self.speed = 2.0
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.direction_change_timer = 0
        self.direction_change_interval = random.randint(30, 60)  # Snellere richting veranderingen

        # Kleuren (zwarte vleermuis)
        self.body_color = BAT_BODY_COLOR
        self.wing_color = BAT_WING_COLOR
        self.eye_color = BAT_EYE_COLOR

        # Animatie voor vleugels
        self.wing_flap_timer = 0
        self.wing_flap_interval = 10
        self.wings_up = True

        # Damage cooldown (om speler niet te vaak te raken)
        self.damage_cooldown = 0
        self.damage_cooldown_max = 60

    def take_damage(self, damage):
        """Neem schade en sterf als health op is"""
        self.health -= damage
        if self.health <= 0:
            self.alive = False

    def update(self, obstacles, screen_width, screen_height, hud_height, pushable_block=None):
        """Update vleermuis positie en gedrag"""
        if not self.alive:
            return

        # Update damage cooldown
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        # Update richting verandering timer
        self.direction_change_timer += 1
        if self.direction_change_timer >= self.direction_change_interval:
            # Verander richting random
            self.direction_x = random.choice([-1, 0, 1])
            self.direction_y = random.choice([-1, 0, 1])
            self.direction_change_timer = 0
            self.direction_change_interval = random.randint(30, 60)

        # Beweeg in de huidige richting
        new_x = self.x + self.direction_x * self.speed
        new_y = self.y + self.direction_y * self.speed

        # Check grenzen (dungeon muren)
        # screen_width en screen_height zijn de GAME dimensies (zonder HUD)
        if new_x < WALL_THICKNESS or new_x + self.width > screen_width - WALL_THICKNESS:
            self.direction_x *= -1  # Keer richting om
            new_x = self.x

        # Verticale grenzen: hud_height + WALL_THICKNESS tot hud_height + screen_height - WALL_THICKNESS
        top_boundary = hud_height + WALL_THICKNESS
        bottom_boundary = screen_height - WALL_THICKNESS
        if new_y < top_boundary or new_y + self.height > bottom_boundary:
            self.direction_y *= -1  # Keer richting om
            new_y = self.y

        # Update positie
        self.x = new_x
        self.y = new_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Update vleugel animatie
        self.wing_flap_timer += 1
        if self.wing_flap_timer >= self.wing_flap_interval:
            self.wings_up = not self.wings_up
            self.wing_flap_timer = 0

    def render(self, screen):
        """Teken de vleermuis"""
        if not self.alive:
            return

        # Teken lichaam (ovaal)
        body_rect = pygame.Rect(
            int(self.x + self.width // 4),
            int(self.y + self.height // 3),
            self.width // 2,
            self.height // 2
        )
        pygame.draw.ellipse(screen, self.body_color, body_rect)

        # Teken vleugels (driehoeken aan beide kanten)
        wing_offset = 3 if self.wings_up else 6

        # Linker vleugel
        left_wing_points = [
            (int(self.x + self.width // 4), int(self.y + self.height // 2)),  # Bij lichaam
            (int(self.x), int(self.y + wing_offset)),  # Punt
            (int(self.x), int(self.y + self.height - wing_offset))  # Onderkant
        ]
        pygame.draw.polygon(screen, self.wing_color, left_wing_points)

        # Rechter vleugel
        right_wing_points = [
            (int(self.x + 3 * self.width // 4), int(self.y + self.height // 2)),  # Bij lichaam
            (int(self.x + self.width), int(self.y + wing_offset)),  # Punt
            (int(self.x + self.width), int(self.y + self.height - wing_offset))  # Onderkant
        ]
        pygame.draw.polygon(screen, self.wing_color, right_wing_points)

        # Teken oogjes (kleine rode puntjes)
        eye_radius = 2
        left_eye_pos = (int(self.x + self.width // 3), int(self.y + self.height // 2))
        right_eye_pos = (int(self.x + 2 * self.width // 3), int(self.y + self.height // 2))
        pygame.draw.circle(screen, self.eye_color, left_eye_pos, eye_radius)
        pygame.draw.circle(screen, self.eye_color, right_eye_pos, eye_radius)
