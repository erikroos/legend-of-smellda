import pygame
import random
from entities.arrow import Arrow
from constants import (
    ARCHER_WIDTH, ARCHER_HEIGHT, ARCHER_SPEED, ARCHER_HEALTH,
    ARCHER_SHOOT_COOLDOWN, WALL_THICKNESS, HUD_HEIGHT,
    ARCHER_BODY_COLOR, ARCHER_EYE_COLOR, ARCHER_PUPIL_COLOR, ARCHER_BOW_COLOR,
    MONSTER_DAMAGE_COOLDOWN
)

class Archer:
    """Turkoois vijand die pijlen afvuurt"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = ARCHER_WIDTH
        self.height = ARCHER_HEIGHT
        self.speed = ARCHER_SPEED
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Random bewegingsrichting
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.direction_timer = 0
        self.direction_change_interval = random.randint(60, 180)

        # Health
        self.health = ARCHER_HEALTH
        self.alive = True

        # Damage cooldown (voor contact damage met speler)
        self.can_damage = True
        self.damage_cooldown = 0

        # Arrow shooting
        self.shoot_cooldown = 120  # Start met vertraging voordat eerste schot
        self.arrows = []

    def update(self, obstacles, screen_width, screen_height, hud_height, pushable_block, player):
        """Update archer beweging en pijlen"""
        if not self.alive:
            return

        # Verander af en toe van richting
        self.direction_timer += 1
        if self.direction_timer >= self.direction_change_interval:
            self.direction = random.choice(['left', 'right', 'up', 'down'])
            self.direction_timer = 0
            self.direction_change_interval = random.randint(60, 180)

        # Sla oude positie op
        old_x = self.x
        old_y = self.y

        # Beweeg in de huidige richting
        if self.direction == 'left':
            self.x -= self.speed
        elif self.direction == 'right':
            self.x += self.speed
        elif self.direction == 'up':
            self.y -= self.speed
        elif self.direction == 'down':
            self.y += self.speed

        # Update rect
        self.rect.x = self.x
        self.rect.y = self.y

        # Check muur collisions
        if self.x < WALL_THICKNESS or self.x + self.width > screen_width - WALL_THICKNESS:
            self.x = old_x
            self.direction = random.choice(['left', 'right', 'up', 'down'])
            self.direction_timer = 0

        if self.y < hud_height + WALL_THICKNESS or self.y + self.height > screen_height - WALL_THICKNESS:
            self.y = old_y
            self.direction = random.choice(['left', 'right', 'up', 'down'])
            self.direction_timer = 0

        # Check obstakel collisions
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.x = old_x
                self.y = old_y
                self.direction = random.choice(['left', 'right', 'up', 'down'])
                self.direction_timer = 0
                break

        # Check pushable block collision
        if pushable_block and self.rect.colliderect(pushable_block.rect):
            self.x = old_x
            self.y = old_y
            self.direction = random.choice(['left', 'right', 'up', 'down'])
            self.direction_timer = 0

        # Update rect met nieuwe positie
        self.rect.x = self.x
        self.rect.y = self.y

        # Update damage cooldown
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
            if self.damage_cooldown == 0:
                self.can_damage = True

        # Update shoot cooldown en schiet pijl
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        else:
            # Schiet pijl richting speler
            self.shoot_arrow(player.x + player.width // 2, player.y + player.height // 2)
            self.shoot_cooldown = ARCHER_SHOOT_COOLDOWN

        # Update arrows
        for arrow in self.arrows[:]:
            arrow.update()

        # Verwijder pijlen die buiten scherm zijn
        self.arrows = [arrow for arrow in self.arrows
                      if (0 <= arrow.x <= screen_width and
                          hud_height <= arrow.y <= screen_height)]

    def shoot_arrow(self, target_x, target_y):
        """Schiet een pijl richting het doel"""
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2

        dx = target_x - center_x
        dy = target_y - center_y

        # Normaliseer de richting
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            dx /= distance
            dy /= distance

        # Maak nieuwe pijl
        arrow = Arrow(center_x, center_y, dx, dy)
        self.arrows.append(arrow)

    def take_damage(self):
        """Neem schade van zwaard"""
        self.health -= 1
        if self.health <= 0:
            self.alive = False

    def reset_damage_cooldown(self):
        """Reset damage cooldown na contact met speler"""
        self.can_damage = False
        self.damage_cooldown = MONSTER_DAMAGE_COOLDOWN

    def render(self, screen):
        """Teken de archer"""
        if not self.alive:
            return

        # Turkoois lichaam
        pygame.draw.rect(screen, ARCHER_BODY_COLOR, self.rect)

        # Ogen
        eye_y = self.y + 10
        # Linker oog
        pygame.draw.circle(screen, ARCHER_EYE_COLOR, (int(self.x + 10), int(eye_y)), 4)
        pygame.draw.circle(screen, ARCHER_PUPIL_COLOR, (int(self.x + 10), int(eye_y)), 2)
        # Rechter oog
        pygame.draw.circle(screen, ARCHER_EYE_COLOR, (int(self.x + 20), int(eye_y)), 4)
        pygame.draw.circle(screen, ARCHER_PUPIL_COLOR, (int(self.x + 20), int(eye_y)), 2)

        # Boog (simpele boog aan de zijkant)
        bow_x = self.x + self.width - 5
        bow_y = self.y + self.height // 2
        pygame.draw.arc(screen, ARCHER_BOW_COLOR,
                       pygame.Rect(bow_x - 8, bow_y - 10, 12, 20),
                       -1.5, 1.5, 2)

        # Render arrows
        for arrow in self.arrows:
            arrow.render(screen)
