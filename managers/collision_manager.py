"""
CollisionManager - Centraliseert alle collision detection logic
"""
from constants import WALL_THICKNESS, EXIT_SIZE, GAME_WIDTH, GAME_HEIGHT, HUD_HEIGHT


class CollisionManager:
    """Beheert alle collision detection in de game"""

    def __init__(self):
        pass

    def check_obstacle_collisions(self, player, obstacles, old_x, old_y):
        """
        Check of speler botst met obstakels
        Returns: True als er een collision was
        """
        for obstacle in obstacles:
            if player.rect.colliderect(obstacle.rect):
                player.x = old_x
                player.y = old_y
                player.rect.x = old_x
                player.rect.y = old_y
                return True
        return False

    def check_pushable_block_collision(self, player, block, old_x, old_y, block_was_pushed):
        """
        Check of speler botst met een duwbaar blok
        Returns: True als er een collision was (en blok niet werd geduwd)
        """
        if block and not block_was_pushed:
            if player.rect.colliderect(block.rect):
                player.x = old_x
                player.y = old_y
                player.rect.x = old_x
                player.rect.y = old_y
                return True
        return False

    def check_sword_hits(self, player, monsters):
        """
        Check of zwaard een monster raakt
        Returns: List van monsters die geraakt werden
        """
        if not player.attacking:
            return []

        attack_rect = player.get_attack_rect()
        hit_monsters = []

        for monster in monsters:
            if monster.alive and attack_rect.colliderect(monster.rect):
                hit_monsters.append(monster)

        return hit_monsters

    def check_monster_damage(self, player, monsters):
        """
        Check of een monster de speler raakt
        Returns: (damaged, damage_amount)
        """
        for monster in monsters:
            if monster.alive and monster.can_damage:
                if player.rect.colliderect(monster.rect):
                    return (True, 1, monster)  # 1 half hart schade
        return (False, 0, None)

    def check_item_collection(self, player, items):
        """
        Check of speler een item oppakt
        Returns: List van items die gecollecteerd werden
        """
        collected_items = []
        for item in items:
            if not item.collected and player.rect.colliderect(item.rect):
                collected_items.append(item)
        return collected_items

    def check_room_transition(self, player, current_room):
        """
        Check of speler een room exit bereikt
        Returns: (should_transition, direction) of (False, None)
        """
        wall_thickness = WALL_THICKNESS
        exit_size = EXIT_SIZE

        # Bereken midden van speelveld
        center_x = GAME_WIDTH // 2
        center_y = HUD_HEIGHT + GAME_HEIGHT // 2

        # Check west exit
        if player.x < wall_thickness:
            if current_room.exits['west']:
                player_center_y = player.y + player.height // 2
                if center_y - exit_size // 2 < player_center_y < center_y + exit_size // 2:
                    if player.x < 0:
                        return (True, 'west')
                else:
                    player.x = wall_thickness
            else:
                player.x = wall_thickness

        # Check east exit
        if player.x + player.width > GAME_WIDTH - wall_thickness:
            if current_room.exits['east']:
                player_center_y = player.y + player.height // 2
                if center_y - exit_size // 2 < player_center_y < center_y + exit_size // 2:
                    if player.x + player.width > GAME_WIDTH:
                        return (True, 'east')
                else:
                    player.x = GAME_WIDTH - wall_thickness - player.width
            else:
                player.x = GAME_WIDTH - wall_thickness - player.width

        # Check north exit
        if player.y < HUD_HEIGHT + wall_thickness:
            if current_room.exits['north']:
                player_center_x = player.x + player.width // 2
                if center_x - exit_size // 2 < player_center_x < center_x + exit_size // 2:
                    if player.y < HUD_HEIGHT:
                        return (True, 'north')
                else:
                    player.y = HUD_HEIGHT + wall_thickness
            else:
                player.y = HUD_HEIGHT + wall_thickness

        # Check south exit
        if player.y + player.height > HUD_HEIGHT + GAME_HEIGHT - wall_thickness:
            if current_room.exits['south']:
                player_center_x = player.x + player.width // 2
                if center_x - exit_size // 2 < player_center_x < center_x + exit_size // 2:
                    if player.y + player.height > HUD_HEIGHT + GAME_HEIGHT:
                        return (True, 'south')
                else:
                    player.y = HUD_HEIGHT + GAME_HEIGHT - wall_thickness - player.height
            else:
                player.y = HUD_HEIGHT + GAME_HEIGHT - wall_thickness - player.height

        # Update rect
        player.rect.x = player.x
        player.rect.y = player.y

        return (False, None)

    def check_pushable_block_push(self, player, block, obstacles):
        """
        Check of speler een blok probeert te duwen
        Returns: True als blok werd geduwd
        """
        if not block:
            return False

        # Check of speler tegen het blok botst EN in de richting van het blok kijkt
        if player.rect.colliderect(block.rect):
            # Check of blok geduwd kan worden in de richting waar speler naar kijkt
            if block.can_be_pushed(player.rect, player.facing, obstacles):
                # Duw het blok
                block.push(player.facing)
                return True

        return False

    def is_within_bounds(self, x, y, width, height):
        """Check of een positie binnen de speelbare area is"""
        if (x < WALL_THICKNESS or
            x + width > GAME_WIDTH - WALL_THICKNESS or
            y < HUD_HEIGHT + WALL_THICKNESS or
            y + height > HUD_HEIGHT + GAME_HEIGHT - WALL_THICKNESS):
            return False
        return True
