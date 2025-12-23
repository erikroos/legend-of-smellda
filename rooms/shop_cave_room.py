import pygame
from rooms.base_cave_room import BaseCaveRoom
from entities.old_man import OldMan
from items.heart_container import HeartContainer
from items.shield_item import ShieldItem
from world.fire import Fire
from constants import HUD_HEIGHT, GAME_WIDTH, GAME_HEIGHT

class ShopCaveRoom(BaseCaveRoom):
    """Een cave room met een shop - oude man verkoopt een heart container"""

    def __init__(self):
        super().__init__()

        # Overschrijf vuren voor meer ruimte in de shop
        center_x = GAME_WIDTH // 2
        center_y = HUD_HEIGHT + GAME_HEIGHT // 2
        self.fires = [
            Fire(center_x - 120, center_y - 40),  # Linker vuur verder naar links
            Fire(center_x + 100, center_y - 40)   # Rechter vuur verder naar rechts
        ]

        # Plaats oude man in het midden-boven
        old_man_x = self.screen_width // 2 - 20
        old_man_y = HUD_HEIGHT + 120
        self.old_man = OldMan(old_man_x, old_man_y)
        # Pas tekst aan voor shop
        self.old_man.text = "BUY SOMETHING, WILL YA!"
        self.old_man.text2 = ""

        # Plaats heart container links voor de oude man
        heart_x = self.screen_width // 2 - 60
        heart_y = HUD_HEIGHT + 250
        self.heart_container = HeartContainer(heart_x, heart_y)
        self.heart_container_price = 30

        # Plaats schild rechts voor de oude man
        shield_x = self.screen_width // 2 + 30
        shield_y = HUD_HEIGHT + 250
        self.shield = ShieldItem(shield_x, shield_y)
        self.shield_price = 20

        # Track welke items al gekocht zijn
        self.heart_purchased = False
        self.shield_purchased = False

    def update(self):
        """Update de shop cave"""
        if not self.heart_purchased and not self.heart_container.collected:
            self.heart_container.update()
        if not self.shield_purchased and not self.shield.collected:
            self.shield.update()

    def check_purchase(self, player):
        """Check of speler items koopt (heart container of schild)"""
        purchased = False

        # Check heart container aankoop
        if not self.heart_purchased and not self.heart_container.collected:
            if player.rupees >= self.heart_container_price:
                if player.rect.colliderect(self.heart_container.rect):
                    # Aankoop!
                    player.rupees -= self.heart_container_price
                    player.max_health += 2  # +1 hartje = +2 HP
                    player.health = player.max_health  # Vul alle hartjes
                    self.heart_container.collected = True
                    self.heart_purchased = True
                    purchased = True

        # Check schild aankoop
        if not self.shield_purchased and not self.shield.collected:
            if player.rupees >= self.shield_price:
                if player.rect.colliderect(self.shield.rect):
                    # Aankoop!
                    player.rupees -= self.shield_price
                    player.has_shield = True
                    self.shield.collected = True
                    self.shield_purchased = True
                    purchased = True

        # Verberg oude man als beide items gekocht zijn
        if self.heart_purchased and self.shield_purchased:
            self.old_man.visible = False

        return purchased

    def render(self, screen, hud_height):
        """Render de shop cave"""
        # Render de basis cave (muren, exit, etc)
        super().render(screen, hud_height)

        # Render oude man
        self.old_man.render(screen)

        # Render heart container als deze nog niet gekocht is
        if not self.heart_purchased and not self.heart_container.collected:
            self.heart_container.render(screen)
            self._render_price(screen, self.heart_container, self.heart_container_price)

        # Render schild als deze nog niet gekocht is
        if not self.shield_purchased and not self.shield.collected:
            self.shield.render(screen)
            self._render_price(screen, self.shield, self.shield_price)

    def _render_price(self, screen, item, price):
        """Helper methode om prijs boven een item te renderen"""
        # Render prijs boven het item
        font = pygame.font.Font(None, 32)
        price_text = font.render(f"{price}", True, (255, 215, 0))

        # Teken een klein rupee symbool naast de prijs
        rupee_size = 12
        text_width = price_text.get_width()

        # Positie: gecentreerd boven het item
        total_width = rupee_size + 4 + text_width
        price_x = item.x + (item.width // 2) - (total_width // 2)
        price_y = item.y - 35

        # Teken rupee symbool
        rupee_center_x = price_x + rupee_size // 2
        rupee_center_y = price_y + 12

        rupee_points = [
            (rupee_center_x, rupee_center_y - rupee_size // 2),  # Boven
            (rupee_center_x + rupee_size // 2, rupee_center_y),  # Rechts
            (rupee_center_x, rupee_center_y + rupee_size // 2),  # Onder
            (rupee_center_x - rupee_size // 2, rupee_center_y),  # Links
        ]

        pygame.draw.polygon(screen, (100, 200, 50), rupee_points)
        pygame.draw.polygon(screen, (50, 100, 25), rupee_points, 1)

        # Teken prijs tekst
        screen.blit(price_text, (price_x + rupee_size + 4, price_y))
