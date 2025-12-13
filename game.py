import pygame
import sys
import random
from entities.player import Player
from rooms.room import RoomManager
from managers.collision_manager import CollisionManager
from rooms.cave_room import CaveRoom
from rooms.hint_cave_room import HintCaveRoom
from rooms.shop_cave_room import ShopCaveRoom
from rooms.cave_entrance import CaveEntrance
from rooms.dungeon_room import DungeonManager
from managers.hud_renderer import HUDRenderer
from managers.combat_manager import CombatManager
from managers.transition_manager import TransitionManager
from managers.audio_manager import AudioManager
from managers.dungeon_interaction_manager import DungeonInteractionManager
from constants import (
    GAME_WIDTH, GAME_HEIGHT, HUD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT,
    FPS, WALL_THICKNESS, EXIT_SIZE
)

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Legend of Smellda")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialiseer player
        self.player = Player(GAME_WIDTH // 2, GAME_HEIGHT // 2 + HUD_HEIGHT)

        # Cave entrances (maak deze EERST, voordat rooms gemaakt worden)
        self.cave_entrances = {}  # Dict met (room_x, room_y) -> (entrance, exit_pos)

        # Maak sword cave entrance in starting room (1, 1)
        sword_entrance, sword_exit_pos = self.create_cave_entrance()
        self.cave_entrances[(1, 1)] = (sword_entrance, sword_exit_pos)

        # Maak hint cave entrance in room (2, 0) - noordoosten
        hint_entrance, hint_exit_pos = self.create_cave_entrance()
        self.cave_entrances[(2, 0)] = (hint_entrance, hint_exit_pos)

        # Maak shop cave entrance in room (0, 2) - linker onderhoek
        shop_entrance, shop_exit_pos = self.create_cave_entrance()
        self.cave_entrances[(0, 2)] = (shop_entrance, shop_exit_pos)

        # Maak room manager (nu met cave entrance informatie)
        self.room_manager = RoomManager(GAME_WIDTH, GAME_HEIGHT, 3, 3, self.cave_entrances)
        self.collision_manager = CollisionManager()

        # Cave system
        self.in_cave = False
        self.current_cave = None  # Track welke cave we in zijn: 'sword', 'hint', of 'shop'
        self.sword_cave_room = CaveRoom()
        self.hint_cave_room = HintCaveRoom()
        self.shop_cave_room = ShopCaveRoom()

        # Dungeon system
        self.in_dungeon = False
        self.dungeon_manager = DungeonManager(GAME_WIDTH, GAME_HEIGHT)

        # Game states
        self.game_won = False

        # Initialiseer managers
        self.audio_manager = AudioManager()
        self.hud_renderer = HUDRenderer(self.screen)
        self.combat_manager = CombatManager(self.collision_manager, self.audio_manager.hurt_sound, self.audio_manager.shield_sound)
        self.transition_manager = TransitionManager(self.collision_manager)
        self.dungeon_interaction_manager = DungeonInteractionManager(
            self.audio_manager.get_item_sound,
            self.audio_manager.get_heart_sound
        )

        # Zorg dat speler niet op een obstakel spawnt
        self.fix_player_spawn()

    def create_cave_entrance(self):
        """Maak een cave entrance langs een random rand van de starting room"""
        # Kies een random kant: 0=noord, 1=oost, 2=zuid, 3=west
        side = random.randint(0, 3)

        entrance_width = EXIT_SIZE // 2
        entrance_height = WALL_THICKNESS

        # Exit zone berekenen (gecentreerd op midden van de muur)
        # Exit is EXIT_SIZE breed, gecentreerd
        # Safe zone = exit + 100px aan beide kanten

        if side == 0:  # Noord (horizontale muur)
            center_x = GAME_WIDTH // 2
            exit_zone_start = center_x - EXIT_SIZE // 2 - 100
            exit_zone_end = center_x + EXIT_SIZE // 2 + 100

            # Kies random positie links of rechts van de exit zone
            if random.choice([True, False]):
                # Links van exit zone
                x = random.randint(WALL_THICKNESS, exit_zone_start - entrance_width)
            else:
                # Rechts van exit zone
                x = random.randint(exit_zone_end, GAME_WIDTH - WALL_THICKNESS - entrance_width)

            y = HUD_HEIGHT
            cave_exit_pos = (x + entrance_width // 2, y + entrance_height + 80)

        elif side == 1:  # Oost (verticale muur)
            center_y = HUD_HEIGHT + GAME_HEIGHT // 2
            exit_zone_start = center_y - EXIT_SIZE // 2 - 100
            exit_zone_end = center_y + EXIT_SIZE // 2 + 100

            # Kies random positie boven of onder de exit zone
            if random.choice([True, False]):
                # Boven exit zone
                y = random.randint(HUD_HEIGHT + WALL_THICKNESS, exit_zone_start - entrance_width)
            else:
                # Onder exit zone
                y = random.randint(exit_zone_end, HUD_HEIGHT + GAME_HEIGHT - WALL_THICKNESS - entrance_width)

            x = GAME_WIDTH - WALL_THICKNESS
            entrance_width, entrance_height = entrance_height, entrance_width  # Wissel voor verticaal
            cave_exit_pos = (x - 50, y + entrance_height // 2)

        elif side == 2:  # Zuid (horizontale muur)
            center_x = GAME_WIDTH // 2
            exit_zone_start = center_x - EXIT_SIZE // 2 - 100
            exit_zone_end = center_x + EXIT_SIZE // 2 + 100

            # Kies random positie links of rechts van de exit zone
            if random.choice([True, False]):
                # Links van exit zone
                x = random.randint(WALL_THICKNESS, exit_zone_start - entrance_width)
            else:
                # Rechts van exit zone
                x = random.randint(exit_zone_end, GAME_WIDTH - WALL_THICKNESS - entrance_width)

            y = HUD_HEIGHT + GAME_HEIGHT - WALL_THICKNESS
            cave_exit_pos = (x + entrance_width // 2, y - 50)

        else:  # West (verticale muur)
            center_y = HUD_HEIGHT + GAME_HEIGHT // 2
            exit_zone_start = center_y - EXIT_SIZE // 2 - 100
            exit_zone_end = center_y + EXIT_SIZE // 2 + 100

            # Kies random positie boven of onder de exit zone
            if random.choice([True, False]):
                # Boven exit zone
                y = random.randint(HUD_HEIGHT + WALL_THICKNESS, exit_zone_start - entrance_width)
            else:
                # Onder exit zone
                y = random.randint(exit_zone_end, HUD_HEIGHT + GAME_HEIGHT - WALL_THICKNESS - entrance_width)

            x = 0
            entrance_width, entrance_height = entrance_height, entrance_width  # Wissel voor verticaal
            cave_exit_pos = (x + entrance_height + 50, y + entrance_width // 2)

        return CaveEntrance(x, y, entrance_width, entrance_height), cave_exit_pos

    def fix_player_spawn(self):
        """Zorg dat de speler niet op een obstakel spawnt"""
        current_room = self.room_manager.get_current_room()

        # Check of speler op een obstakel staat
        for obstacle in current_room.obstacles:
            if self.player.rect.colliderect(obstacle.rect):
                # Zoek een veilige spawn positie
                safe_spawn_found = False

                # Probeer posities rondom het midden
                for offset_x in range(-100, 101, 50):
                    for offset_y in range(-100, 101, 50):
                        test_x = GAME_WIDTH // 2 + offset_x
                        test_y = GAME_HEIGHT // 2 + HUD_HEIGHT + offset_y

                        # Check of positie binnen bounds is
                        if not self.collision_manager.is_within_bounds(
                            test_x, test_y, self.player.width, self.player.height):
                            continue

                        # Check overlap met obstakels
                        test_rect = pygame.Rect(test_x, test_y, self.player.width, self.player.height)
                        overlap = False
                        for obs in current_room.obstacles:
                            if test_rect.colliderect(obs.rect):
                                overlap = True
                                break

                        if not overlap:
                            # Veilige positie gevonden
                            self.player.x = test_x
                            self.player.y = test_y
                            self.player.rect.x = test_x
                            self.player.rect.y = test_y
                            safe_spawn_found = True
                            break

                    if safe_spawn_found:
                        break

                return

    def cleanup(self):
        self.audio_manager.stop()
        pygame.quit()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_m:
                    self.audio_manager.toggle_mute()
                elif event.key == pygame.K_SPACE:
                    # Alleen attack als speler leeft en het spel niet gewonnen is
                    if self.player.alive and not self.game_won and self.player.attack():
                        # Speel zwaard geluid af
                        if self.audio_manager.sword_sound:
                            self.audio_manager.sword_sound.play()

    def update(self):
        # Als speler dood is of het spel gewonnen is, bevries de game (stop updates)
        if not self.player.alive or self.game_won:
            return

        # Haal keyboard state op
        keys = pygame.key.get_pressed()

        # Sla oude positie op
        old_x = self.player.x
        old_y = self.player.y

        # Update player
        self.player.update(keys)

        if self.in_dungeon:
            self.update_dungeon(old_x, old_y)
        elif self.in_cave:
            self.update_cave()
        else:
            self.update_overworld(old_x, old_y)

    def update_dungeon(self, old_x, old_y):
        """Update logic voor dungeon"""
        # Update dungeon room
        dungeon_room = self.dungeon_manager.get_current_room()
        dungeon_room.update(GAME_WIDTH, HUD_HEIGHT + GAME_HEIGHT, HUD_HEIGHT, self.player, self.audio_manager.boss_sound)

        # Check collision met locked doors
        self.dungeon_interaction_manager.check_locked_door_collision(self.player, dungeon_room, old_x, old_y)

        # Check collision met barrier blocks en pushable block
        self.dungeon_interaction_manager.check_barrier_collision(self.player, dungeon_room, old_x, old_y)

        # Check key collection
        self.dungeon_interaction_manager.check_dungeon_key_collection(self.player, dungeon_room)

        # Check heart container collection
        self.dungeon_interaction_manager.check_heart_container_collection(self.player, dungeon_room)

        # Check health drop collection
        for health_drop in dungeon_room.health_drops[:]:
            if not health_drop.collected and self.player.rect.colliderect(health_drop.rect):
                health_drop.collect()
                # Geef speler 2 HP (1 heel hartje)
                self.player.health = min(self.player.health + 2, self.player.max_health)
                # Speel get-heart geluid af
                if self.audio_manager.get_heart_sound:
                    self.audio_manager.get_heart_sound.play()

        # Check rupee drop collection
        for rupee_drop in dungeon_room.rupee_drops[:]:
            if not rupee_drop.collected and self.player.rect.colliderect(rupee_drop.rect):
                rupee_drop.collect()
                # Geef speler rupees
                self.player.rupees += rupee_drop.value
                # Speel get-rupee geluid af
                if self.audio_manager.get_rupee_sound:
                    self.audio_manager.get_rupee_sound.play()

        # Check triforce collection (win condition!)
        if self.dungeon_interaction_manager.check_triforce_collection(self.player, dungeon_room):
            self.game_won = True

        # Check door unlock interaction
        self.dungeon_interaction_manager.check_door_unlock(self.player, dungeon_room)

        # Check bat combat
        self.combat_manager.check_bat_sword_collision(self.player, dungeon_room)
        self.combat_manager.check_bat_player_collision(self.player, dungeon_room)

        # Check slime combat
        self.combat_manager.check_slime_sword_collision(self.player, dungeon_room)
        self.combat_manager.check_slime_player_collision(self.player, dungeon_room)

        # Check boss combat
        self.combat_manager.check_boss_sword_collision(self.player, dungeon_room, self.audio_manager.push_sound)
        self.combat_manager.check_boss_player_collision(self.player, dungeon_room)
        self.combat_manager.check_fireball_player_collision(self.player, dungeon_room)

        # Check of alle bats dood zijn en reveal de sleutel
        if dungeon_room.key and not dungeon_room.key_revealed:
            all_bats_dead = all(not bat.alive for bat in dungeon_room.bats)
            if all_bats_dead and len(dungeon_room.bats) > 0:
                dungeon_room.key_revealed = True
                # Speel secret geluid af
                if self.audio_manager.push_sound:
                    self.audio_manager.push_sound.play()

        # Check of alle slimes dood zijn en reveal de heart container
        if dungeon_room.heart_container and not dungeon_room.heart_container_revealed:
            all_slimes_dead = all(not slime.alive for slime in dungeon_room.slimes)
            if all_slimes_dead and len(dungeon_room.slimes) > 0:
                dungeon_room.heart_container_revealed = True
                # Speel secret geluid af
                if self.audio_manager.push_sound:
                    self.audio_manager.push_sound.play()


        # Check dungeon exit
        if self.transition_manager.check_dungeon_exit(self.player, self.dungeon_manager, self.room_manager):
            self.in_dungeon = False
            self.audio_manager.switch_to_overworld_music()

        # Check dungeon room transitions
        self.transition_manager.check_dungeon_transitions(self.player, self.dungeon_manager)

    def update_cave(self):
        """Update logic voor cave"""
        # Update juiste cave room
        if self.current_cave == 'sword':
            self.sword_cave_room.update()

            # Check sword collection (alleen in sword cave)
            if not self.sword_cave_room.sword.collected:
                if self.player.rect.colliderect(self.sword_cave_room.sword.rect):
                    self.sword_cave_room.sword.collected = True
                    self.player.has_sword = True
                    # Verberg oude man en tekst
                    self.sword_cave_room.old_man.visible = False
                    # Speel get-item geluid af
                    if self.audio_manager.get_item_sound:
                        self.audio_manager.get_item_sound.play()
        elif self.current_cave == 'hint':
            self.hint_cave_room.update()
        elif self.current_cave == 'shop':
            self.shop_cave_room.update()

            # Check heart container purchase (alleen in shop cave)
            if self.shop_cave_room.check_purchase(self.player):
                # Speel get-item geluid af
                if self.audio_manager.get_item_sound:
                    self.audio_manager.get_item_sound.play()

        # Enforce wall boundaries in cave (keep player within bounds)
        # Left wall
        if self.player.x < WALL_THICKNESS:
            self.player.x = WALL_THICKNESS
        # Right wall
        if self.player.x + self.player.width > GAME_WIDTH - WALL_THICKNESS:
            self.player.x = GAME_WIDTH - WALL_THICKNESS - self.player.width
        # Top wall
        if self.player.y < HUD_HEIGHT + WALL_THICKNESS:
            self.player.y = HUD_HEIGHT + WALL_THICKNESS
        # Bottom wall (except at exit area)
        if self.player.y + self.player.height > HUD_HEIGHT + GAME_HEIGHT - WALL_THICKNESS:
            # Check if player is in the exit area (center 50px wide)
            player_center_x = self.player.x + self.player.width // 2
            exit_left = GAME_WIDTH // 2 - 25
            exit_right = GAME_WIDTH // 2 + 25
            if not (exit_left < player_center_x < exit_right):
                # Not in exit area, block the wall
                self.player.y = HUD_HEIGHT + GAME_HEIGHT - WALL_THICKNESS - self.player.height

        # Update rect after boundary enforcement
        self.player.rect.x = self.player.x
        self.player.rect.y = self.player.y

        # Check cave exit
        exited, new_cave = self.transition_manager.check_cave_exit(
            self.player, self.cave_entrances, self.current_cave,
            lambda pos, room: self.transition_manager.find_safe_cave_exit_position(
                pos, room, self.room_manager, self.player),
            self.room_manager)

        if exited:
            self.in_cave = False
            self.current_cave = None

    def update_overworld(self, old_x, old_y):
        """Update logic voor overworld"""
        # Update current room (monsters en archers)
        current_room = self.room_manager.get_current_room()
        current_room.update(GAME_WIDTH, HUD_HEIGHT + GAME_HEIGHT, HUD_HEIGHT, self.player)

        # Check cave entrance (voor alle rooms met een cave)
        current_room_pos = self.room_manager.current_room
        if current_room_pos in self.cave_entrances:
            cave_entrance, _ = self.cave_entrances[current_room_pos]
            if self.player.rect.colliderect(cave_entrance.rect):
                self.in_cave = True
                # Bepaal welke cave dit is
                if current_room_pos == (1, 1):
                    self.current_cave = 'sword'
                elif current_room_pos == (2, 0):
                    self.current_cave = 'hint'
                elif current_room_pos == (0, 2):
                    self.current_cave = 'shop'

                # Plaats speler bij de onderkant van de cave (bij de exit)
                self.player.x = GAME_WIDTH // 2 - self.player.width // 2
                self.player.y = HUD_HEIGHT + GAME_HEIGHT - WALL_THICKNESS - self.player.height - 60
                self.player.rect.x = self.player.x
                self.player.rect.y = self.player.y
                return  # Stop verdere verwerking, we zijn nu in de cave

        # Check dungeon entrance via hidden stairs
        if current_room.hidden_stairs and current_room.hidden_stairs.can_enter():
            if self.player.rect.colliderect(current_room.hidden_stairs.rect):
                # Ga de dungeon in!
                self.in_dungeon = True
                self.audio_manager.switch_to_dungeon_music()
                # Plaats speler bij de zuid-exit van de dungeon start room
                self.player.x = GAME_WIDTH // 2 - self.player.width // 2
                self.player.y = HUD_HEIGHT + GAME_HEIGHT - WALL_THICKNESS - self.player.height - 10
                self.player.rect.x = self.player.x
                self.player.rect.y = self.player.y
                return

        # Check pushable block FIRST (before collision checks)
        block_was_pushed = self.check_pushable_block()

        # Als blok geduwd is, zet speler terug naar oude positie (blok beweegt, speler niet)
        if block_was_pushed:
            self.player.x = old_x
            self.player.y = old_y
            self.player.rect.x = old_x
            self.player.rect.y = old_y

        # Check collision met obstakels
        self.check_obstacle_collisions(old_x, old_y, block_was_pushed)

        # Check combat: zwaard raakt monsters en archers
        self.combat_manager.check_sword_hits(self.player, current_room)
        self.combat_manager.check_archer_sword_collision(self.player, current_room)

        # Check damage: monsters en archers raken speler
        self.combat_manager.check_monster_damage(self.player, current_room)
        self.combat_manager.check_archer_player_collision(self.player, current_room)

        # Check arrow collisions
        self.combat_manager.check_arrow_player_collision(self.player, current_room)
        self.combat_manager.check_arrow_obstacle_collision(current_room, GAME_WIDTH, HUD_HEIGHT + GAME_HEIGHT)

        # Check item collection
        self.check_item_collection()

        # Check screen transitions
        self.transition_manager.check_room_transitions(self.player, self.room_manager)

    def check_obstacle_collisions(self, old_x, old_y, block_was_pushed=False):
        """Check collisions met obstakels en blokken"""
        current_room = self.room_manager.get_current_room()

        # Check obstakels
        self.collision_manager.check_obstacle_collisions(
            self.player, current_room.obstacles, old_x, old_y)

        # Check duwbaar blok
        self.collision_manager.check_pushable_block_collision(
            self.player, current_room.pushable_block, old_x, old_y, block_was_pushed)

    def check_item_collection(self):
        """Check of speler items oppakt"""
        current_room = self.room_manager.get_current_room()
        collected_items = self.collision_manager.check_item_collection(
            self.player, current_room.items)

        for item in collected_items:
            item.collect()

            # Speel item-geluid af
            if self.audio_manager.get_item_sound:
                self.audio_manager.get_item_sound.play()

            # Pas effect toe gebaseerd op item type
            if item.type == 'health_potion':
                # Vul alle health aan
                self.player.health = self.player.max_health

        # Check ook health drops
        for health_drop in current_room.health_drops[:]:
            if not health_drop.collected and self.player.rect.colliderect(health_drop.rect):
                health_drop.collect()
                # Geef speler 2 HP (1 heel hartje)
                self.player.health = min(self.player.health + 2, self.player.max_health)
                # Speel get-heart geluid af
                if self.audio_manager.get_heart_sound:
                    self.audio_manager.get_heart_sound.play()

        # Check ook rupee drops
        for rupee_drop in current_room.rupee_drops[:]:
            if not rupee_drop.collected and self.player.rect.colliderect(rupee_drop.rect):
                rupee_drop.collect()
                # Geef speler rupees
                self.player.rupees += rupee_drop.value
                # Speel get-rupee geluid af
                if self.audio_manager.get_rupee_sound:
                    self.audio_manager.get_rupee_sound.play()

    def check_pushable_block(self):
        """Check of speler een duwbaar blok probeert te duwen"""
        current_room = self.room_manager.get_current_room()

        block_was_pushed = self.collision_manager.check_pushable_block_push(
            self.player, current_room.pushable_block, current_room.obstacles)

        if block_was_pushed:
            # Speel geluid af
            if self.audio_manager.push_sound:
                self.audio_manager.push_sound.play()

            # Check of blok niet meer op de trap staat - onthul de trap
            if current_room.hidden_stairs:
                if not current_room.pushable_block.rect.colliderect(current_room.hidden_stairs.rect):
                    current_room.hidden_stairs.reveal()

        return block_was_pushed

    def render_win_screen(self):
        """Render het win scherm met Link die de triforce omhoog houdt"""
        # Donkere overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        self.screen.blit(overlay, (0, 0))

        # Teken Link in het midden (iets hoger dan centrum)
        link_x = SCREEN_WIDTH // 2 - 20
        link_y = SCREEN_HEIGHT // 2 - 60

        # Link's body (tunic)
        pygame.draw.rect(self.screen, (50, 180, 50), (link_x, link_y, 40, 50))

        # Link's head
        pygame.draw.circle(self.screen, (255, 220, 177), (link_x + 20, link_y - 10), 15)

        # Link's hat
        hat_points = [
            (link_x + 20, link_y - 25),  # Top
            (link_x + 5, link_y - 5),    # Left
            (link_x + 35, link_y - 5)    # Right
        ]
        pygame.draw.polygon(self.screen, (50, 180, 50), hat_points)

        # Link's arms omhoog (handen boven hoofd)
        # Linkerarm
        pygame.draw.rect(self.screen, (255, 220, 177), (link_x - 10, link_y - 30, 10, 35))
        # Rechterarm
        pygame.draw.rect(self.screen, (255, 220, 177), (link_x + 40, link_y - 30, 10, 35))

        # Triforce boven Link's hoofd (tussen de handen)
        triforce_x = link_x + 20 - 20  # Gecentreerd boven Link
        triforce_y = link_y - 50

        # Teken triforce (3 driehoeken)
        gold = (255, 215, 0)
        dark_gold = (218, 165, 32)
        triangle_size = 15

        # Bovenste driehoek
        top_points = [
            (triforce_x + 20, triforce_y),
            (triforce_x + 20 - triangle_size, triforce_y + triangle_size),
            (triforce_x + 20 + triangle_size, triforce_y + triangle_size)
        ]
        pygame.draw.polygon(self.screen, gold, top_points)
        pygame.draw.polygon(self.screen, dark_gold, top_points, 2)

        # Linker onderste driehoek
        left_points = [
            (triforce_x + 20 - triangle_size, triforce_y + triangle_size),
            (triforce_x + 20 - 2 * triangle_size, triforce_y + 2 * triangle_size),
            (triforce_x + 20, triforce_y + 2 * triangle_size)
        ]
        pygame.draw.polygon(self.screen, gold, left_points)
        pygame.draw.polygon(self.screen, dark_gold, left_points, 2)

        # Rechter onderste driehoek
        right_points = [
            (triforce_x + 20 + triangle_size, triforce_y + triangle_size),
            (triforce_x + 20, triforce_y + 2 * triangle_size),
            (triforce_x + 20 + 2 * triangle_size, triforce_y + 2 * triangle_size)
        ]
        pygame.draw.polygon(self.screen, gold, right_points)
        pygame.draw.polygon(self.screen, dark_gold, right_points, 2)

        # Teken "YOU WON" tekst
        font = pygame.font.Font(None, 72)
        text = font.render("YOU WON", True, (255, 215, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(text, text_rect)

    def render(self):
        if self.in_dungeon:
            # Render dungeon room
            dungeon_room = self.dungeon_manager.get_current_room()
            dungeon_room.render(self.screen, HUD_HEIGHT)

            # Render player
            self.player.render(self.screen)

        elif self.in_cave:
            # Render juiste cave room
            if self.current_cave == 'sword':
                self.sword_cave_room.render(self.screen, HUD_HEIGHT)
            elif self.current_cave == 'hint':
                self.hint_cave_room.render(self.screen, HUD_HEIGHT)
            elif self.current_cave == 'shop':
                self.shop_cave_room.render(self.screen, HUD_HEIGHT)

            # Render player
            self.player.render(self.screen)
        else:
            # Render current room (met HUD offset)
            current_room = self.room_manager.get_current_room()
            current_room.render(self.screen, HUD_HEIGHT)

            # Render cave entrance (voor alle rooms met een cave)
            current_room_pos = self.room_manager.current_room
            if current_room_pos in self.cave_entrances:
                cave_entrance, _ = self.cave_entrances[current_room_pos]
                cave_entrance.render(self.screen)

            # Render player
            self.player.render(self.screen)

        # Render HUD bar bovenaan
        self.hud_renderer.render_hud(self.player, self.room_manager, self.in_dungeon, self.dungeon_manager)

        # Render game over screen als speler dood is
        self.hud_renderer.render_game_over(self.player)

        # Render win screen als speler de triforce heeft gepakt
        if self.game_won:
            self.render_win_screen()

        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
