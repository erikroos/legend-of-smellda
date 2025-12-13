import pygame
from constants import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_MAX_HEALTH,
    PLAYER_ATTACK_COOLDOWN, PLAYER_INVINCIBILITY_FRAMES,
    SWORD_LENGTH, SWORD_WIDTH, SWORD_WIDTH_RENDER, HALF_PLAYER_WIDTH_MINUS_SWORD,
    TUNIC_COLOR, SKIN_COLOR, HAIR_COLOR, BELT_COLOR,
    SWORD_BLADE_COLOR, SWORD_HANDLE_COLOR, SHIELD_COLOR, SHIELD_EDGE_COLOR
)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Zwaard aanval
        self.has_sword = False  # Speler begint ZONDER zwaard
        self.attacking = False
        self.attack_cooldown = 0
        self.attack_duration = 10  # Aantal frames dat de aanval zichtbaar is
        self.attack_timer = 0  # Timer voor aanval animatie
        self.facing = 'down'  # richting waar speler naar kijkt

        # Inventory
        self.has_key = False  # Dungeon sleutel
        self.rupees = 0  # Geldsysteem
        self.has_shield = False  # Schild voor bescherming tegen pijlen

        # Health systeem
        self.max_health = PLAYER_MAX_HEALTH
        self.health = PLAYER_MAX_HEALTH
        self.invincible = False  # Tijdelijk onoverwinnelijk na schade
        self.invincible_timer = 0
        self.alive = True
        
    def update(self, keys):
        # Beweging
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            dx = self.speed
            self.facing = 'right'
        if keys[pygame.K_UP]:
            dy = -self.speed
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            dy = self.speed
            self.facing = 'down'
            
        self.x += dx
        self.y += dy
        self.rect.x = self.x
        self.rect.y = self.y

        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Update attack animation timer
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer == 0:
                self.attacking = False

        # Update invincibility
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            if self.invincible_timer == 0:
                self.invincible = False

    def attack(self):
        """Trigger een zwaard aanval (call this from event handler)
        Returns True als aanval succesvol was, False als nog in cooldown of geen zwaard"""
        if not self.has_sword:
            return False  # Kan niet aanvallen zonder zwaard!

        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
            self.attack_timer = self.attack_duration
            return True
        return False

    def take_damage(self, amount=1):
        """Neem schade en word tijdelijk onoverwinnelijk"""
        if not self.invincible and self.alive:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.alive = False
            else:
                # Word tijdelijk onoverwinnelijk
                self.invincible = True
                self.invincible_timer = PLAYER_INVINCIBILITY_FRAMES
            return True
        return False

    def can_block_arrow(self, arrow_x, arrow_y, arrow_dx, arrow_dy):
        """Check of het schild een pijl kan blokkeren op basis van richting"""
        if not self.has_shield:
            return False

        # Bereken vanuit welke richting de pijl komt
        # arrow_dx en arrow_dy zijn genormaliseerde richting vectoren

        # Pijl komt van links (positieve dx betekent pijl gaat naar rechts)
        if arrow_dx > 0.5 and self.facing == 'left':
            return True
        # Pijl komt van rechts (negatieve dx betekent pijl gaat naar links)
        elif arrow_dx < -0.5 and self.facing == 'right':
            return True
        # Pijl komt van boven (positieve dy betekent pijl gaat naar beneden)
        elif arrow_dy > 0.5 and self.facing == 'up':
            return True
        # Pijl komt van onder (negatieve dy betekent pijl gaat naar boven)
        elif arrow_dy < -0.5 and self.facing == 'down':
            return True

        return False

    def get_attack_rect(self):
        # Geef hitbox terug gebaseerd op facing richting
        if self.facing == 'left':
            return pygame.Rect(self.x - SWORD_LENGTH, self.y, SWORD_LENGTH, SWORD_WIDTH)
        elif self.facing == 'right':
            return pygame.Rect(self.x + self.width, self.y, SWORD_LENGTH, SWORD_WIDTH)
        elif self.facing == 'up':
            return pygame.Rect(self.x, self.y - SWORD_LENGTH, SWORD_WIDTH, SWORD_LENGTH)
        else:  # down
            return pygame.Rect(self.x, self.y + self.height, SWORD_WIDTH, SWORD_LENGTH)
    
    def get_attack_rect_for_render(self):
        if self.facing == 'left':
            return pygame.Rect(self.x - SWORD_LENGTH, self.y + HALF_PLAYER_WIDTH_MINUS_SWORD, SWORD_LENGTH, SWORD_WIDTH_RENDER)
        elif self.facing == 'right':
            return pygame.Rect(self.x + self.width, self.y + HALF_PLAYER_WIDTH_MINUS_SWORD, SWORD_LENGTH, SWORD_WIDTH_RENDER)
        elif self.facing == 'up':
            return pygame.Rect(self.x + HALF_PLAYER_WIDTH_MINUS_SWORD, self.y - SWORD_LENGTH, SWORD_WIDTH_RENDER, SWORD_LENGTH)
        else:  # down
            return pygame.Rect(self.x + HALF_PLAYER_WIDTH_MINUS_SWORD, self.y + self.height, SWORD_WIDTH_RENDER, SWORD_LENGTH)

    def render(self, screen):
        # Skip rendering elke paar frames als invincible (knipperen)
        if self.invincible and (self.invincible_timer // 5) % 2 == 0:
            return

        cx = self.x + self.width // 2

        if self.facing == 'down':
            # Lichaam (tuniek) - eerst tekenen
            pygame.draw.rect(screen, TUNIC_COLOR, (self.x + 8, self.y + 16, 24, 18))
            # Hoofd
            pygame.draw.circle(screen, SKIN_COLOR, (cx, self.y + 10), 8)
            # Haar/pet
            pygame.draw.circle(screen, HAIR_COLOR, (cx, self.y + 8), 9)
            # Benen
            pygame.draw.rect(screen, TUNIC_COLOR, (self.x + 10, self.y + 30, 8, 10))
            pygame.draw.rect(screen, TUNIC_COLOR, (self.x + 22, self.y + 30, 8, 10))
            # Riem
            pygame.draw.rect(screen, BELT_COLOR, (self.x + 8, self.y + 23, 24, 3))

            # Schild (over alles heen, aan de voorkant, als speler het heeft)
            if self.has_shield:
                shield_x = self.x + 4
                shield_y = self.y + 16
                shield_width = 14
                shield_height = 20
                # Schild vorm
                pygame.draw.rect(screen, SHIELD_COLOR, (shield_x, shield_y, shield_width, shield_height))
                # Donkere rand
                pygame.draw.rect(screen, SHIELD_EDGE_COLOR, (shield_x, shield_y, shield_width, shield_height), 2)
                # Decoratief kruisje
                center_x_shield = shield_x + shield_width // 2
                center_y_shield = shield_y + shield_height // 2
                # Verticale lijn
                pygame.draw.line(screen, SHIELD_EDGE_COLOR,
                                (center_x_shield, shield_y + 4),
                                (center_x_shield, shield_y + shield_height - 4), 2)
                # Horizontale lijn
                pygame.draw.line(screen, SHIELD_EDGE_COLOR,
                                (shield_x + 3, center_y_shield),
                                (shield_x + shield_width - 3, center_y_shield), 2)

        elif self.facing == 'up':
            # Lichaam (tuniek)
            pygame.draw.rect(screen, TUNIC_COLOR, (self.x + 8, self.y + 12, 24, 18))
            # Hoofd (achterkant)
            pygame.draw.circle(screen, HAIR_COLOR, (cx, self.y + 8), 9)
            # Benen
            pygame.draw.rect(screen, TUNIC_COLOR, (self.x + 10, self.y + 26, 8, 10))
            pygame.draw.rect(screen, TUNIC_COLOR, (self.x + 22, self.y + 26, 8, 10))
            # Riem
            pygame.draw.rect(screen, BELT_COLOR, (self.x + 8, self.y + 19, 24, 3))
            # Geen schild rendering bij 'up' - schild is niet zichtbaar op de rug

        elif self.facing == 'left':
            # Lichaam (tuniek)
            pygame.draw.rect(screen, TUNIC_COLOR, (self.x + 10, self.y + 16, 20, 18))
            # Hoofd
            pygame.draw.circle(screen, SKIN_COLOR, (self.x + 14, self.y + 10), 8)
            # Haar/pet
            pygame.draw.circle(screen, HAIR_COLOR, (self.x + 14, self.y + 8), 9)
            # Benen
            pygame.draw.rect(screen, TUNIC_COLOR, (self.x + 14, self.y + 30, 10, 10))
            # Riem
            pygame.draw.rect(screen, BELT_COLOR, (self.x + 10, self.y + 23, 20, 3))
            # Schild (dunne streep aan de voorkant/zijkant)
            if self.has_shield:
                pygame.draw.line(screen, SHIELD_COLOR, (self.x + 8, self.y + 18), (self.x + 8, self.y + 32), 3)

        elif self.facing == 'right':
            # Lichaam (tuniek)
            pygame.draw.rect(screen, TUNIC_COLOR, (self.x + 10, self.y + 16, 20, 18))
            # Hoofd
            pygame.draw.circle(screen, SKIN_COLOR, (self.x + 26, self.y + 10), 8)
            # Haar/pet
            pygame.draw.circle(screen, HAIR_COLOR, (self.x + 26, self.y + 8), 9)
            # Benen
            pygame.draw.rect(screen, TUNIC_COLOR, (self.x + 16, self.y + 30, 10, 10))
            # Riem
            pygame.draw.rect(screen, BELT_COLOR, (self.x + 10, self.y + 23, 20, 3))
            # Schild (dunne streep aan de voorkant/zijkant)
            if self.has_shield:
                pygame.draw.line(screen, SHIELD_COLOR, (self.x + 32, self.y + 18), (self.x + 32, self.y + 32), 3)

        # Teken zwaard tijdens aanval
        if self.attacking:
            attack_rect = self.get_attack_rect_for_render()

            if self.facing in ['left', 'right']:
                # Horizontaal zwaard
                pygame.draw.rect(screen, SWORD_BLADE_COLOR, attack_rect)
                if self.facing == 'left':
                    pygame.draw.rect(screen, SWORD_HANDLE_COLOR, (attack_rect.right - 8, attack_rect.y, 8, attack_rect.height))
                else:
                    pygame.draw.rect(screen, SWORD_HANDLE_COLOR, (attack_rect.x, attack_rect.y, 8, attack_rect.height))
            else:
                # Verticaal zwaard
                pygame.draw.rect(screen, SWORD_BLADE_COLOR, attack_rect)
                if self.facing == 'up':
                    pygame.draw.rect(screen, SWORD_HANDLE_COLOR, (attack_rect.x, attack_rect.bottom - 8, attack_rect.width, 8))
                else:
                    pygame.draw.rect(screen, SWORD_HANDLE_COLOR, (attack_rect.x, attack_rect.y, attack_rect.width, 8))