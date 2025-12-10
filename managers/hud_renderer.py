import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, HUD_HEIGHT, GAME_HEIGHT,
    HUD_BG_COLOR, HUD_BORDER_COLOR,
    MINIMAP_ROOM_SIZE, MINIMAP_ROOM_SPACING, MINIMAP_START_X,
    MINIMAP_VISITED_ROOM_COLOR, MINIMAP_CURRENT_ROOM_COLOR, MINIMAP_UNVISITED_ROOM_COLOR,
    HEART_SIZE, HEART_SPACING, HEART_FULL_COLOR, HEART_EMPTY_COLOR,
    KEY_COLOR, KEY_DARK_COLOR,
    GAME_OVER_TEXT_COLOR, GAME_OVER_SUBTITLE_COLOR, OVERLAY_COLOR
)

class HUDRenderer:
    def __init__(self, screen):
        self.screen = screen

    def render_hud(self, player, room_manager, in_dungeon, dungeon_manager):
        """Render de HUD bar bovenaan het scherm"""
        # Teken HUD achtergrond
        pygame.draw.rect(self.screen, HUD_BG_COLOR, (0, 0, SCREEN_WIDTH, HUD_HEIGHT))

        # Teken een rand onderaan de HUD
        pygame.draw.line(self.screen, HUD_BORDER_COLOR, (0, HUD_HEIGHT - 1), (SCREEN_WIDTH, HUD_HEIGHT - 1), 2)

        # Render minimap (links)
        self.render_minimap(room_manager, in_dungeon, dungeon_manager)

        # Render hartjes in de HUD
        self.render_hearts(player)

        # Render inventory (midden-rechts)
        self.render_inventory(player)

    def render_minimap(self, room_manager, in_dungeon, dungeon_manager):
        """Render de minimap in de linkerhoek van de HUD"""
        if in_dungeon:
            # Render dungeon minimap - kruisvorm met 5 kamers
            # Layout:
            #     [N] (0, -1)
            #      |
            # [W]-[M]-[E]  (-1,0) (0,0) (1,0)
            #      |
            #     [S] (0, 1)

            # Bereken centrum positie voor de kruisvorm
            center_x = MINIMAP_START_X + MINIMAP_ROOM_SIZE + MINIMAP_ROOM_SPACING
            center_y = (HUD_HEIGHT - MINIMAP_ROOM_SIZE) // 2

            # Dungeon rooms coordinaten (relatief in de dungeon)
            dungeon_rooms = [
                (0, -1),   # North
                (-1, 0),   # West
                (0, 0),    # Center
                (1, 0),    # East
                (0, 1),    # South (start)
            ]

            current_room = dungeon_manager.current_room

            for room_x, room_y in dungeon_rooms:
                # Bereken scherm positie voor deze room
                screen_x = center_x + (room_x * (MINIMAP_ROOM_SIZE + MINIMAP_ROOM_SPACING))
                screen_y = center_y + (room_y * (MINIMAP_ROOM_SIZE + MINIMAP_ROOM_SPACING))

                # Bepaal kleur: current room of visited room
                if (room_x, room_y) == current_room:
                    color = MINIMAP_CURRENT_ROOM_COLOR
                elif (room_x, room_y) in dungeon_manager.visited_rooms:
                    color = MINIMAP_VISITED_ROOM_COLOR
                else:
                    color = MINIMAP_UNVISITED_ROOM_COLOR

                # Teken room blokje
                pygame.draw.rect(self.screen, color,
                               (screen_x, screen_y, MINIMAP_ROOM_SIZE, MINIMAP_ROOM_SIZE))
        else:
            # Render overworld minimap
            start_y = (HUD_HEIGHT - (room_manager.world_height * (MINIMAP_ROOM_SIZE + MINIMAP_ROOM_SPACING))) // 2

            # Teken alle rooms in de wereld
            for y in range(room_manager.world_height):
                for x in range(room_manager.world_width):
                    # Bereken positie van dit room blokje
                    block_x = MINIMAP_START_X + (x * (MINIMAP_ROOM_SIZE + MINIMAP_ROOM_SPACING))
                    block_y = start_y + (y * (MINIMAP_ROOM_SIZE + MINIMAP_ROOM_SPACING))

                    # Check of dit de huidige room is
                    if (x, y) == room_manager.current_room:
                        color = MINIMAP_CURRENT_ROOM_COLOR
                    else:
                        color = MINIMAP_VISITED_ROOM_COLOR

                    # Teken het room blokje
                    pygame.draw.rect(self.screen, color, (block_x, block_y, MINIMAP_ROOM_SIZE, MINIMAP_ROOM_SIZE))

    def render_hearts(self, player):
        """Teken hartjes in de HUD"""
        # Bereken aantal hartjes op basis van max_health (elk hartje = 2 health)
        num_hearts = player.max_health // 2
        start_x = SCREEN_WIDTH - 10 - (num_hearts * HEART_SPACING)  # Dynamisch aantal hartjes, rechts in HUD
        start_y = (HUD_HEIGHT - HEART_SIZE) // 2  # Verticaal gecentreerd in HUD

        for i in range(num_hearts):  # Dynamisch aantal hartjes
            x = start_x + (i * HEART_SPACING)
            health_for_this_heart = player.health - (i * 2)

            # Bepaal of het hartje vol, half of leeg is
            if health_for_this_heart >= 2:
                # Vol hart
                self.draw_heart(x, start_y, HEART_SIZE, 'full')
            elif health_for_this_heart == 1:
                # Half hart
                self.draw_heart(x, start_y, HEART_SIZE, 'half')
            else:
                # Leeg hart
                self.draw_heart(x, start_y, HEART_SIZE, 'empty')

    def draw_heart(self, x, y, size, state):
        """Teken een enkel hartje"""
        heart_color = HEART_FULL_COLOR if state != 'empty' else HEART_EMPTY_COLOR

        # Teken een simpel hart met cirkels en een driehoek
        # Twee bovencirkels
        pygame.draw.circle(self.screen, heart_color, (x + size // 4, y + size // 3), size // 4)
        pygame.draw.circle(self.screen, heart_color, (x + 3 * size // 4, y + size // 3), size // 4)

        # Onderste driehoek
        points = [
            (x, y + size // 3),
            (x + size, y + size // 3),
            (x + size // 2, y + size)
        ]
        pygame.draw.polygon(self.screen, heart_color, points)

        # Als half hart, teken grijze helft over de rechterkant
        if state == 'half':
            pygame.draw.circle(self.screen, HEART_EMPTY_COLOR, (x + 3 * size // 4, y + size // 3), size // 4)
            right_points = [
                (x + size // 2, y + size // 3),
                (x + size, y + size // 3),
                (x + size // 2, y + size)
            ]
            pygame.draw.polygon(self.screen, HEART_EMPTY_COLOR, right_points)

    def render_inventory(self, player):
        """Render inventory items in de HUD (midden-rechts)"""
        # Positie: tussen de minimap en de hartjes
        inv_x = SCREEN_WIDTH // 2
        inv_y = (HUD_HEIGHT - 30) // 2  # Verticaal gecentreerd

        # Teken rupee counter (altijd zichtbaar)
        self.draw_rupee_counter(inv_x - 80, inv_y, player.rupees)

        # Teken sleutel als speler deze heeft
        if player.has_key:
            self.draw_key_icon(inv_x + 50, inv_y, 30)

    def draw_rupee_counter(self, x, y, count):
        """Teken rupee symbool met teller"""
        # Teken rupee diamant symbool (groen-geel voor 1 rupee)
        rupee_size = 20
        rupee_center_x = x + rupee_size // 2
        rupee_center_y = y + rupee_size // 2

        # Diamant vorm (4 punten)
        points = [
            (rupee_center_x, rupee_center_y - rupee_size // 2),  # Boven
            (rupee_center_x + rupee_size // 2, rupee_center_y),  # Rechts
            (rupee_center_x, rupee_center_y + rupee_size // 2),  # Onder
            (rupee_center_x - rupee_size // 2, rupee_center_y),  # Links
        ]

        # Groen-geel gradient effect: teken meerdere lagen
        pygame.draw.polygon(self.screen, (100, 200, 50), points)  # Groen-geel basis

        # Donkere rand voor contrast
        pygame.draw.polygon(self.screen, (50, 100, 25), points, 2)

        # Highlight voor glans effect (kleine witte driehoek bovenin)
        highlight_points = [
            (rupee_center_x - 4, rupee_center_y - 4),
            (rupee_center_x + 4, rupee_center_y - 4),
            (rupee_center_x, rupee_center_y + 2),
        ]
        pygame.draw.polygon(self.screen, (200, 255, 150), highlight_points)

        # Teken teller rechts naast het symbool
        font = pygame.font.Font(None, 28)
        count_text = font.render(f"x {count}", True, (255, 255, 255))
        self.screen.blit(count_text, (x + rupee_size + 8, y + 5))

    def draw_key_icon(self, x, y, size):
        """Teken een sleutel icoon in de HUD"""
        # Key kleuren (goudgeel)
        color = KEY_COLOR
        dark_color = KEY_DARK_COLOR

        # Hoofd van de sleutel (cirkel)
        head_radius = size // 3
        head_center = (x + head_radius, y + head_radius)
        pygame.draw.circle(self.screen, color, head_center, head_radius)
        pygame.draw.circle(self.screen, dark_color, head_center, head_radius // 2)

        # Steel van de sleutel
        shaft_start = (x + head_radius, y + head_radius * 2)
        shaft_end = (x + head_radius, y + size)
        pygame.draw.line(self.screen, color, shaft_start, shaft_end, 4)

        # Tanden van de sleutel
        tooth_width = 6
        tooth_height = 4
        tooth1_y = y + size - 10
        tooth2_y = y + size - 5

        pygame.draw.rect(self.screen, color,
                        (x + head_radius, tooth1_y, tooth_width, tooth_height))
        pygame.draw.rect(self.screen, color,
                        (x + head_radius, tooth2_y, tooth_width, tooth_height))

    def render_game_over(self, player):
        """Render game over screen als speler dood is"""
        if not player.alive:
            # Semi-transparante overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(OVERLAY_COLOR)
            self.screen.blit(overlay, (0, 0))

            # Game Over tekst
            try:
                font = pygame.font.Font(None, 74)
                text = font.render('GAME OVER', True, GAME_OVER_TEXT_COLOR)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
                self.screen.blit(text, text_rect)

                font_small = pygame.font.Font(None, 36)
                restart_text = font_small.render('Press ESC to quit', True, GAME_OVER_SUBTITLE_COLOR)
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
                self.screen.blit(restart_text, restart_rect)
            except:
                pass
