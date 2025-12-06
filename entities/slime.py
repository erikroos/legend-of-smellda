import pygame
import random
from constants import (
    HUD_HEIGHT, WALL_THICKNESS,
    SLIME_LARGE_COLOR, SLIME_SMALL_COLOR, SLIME_HIGHLIGHT_COLOR
)

class Slime:
    def __init__(self, x, y, is_large=True):
        self.x = x
        self.y = y
        self.is_large = is_large

        # Grootte afhankelijk van type
        if is_large:
            self.width = 40
            self.height = 35
            self.health = 1  # 1 slag splits hem
            self.color = SLIME_LARGE_COLOR
        else:
            self.width = 20
            self.height = 18
            self.health = 1  # 1 slag doodt kleine slime
            self.color = SLIME_SMALL_COLOR

        self.rect = pygame.Rect(int(x), int(y), self.width, self.height)
        self.alive = True

        # Beweging - slimes bewegen langzaam
        self.speed = 0.8 if is_large else 1.2  # Kleine slimes iets sneller
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.direction_change_timer = 0
        self.direction_change_interval = random.randint(60, 120)  # Langzame richting veranderingen

        # Animatie - slimes "wiebelen"
        self.wobble_timer = 0
        self.wobble_offset = 0

        # Damage cooldown (om speler niet te vaak te raken)
        self.damage_cooldown = 0
        self.damage_cooldown_max = 60

        # Flag om te tracken of deze slime al gesplitst is
        self.has_split = False

    def take_damage(self, damage):
        """Neem schade - grote slimes splitsen, kleine slimes sterven"""
        self.health -= damage
        if self.health <= 0:
            if self.is_large and not self.has_split:
                # Grote slime splitst - parent class zal dit afhandelen
                self.has_split = True
                return True  # Return True om aan te geven dat split moet gebeuren
            else:
                # Kleine slime of al gesplitste grote slime sterft gewoon
                self.alive = False
                return False
        return False

    def update(self, obstacles, screen_width, screen_height, hud_height, pushable_block=None):
        """Update slime positie en gedrag"""
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
            self.direction_change_interval = random.randint(60, 120)

        # Beweeg in de huidige richting
        new_x = self.x + self.direction_x * self.speed
        new_y = self.y + self.direction_y * self.speed

        # Check grenzen (dungeon muren)
        if new_x < WALL_THICKNESS or new_x + self.width > screen_width - WALL_THICKNESS:
            self.direction_x *= -1  # Keer richting om
            new_x = self.x

        # Verticale grenzen
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

        # Update wobble animatie
        self.wobble_timer += 1
        if self.wobble_timer % 20 == 0:
            self.wobble_offset = random.randint(-2, 2)

    def render(self, screen):
        """Teken de slime als een druppelvorm"""
        if not self.alive:
            return

        # Teken hoofdlichaam (grote ellips/druppelvorm)
        body_rect = pygame.Rect(
            int(self.x),
            int(self.y + self.wobble_offset),
            self.width,
            int(self.height * 0.8)
        )
        pygame.draw.ellipse(screen, self.color, body_rect)

        # Teken bovenkant (kleinere cirkel voor druppelvorm)
        top_radius = self.width // 3
        top_center = (
            int(self.x + self.width // 2),
            int(self.y + top_radius // 2 + self.wobble_offset)
        )
        pygame.draw.circle(screen, self.color, top_center, top_radius)

        # Teken highlight (voor 3D effect)
        highlight_offset = 5
        highlight_radius = max(3, self.width // 6)
        highlight_center = (
            int(self.x + self.width // 3 + highlight_offset),
            int(self.y + self.height // 4 + self.wobble_offset)
        )
        pygame.draw.circle(screen, SLIME_HIGHLIGHT_COLOR, highlight_center, highlight_radius)
