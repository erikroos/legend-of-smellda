import pygame
from constants import GAME_WIDTH, GAME_HEIGHT, HUD_HEIGHT, WALL_THICKNESS

class DungeonInteractionManager:
    def __init__(self, get_item_sound=None):
        self.get_item_sound = get_item_sound

    def check_locked_door_collision(self, player, dungeon_room, old_x, old_y):
        """Check of speler tegen een locked door aan loopt"""
        locked_door_rects = dungeon_room.get_locked_door_rects(HUD_HEIGHT)

        for door_rect in locked_door_rects:
            if player.rect.colliderect(door_rect):
                # Reset speler naar oude positie
                player.x = old_x
                player.y = old_y
                player.rect.x = old_x
                player.rect.y = old_y
                return

    def check_barrier_collision(self, player, dungeon_room, old_x, old_y):
        """Check of speler tegen barrier blocks of pushable block aan loopt"""
        # Check barrier blocks
        if hasattr(dungeon_room, 'barrier_blocks'):
            for block in dungeon_room.barrier_blocks:
                if player.rect.colliderect(block):
                    # Reset speler naar oude positie
                    player.x = old_x
                    player.y = old_y
                    player.rect.x = old_x
                    player.rect.y = old_y
                    return

        # Check pushable block
        if hasattr(dungeon_room, 'pushable_block'):
            if player.rect.colliderect(dungeon_room.pushable_block.rect):
                # Check of het blok pushable is
                if hasattr(dungeon_room, 'pushable_block_pushable') and dungeon_room.pushable_block_pushable:
                    # Probeer het blok te duwen
                    can_push = dungeon_room.pushable_block.can_be_pushed(
                        player.rect, player.facing, dungeon_room.barrier_blocks if hasattr(dungeon_room, 'barrier_blocks') else []
                    )
                    if can_push:
                        dungeon_room.pushable_block.push(player.facing)
                        return

                # Als niet pushable of niet kan duwen, reset speler positie
                player.x = old_x
                player.y = old_y
                player.rect.x = old_x
                player.rect.y = old_y
                return

    def check_dungeon_key_collection(self, player, dungeon_room):
        """Check of speler de sleutel oppakt in de dungeon"""
        if dungeon_room.key and not dungeon_room.key.collected and dungeon_room.key_revealed:
            if player.rect.colliderect(dungeon_room.key.rect):
                # Collect the key
                dungeon_room.key.collect()
                player.has_key = True

                # Speel get-item geluid af
                if self.get_item_sound:
                    self.get_item_sound.play()

    def check_heart_container_collection(self, player, dungeon_room):
        """Check of speler de heart container oppakt"""
        if dungeon_room.heart_container and not dungeon_room.heart_container.collected and dungeon_room.heart_container_revealed:
            if player.rect.colliderect(dungeon_room.heart_container.rect):
                # Collect the heart container
                dungeon_room.heart_container.collect()

                # Verhoog max health met 2 (= 1 heel hartje)
                player.max_health += 2
                # Vul alle hartjes aan
                player.health = player.max_health

                # Speel get-item geluid af
                if self.get_item_sound:
                    self.get_item_sound.play()

    def check_triforce_collection(self, player, dungeon_room):
        """Check of speler de triforce oppakt"""
        if dungeon_room.triforce and not dungeon_room.triforce.collected and dungeon_room.triforce_revealed:
            if player.rect.colliderect(dungeon_room.triforce.rect):
                # Collect the triforce
                dungeon_room.triforce.collect()

                # Speel get-item geluid af
                if self.get_item_sound:
                    self.get_item_sound.play()

                return True  # Return True om aan te geven dat speler gewonnen heeft
        return False

    def check_door_unlock(self, player, dungeon_room):
        """Check of speler bij een locked door staat en deze kan unlocken"""
        if not player.has_key:
            return

        # Check alle 4 de richtingen voor locked doors
        # Noord door
        if dungeon_room.locked_exits['north']:
            north_door_rect = pygame.Rect(
                GAME_WIDTH // 2 - 50,
                HUD_HEIGHT,
                100,
                WALL_THICKNESS + 20  # Iets groter hitbox voor interactie
            )
            if player.rect.colliderect(north_door_rect):
                dungeon_room.unlock_exit('north')
                player.has_key = False  # Sleutel wordt gebruikt
                return

        # Zuid door
        if dungeon_room.locked_exits['south']:
            south_door_rect = pygame.Rect(
                GAME_WIDTH // 2 - 50,
                HUD_HEIGHT + GAME_HEIGHT - WALL_THICKNESS - 20,
                100,
                WALL_THICKNESS + 20
            )
            if player.rect.colliderect(south_door_rect):
                dungeon_room.unlock_exit('south')
                player.has_key = False
                return

        # West door
        if dungeon_room.locked_exits['west']:
            west_door_rect = pygame.Rect(
                0,
                HUD_HEIGHT + GAME_HEIGHT // 2 - 50,
                WALL_THICKNESS + 20,
                100
            )
            if player.rect.colliderect(west_door_rect):
                dungeon_room.unlock_exit('west')
                player.has_key = False
                return

        # East door
        if dungeon_room.locked_exits['east']:
            east_door_rect = pygame.Rect(
                GAME_WIDTH - WALL_THICKNESS - 20,
                HUD_HEIGHT + GAME_HEIGHT // 2 - 50,
                WALL_THICKNESS + 20,
                100
            )
            if player.rect.colliderect(east_door_rect):
                dungeon_room.unlock_exit('east')
                player.has_key = False
                return
