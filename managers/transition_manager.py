import pygame
from constants import GAME_WIDTH, GAME_HEIGHT, HUD_HEIGHT, WALL_THICKNESS

class TransitionManager:
    def __init__(self, collision_manager):
        self.collision_manager = collision_manager

    def check_cave_exit(self, player, cave_entrances, current_cave, find_safe_position_callback):
        """Check of speler de grot verlaat"""
        # Exit is onderaan in het midden
        exit_rect = pygame.Rect(
            GAME_WIDTH // 2 - 25,
            HUD_HEIGHT + GAME_HEIGHT - WALL_THICKNESS,
            50,
            WALL_THICKNESS
        )

        if player.rect.colliderect(exit_rect):
            # Bepaal welke room we naar terug moeten
            if current_cave == 'sword':
                exit_room_pos = (1, 1)
            elif current_cave == 'hint':
                exit_room_pos = (2, 0)
            else:
                return False, None  # Geen geldige cave

            # Haal exit positie op en vind veilige spawn positie
            if exit_room_pos in cave_entrances:
                _, cave_exit_pos = cave_entrances[exit_room_pos]

                # Zoek veilige positie rondom de exit
                safe_pos = find_safe_position_callback(cave_exit_pos, exit_room_pos)

                player.x = safe_pos[0] - player.width // 2
                player.y = safe_pos[1] - player.height // 2
                player.rect.x = player.x
                player.rect.y = player.y

            return True, None  # Exited cave

        return False, current_cave  # Still in cave

    def check_dungeon_exit(self, player, dungeon_manager, room_manager):
        """Check of speler de dungeon verlaat via zuid-exit"""
        dungeon_room = dungeon_manager.get_current_room()

        # Check zuid-exit (terug naar overworld) - ALLEEN in de start room (0, 1)
        if dungeon_manager.current_room == (0, 1) and dungeon_room.exits['south']:
            exit_rect = pygame.Rect(
                GAME_WIDTH // 2 - 50,
                HUD_HEIGHT + GAME_HEIGHT - WALL_THICKNESS,
                100,
                WALL_THICKNESS
            )

            if player.rect.colliderect(exit_rect):
                # Verlaat dungeon en ga terug naar overworld room (2,2)
                room_manager.current_room = (2, 2)

                # Plaats speler op een veilige plek bij de hidden stairs
                current_room = room_manager.get_current_room()
                if current_room.hidden_stairs:
                    stairs_x = current_room.hidden_stairs.x
                    stairs_y = current_room.hidden_stairs.y

                    # Check of het blok onder de trap staat (originele positie)
                    block_below = False
                    if current_room.pushable_block:
                        block_x = current_room.pushable_block.x
                        block_y = current_room.pushable_block.y
                        # Blok staat onder de trap als het binnen ~60 pixels onder de trap is
                        if abs(block_x - stairs_x) < 10 and block_y > stairs_y and block_y - stairs_y < 70:
                            block_below = True

                    # Plaats speler boven of onder de trap, afhankelijk van waar het blok staat
                    player.x = stairs_x + (current_room.hidden_stairs.size // 2) - (player.width // 2)
                    if block_below:
                        # Blok staat onder de trap, plaats speler boven de trap
                        player.y = stairs_y - player.height - 10
                    else:
                        # Blok staat niet onder de trap (of is geduwd), plaats speler onder de trap
                        player.y = stairs_y + current_room.hidden_stairs.size + 10

                    player.rect.x = player.x
                    player.rect.y = player.y

                return True  # Exited dungeon

        return False  # Still in dungeon

    def check_dungeon_transitions(self, player, dungeon_manager):
        """Check of speler naar een andere dungeon room gaat"""
        dungeon_room = dungeon_manager.get_current_room()
        should_transition, direction = self.collision_manager.check_room_transition(
            player, dungeon_room)

        if should_transition:
            # Check of deze exit locked is
            if dungeon_room.locked_exits[direction]:
                # Door is locked - push player terug
                if direction == 'north':
                    player.y = HUD_HEIGHT + WALL_THICKNESS + 5
                elif direction == 'south':
                    player.y = HUD_HEIGHT + GAME_HEIGHT - player.height - WALL_THICKNESS - 5
                elif direction == 'west':
                    player.x = WALL_THICKNESS + 5
                elif direction == 'east':
                    player.x = GAME_WIDTH - player.width - WALL_THICKNESS - 5
                player.rect.x = player.x
                player.rect.y = player.y
                return

            # Probeer naar nieuwe dungeon room te gaan
            if dungeon_manager.change_room(direction):
                # Succesvolle transition - plaats speler aan andere kant
                if direction == 'north':
                    player.y = HUD_HEIGHT + GAME_HEIGHT - player.height - WALL_THICKNESS
                elif direction == 'west':
                    player.x = GAME_WIDTH - player.width - WALL_THICKNESS
                elif direction == 'east':
                    player.x = WALL_THICKNESS
                elif direction == 'south':
                    player.y = HUD_HEIGHT + WALL_THICKNESS

                player.rect.x = player.x
                player.rect.y = player.y

    def check_room_transitions(self, player, room_manager):
        """Check of speler naar een andere overworld room gaat"""
        current_room = room_manager.get_current_room()
        should_transition, direction = self.collision_manager.check_room_transition(
            player, current_room)

        if should_transition:
            room_manager.change_room(direction)

            # Zet speler op nieuwe positie na room transition
            if direction == 'west':
                player.x = GAME_WIDTH - player.width - WALL_THICKNESS
            elif direction == 'east':
                player.x = WALL_THICKNESS
            elif direction == 'north':
                player.y = HUD_HEIGHT + GAME_HEIGHT - player.height - WALL_THICKNESS
            elif direction == 'south':
                player.y = HUD_HEIGHT + WALL_THICKNESS

            player.rect.x = player.x
            player.rect.y = player.y

    def find_safe_cave_exit_position(self, preferred_pos, room_pos, room_manager, player):
        """Vind een veilige positie rondom de cave exit zonder obstakels"""
        # Haal de room op
        room_manager.current_room = room_pos
        current_room = room_manager.get_current_room()

        # Test posities in een cirkel rondom de voorkeurspositie
        test_radius_list = [0, 60, 80, 100, 120]  # Probeer steeds verder weg

        for radius in test_radius_list:
            if radius == 0:
                # Test de voorkeurspositie zelf
                test_positions = [preferred_pos]
            else:
                # Test 8 posities rondom de voorkeurspositie
                test_positions = [
                    (preferred_pos[0], preferred_pos[1] - radius),  # Noord
                    (preferred_pos[0] + radius, preferred_pos[1]),  # Oost
                    (preferred_pos[0], preferred_pos[1] + radius),  # Zuid
                    (preferred_pos[0] - radius, preferred_pos[1]),  # West
                    (preferred_pos[0] + radius*0.7, preferred_pos[1] - radius*0.7),  # NO
                    (preferred_pos[0] + radius*0.7, preferred_pos[1] + radius*0.7),  # ZO
                    (preferred_pos[0] - radius*0.7, preferred_pos[1] + radius*0.7),  # ZW
                    (preferred_pos[0] - radius*0.7, preferred_pos[1] - radius*0.7),  # NW
                ]

            for test_pos in test_positions:
                test_x = int(test_pos[0])
                test_y = int(test_pos[1])

                # Check of positie binnen bounds is
                if not self.collision_manager.is_within_bounds(
                    test_x, test_y, player.width, player.height):
                    continue

                # Check of er geen obstakels zijn
                test_rect = pygame.Rect(test_x - player.width // 2,
                                       test_y - player.height // 2,
                                       player.width, player.height)

                has_collision = False
                for obstacle in current_room.obstacles:
                    if test_rect.colliderect(obstacle.rect):
                        has_collision = True
                        break

                # Check pushable block
                if not has_collision and current_room.pushable_block:
                    if test_rect.colliderect(current_room.pushable_block.rect):
                        has_collision = True

                if not has_collision:
                    # Veilige positie gevonden!
                    return (test_x, test_y)

        # Als geen veilige positie gevonden, return voorkeurspositie
        return preferred_pos
