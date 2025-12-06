import pygame
import random
from constants import (
    MONSTER_WIDTH, MONSTER_HEIGHT, MONSTER_SPEED, MONSTER_HEALTH,
    MONSTER_DAMAGE_COOLDOWN, WALL_THICKNESS, HUD_HEIGHT,
    MONSTER_BODY_COLOR, MONSTER_EYE_COLOR, MONSTER_PUPIL_COLOR
)

class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = MONSTER_WIDTH
        self.height = MONSTER_HEIGHT
        self.speed = MONSTER_SPEED
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Random bewegingsrichting
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.direction_timer = 0
        self.direction_change_interval = random.randint(60, 180)  # frames

        # Health
        self.health = MONSTER_HEALTH
        self.alive = True

        # Damage cooldown (om te voorkomen dat speler continu schade neemt)
        self.can_damage = True
        self.damage_cooldown = 0

    def update(self, obstacles, screen_width, screen_height, hud_height=HUD_HEIGHT, pushable_block=None):
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
        # Horizontale muren (links/rechts)
        if self.x < WALL_THICKNESS or self.x + self.width > screen_width - WALL_THICKNESS:
            self.x = old_x
            self.direction = random.choice(['left', 'right', 'up', 'down'])
            self.direction_timer = 0

        # Verticale muren (boven/onder) - rekening houdend met HUD
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

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.alive = False

    def reset_damage_cooldown(self):
        self.can_damage = False
        self.damage_cooldown = MONSTER_DAMAGE_COOLDOWN

    def render(self, screen):
        if not self.alive:
            return

        # Eenvoudig monster: rood vierkant met ogen
        # Lichaam
        pygame.draw.rect(screen, MONSTER_BODY_COLOR, self.rect)

        # Ogen
        eye_y = self.y + 10
        # Links oog
        pygame.draw.circle(screen, MONSTER_EYE_COLOR, (int(self.x + 10), int(eye_y)), 4)
        pygame.draw.circle(screen, MONSTER_PUPIL_COLOR, (int(self.x + 10), int(eye_y)), 2)
        # Rechts oog
        pygame.draw.circle(screen, MONSTER_EYE_COLOR, (int(self.x + 20), int(eye_y)), 4)
        pygame.draw.circle(screen, MONSTER_PUPIL_COLOR, (int(self.x + 20), int(eye_y)), 2)
