import pygame
import random

class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 70
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.alive = True
        self.health = 3  # 3 hits nodig om te verslaan

        # Movement
        self.speed = 1
        self.direction = 1  # 1 = rechts, -1 = links
        self.move_range_x = 150  # Hoe ver heen en weer
        self.start_x = x

        # Fireball attack
        self.fireball_cooldown = 0
        self.fireball_cooldown_max = 180  # 3 seconden @ 60 FPS
        self.fireballs = []

        # Damage cooldown (om te voorkomen dat je hem te snel meerdere keren raakt)
        self.damage_cooldown = 0
        self.damage_cooldown_max = 30
        self.hit_flash_timer = 0  # Timer voor knippereffect

        # Colors
        self.body_color = (150, 50, 50)  # Donkerrood
        self.belly_color = (200, 100, 100)  # Lichter rood
        self.eye_color = (255, 255, 0)  # Geel
        self.horn_color = (80, 30, 30)  # Donkerder rood

    def take_damage(self):
        """Neem schade van zwaard"""
        if self.damage_cooldown == 0:
            self.health -= 1
            self.damage_cooldown = self.damage_cooldown_max
            self.hit_flash_timer = 15  # Knipper voor 15 frames

            if self.health <= 0:
                self.alive = False
            return True
        return False

    def update(self, player, hud_height, screen_width, screen_height, boss_sound=None):
        """Update boss movement en fireball attacks"""
        if not self.alive:
            return

        # Update damage cooldown
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        # Update hit flash timer
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1

        # Beweeg heen en weer
        self.x += self.speed * self.direction

        # Check of we van richting moeten wisselen
        if self.direction == 1 and self.x >= self.start_x + self.move_range_x:
            self.direction = -1
        elif self.direction == -1 and self.x <= self.start_x:
            self.direction = 1

        self.rect.x = self.x

        # Update fireball cooldown
        if self.fireball_cooldown > 0:
            self.fireball_cooldown -= 1
        else:
            # Shoot fireball naar player
            self.shoot_fireball(player.x, player.y)
            self.fireball_cooldown = self.fireball_cooldown_max

            # Speel boss geluid af
            if boss_sound:
                boss_sound.play()

        # Update fireballs
        for fireball in self.fireballs[:]:
            fireball.update()

            # Verwijder fireballs die buiten scherm zijn
            if (fireball.x < 0 or fireball.x > screen_width or
                fireball.y < hud_height or fireball.y > hud_height + screen_height):
                self.fireballs.remove(fireball)

    def shoot_fireball(self, target_x, target_y):
        """Schiet een vuurbal richting de speler"""
        # Bereken richting naar speler
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2

        dx = target_x - center_x
        dy = target_y - center_y

        # Normaliseer de richting
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            dx /= distance
            dy /= distance

        # Maak nieuwe fireball
        fireball = Fireball(center_x, center_y, dx, dy)
        self.fireballs.append(fireball)

    def render(self, screen):
        """Teken de boss (draak)"""
        if not self.alive:
            return

        # Skip rendering elke paar frames als boss hit is (knippereffect)
        if self.hit_flash_timer > 0 and (self.hit_flash_timer // 3) % 2 == 0:
            return

        # Draak lichaam (ovaal)
        body_rect = pygame.Rect(self.x + 10, self.y + 20, self.width - 20, self.height - 30)
        pygame.draw.ellipse(screen, self.body_color, body_rect)

        # Buik (lichtere kleur)
        belly_rect = pygame.Rect(self.x + 20, self.y + 30, self.width - 40, self.height - 45)
        pygame.draw.ellipse(screen, self.belly_color, belly_rect)

        # Hoofd (cirkel)
        head_x = self.x + self.width // 2
        head_y = self.y + 15
        pygame.draw.circle(screen, self.body_color, (head_x, head_y), 18)

        # Ogen (geel, dreigend)
        left_eye_x = head_x - 8
        right_eye_x = head_x + 8
        eye_y = head_y - 3
        pygame.draw.circle(screen, self.eye_color, (left_eye_x, eye_y), 4)
        pygame.draw.circle(screen, self.eye_color, (right_eye_x, eye_y), 4)

        # Pupillen (zwart)
        pygame.draw.circle(screen, (0, 0, 0), (left_eye_x, eye_y), 2)
        pygame.draw.circle(screen, (0, 0, 0), (right_eye_x, eye_y), 2)

        # Hoorns
        left_horn = [
            (head_x - 15, head_y - 10),
            (head_x - 12, head_y - 18),
            (head_x - 10, head_y - 10)
        ]
        right_horn = [
            (head_x + 15, head_y - 10),
            (head_x + 12, head_y - 18),
            (head_x + 10, head_y - 10)
        ]
        pygame.draw.polygon(screen, self.horn_color, left_horn)
        pygame.draw.polygon(screen, self.horn_color, right_horn)

        # Poten (4 korte rechthoeken)
        leg_width = 8
        leg_height = 15
        # Linker voorpoot
        pygame.draw.rect(screen, self.body_color, (self.x + 15, self.y + self.height - leg_height, leg_width, leg_height))
        # Rechter voorpoot
        pygame.draw.rect(screen, self.body_color, (self.x + self.width - 15 - leg_width, self.y + self.height - leg_height, leg_width, leg_height))
        # Linker achterpoot
        pygame.draw.rect(screen, self.body_color, (self.x + 15, self.y + self.height - leg_height - 5, leg_width, leg_height))
        # Rechter achterpoot
        pygame.draw.rect(screen, self.body_color, (self.x + self.width - 15 - leg_width, self.y + self.height - leg_height - 5, leg_width, leg_height))

        # Staart (driehoek aan de achterkant)
        tail_points = [
            (self.x + 10, self.y + 30),
            (self.x - 10, self.y + 35),
            (self.x + 10, self.y + 40)
        ]
        pygame.draw.polygon(screen, self.body_color, tail_points)

        # Render fireballs
        for fireball in self.fireballs:
            fireball.render(screen)


class Fireball:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx * 3  # Snelheid
        self.dy = dy * 3
        self.radius = 8
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)

        # Colors voor vuurbal effect
        self.colors = [
            (255, 69, 0),   # Oranje-rood
            (255, 140, 0),  # Donker oranje
            (255, 215, 0)   # Goud
        ]

    def update(self):
        """Update fireball positie"""
        self.x += self.dx
        self.y += self.dy
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def render(self, screen):
        """Teken de vuurbal met een vuur effect"""
        # Teken meerdere cirkels voor een gloeiend effect
        pygame.draw.circle(screen, self.colors[0], (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, self.colors[1], (int(self.x), int(self.y)), self.radius - 2)
        pygame.draw.circle(screen, self.colors[2], (int(self.x), int(self.y)), self.radius - 4)
