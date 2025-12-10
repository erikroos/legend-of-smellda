import pygame
from rooms.base_cave_room import BaseCaveRoom
from entities.old_man import OldMan
from items.heart_container import HeartContainer
from constants import HUD_HEIGHT

class ShopCaveRoom(BaseCaveRoom):
    """Een cave room met een shop - oude man verkoopt een heart container"""

    def __init__(self):
        super().__init__()

        # Plaats oude man in het midden-boven
        old_man_x = self.screen_width // 2 - 20
        old_man_y = HUD_HEIGHT + 120
        self.old_man = OldMan(old_man_x, old_man_y)
        # Pas tekst aan voor shop
        self.old_man.text = "BUY EXTRA HEALTH HERE"
        self.old_man.text2 = ""

        # Plaats heart container voor de oude man
        heart_x = self.screen_width // 2 - 15
        heart_y = HUD_HEIGHT + 250
        self.heart_container = HeartContainer(heart_x, heart_y)
        self.heart_container_price = 50

        # Track of item al gekocht is
        self.item_purchased = False

    def update(self):
        """Update de shop cave"""
        if not self.item_purchased and not self.heart_container.collected:
            self.heart_container.update()

    def check_purchase(self, player):
        """Check of speler de heart container koopt"""
        if self.item_purchased or self.heart_container.collected:
            return False

        # Check of speler genoeg rupees heeft en over het item heen loopt
        if player.rupees >= self.heart_container_price:
            if player.rect.colliderect(self.heart_container.rect):
                # Aankoop!
                player.rupees -= self.heart_container_price
                player.max_health += 2  # +1 hartje = +2 HP
                player.health = player.max_health  # Vul alle hartjes
                self.heart_container.collected = True
                self.item_purchased = True
                # Verberg oude man na aankoop
                self.old_man.visible = False
                return True

        return False

    def render(self, screen, hud_height):
        """Render de shop cave"""
        # Render de basis cave (muren, exit, etc)
        super().render(screen, hud_height)

        # Render oude man
        self.old_man.render(screen)

        # Render heart container als deze nog niet gekocht is
        if not self.item_purchased and not self.heart_container.collected:
            self.heart_container.render(screen)

            # Render prijs boven de heart container
            font = pygame.font.Font(None, 32)
            price_text = font.render(f"{self.heart_container_price}", True, (255, 215, 0))

            # Teken een klein rupee symbool naast de prijs
            rupee_size = 12
            text_width = price_text.get_width()

            # Positie: gecentreerd boven de heart container
            total_width = rupee_size + 4 + text_width
            price_x = self.heart_container.x + (self.heart_container.width // 2) - (total_width // 2)
            price_y = self.heart_container.y - 35

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
