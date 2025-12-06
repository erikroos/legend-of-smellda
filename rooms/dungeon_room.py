import pygame
import random
from items.key import Key
from items.heart_container import HeartContainer
from items.triforce import Triforce
from entities.bat import Bat
from entities.slime import Slime
from entities.boss import Boss
from world.fire import Fire
from constants import (
    GAME_WIDTH, GAME_HEIGHT, HUD_HEIGHT, WALL_THICKNESS, EXIT_SIZE,
    DUNGEON_WALL_COLOR, DUNGEON_DOOR_COLOR, DUNGEON_BACKGROUND_COLOR,
    DUNGEON_LOCKED_DOOR_COLOR, DUNGEON_LOCK_COLOR, DUNGEON_LOCK_BORDER_COLOR,
    DUNGEON_KEYHOLE_COLOR, DUNGEON_FLOOR_TILE_COLOR, TILE_SIZE
)

class DungeonRoom:
    def __init__(self, x, y, screen_width=GAME_WIDTH, screen_height=GAME_HEIGHT):
        self.grid_x = x
        self.grid_y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.exits = {'north': False, 'south': False, 'east': False, 'west': False}
        self.locked_exits = {'north': False, 'south': False, 'east': False, 'west': False}
        self.monsters = []
        self.obstacles = []
        self.bats = []  # Vleermuizen in deze kamer
        self.slimes = []  # Slimes in deze kamer
        self.boss = None  # Boss in deze kamer
        self.key = None
        self.key_revealed = False  # Track of key is verschenen
        self.heart_container = None  # Heart container
        self.heart_container_revealed = False  # Track of heart container is verschenen
        self.triforce = None  # Triforce (win condition)
        self.triforce_revealed = False  # Track of triforce is verschenen
        self.fires = []  # Decoratieve vuren
        self.floor_tiles = []  # Decoratieve vloertegels
        self.health_drops = []  # Health drops die verschijnen bij enemy deaths

        self.wall_thickness = WALL_THICKNESS
        self.wall_color = DUNGEON_WALL_COLOR
        self.door_color = DUNGEON_DOOR_COLOR
        self.background_color = DUNGEON_BACKGROUND_COLOR
        self.locked_door_color = DUNGEON_LOCKED_DOOR_COLOR
        self.lock_color = DUNGEON_LOCK_COLOR
        self.keyhole_color = DUNGEON_KEYHOLE_COLOR

    def add_exit(self, direction, locked=False):
        self.exits[direction] = True
        self.locked_exits[direction] = locked

    def unlock_exit(self, direction):
        """Unlock een exit"""
        if direction in self.locked_exits:
            self.locked_exits[direction] = False

    def get_locked_door_rects(self, hud_height=HUD_HEIGHT):
        """Return collision rects voor alle locked doors"""
        locked_rects = []

        # Noord deur
        if self.locked_exits['north']:
            locked_rects.append(pygame.Rect(
                self.screen_width // 2 - 50,
                hud_height,
                100,
                self.wall_thickness
            ))

        # Zuid deur
        if self.locked_exits['south']:
            locked_rects.append(pygame.Rect(
                self.screen_width // 2 - 50,
                hud_height + self.screen_height - self.wall_thickness,
                100,
                self.wall_thickness
            ))

        # West deur
        if self.locked_exits['west']:
            locked_rects.append(pygame.Rect(
                0,
                hud_height + self.screen_height // 2 - 50,
                self.wall_thickness,
                100
            ))

        # Oost deur
        if self.locked_exits['east']:
            locked_rects.append(pygame.Rect(
                self.screen_width - self.wall_thickness,
                hud_height + self.screen_height // 2 - 50,
                self.wall_thickness,
                100
            ))

        return locked_rects

    def draw_lock(self, screen, x, y, size, direction):
        """Teken een slot-icoon op een locked door"""
        # Bepaal centrum positie gebaseerd op richting
        if direction in ['north', 'south']:
            # Horizontale deur
            center_x = x + size // 2
            center_y = y + self.wall_thickness // 2
        else:
            # Verticale deur
            center_x = x + self.wall_thickness // 2
            center_y = y + size // 2

        lock_size = 16

        # Teken het slot lichaam (rechthoek)
        lock_body = pygame.Rect(
            center_x - lock_size // 2,
            center_y - lock_size // 4,
            lock_size,
            lock_size // 2 + 4
        )
        pygame.draw.rect(screen, self.lock_color, lock_body)
        pygame.draw.rect(screen, DUNGEON_LOCK_BORDER_COLOR, lock_body, 2)  # Rand

        # Teken de beugel bovenaan (halve cirkel)
        beugel_rect = pygame.Rect(
            center_x - lock_size // 3,
            center_y - lock_size // 2,
            lock_size // 3 * 2,
            lock_size // 2
        )
        pygame.draw.arc(screen, self.lock_color, beugel_rect, 0, 3.14159, 4)

        # Teken sleutelgat
        keyhole_rect = pygame.Rect(
            center_x - 3,
            center_y - 2,
            6,
            8
        )
        pygame.draw.rect(screen, self.keyhole_color, keyhole_rect)

    def add_bats(self, num_bats, hud_height=HUD_HEIGHT):
        """Voeg vleermuizen toe aan deze kamer"""
        for _ in range(num_bats):
            # Random positie binnen de kamer
            x = random.randint(
                self.wall_thickness + 50,
                self.screen_width - self.wall_thickness - 75
            )
            y = random.randint(
                hud_height + self.wall_thickness + 50,
                hud_height + self.screen_height - self.wall_thickness - 70
            )
            bat = Bat(x, y)
            self.bats.append(bat)

    def add_slimes(self, num_slimes, hud_height=HUD_HEIGHT):
        """Voeg slimes toe aan deze kamer (grote slimes)"""
        for _ in range(num_slimes):
            # Random positie binnen de kamer
            x = random.randint(
                self.wall_thickness + 50,
                self.screen_width - self.wall_thickness - 75
            )
            y = random.randint(
                hud_height + self.wall_thickness + 50,
                hud_height + self.screen_height - self.wall_thickness - 70
            )
            slime = Slime(x, y, is_large=True)
            self.slimes.append(slime)

    def update(self, screen_width, screen_height, hud_height=HUD_HEIGHT, player=None, boss_sound=None):
        # Update vleermuizen
        for bat in self.bats:
            if bat.alive:
                bat.update([], screen_width, screen_height, hud_height)

        # Update slimes
        for slime in self.slimes:
            if slime.alive:
                slime.update([], screen_width, screen_height, hud_height)

        # Update boss
        if self.boss and self.boss.alive and player:
            self.boss.update(player, hud_height, screen_width, screen_height, boss_sound)

        # Update vuren
        for fire in self.fires:
            fire.update()

        # Update heart container
        if self.heart_container and not self.heart_container.collected:
            self.heart_container.update()

        # Update triforce
        if self.triforce and not self.triforce.collected:
            self.triforce.update()

        # Update health drops
        for health_drop in self.health_drops[:]:
            health_drop.update()
            # Verwijder drops die gecollecteerd of verlopen zijn
            if health_drop.collected:
                self.health_drops.remove(health_drop)

    def render(self, screen, hud_height=HUD_HEIGHT):
        # Teken donkere achtergrond (ondergronds gevoel)
        game_area = pygame.Rect(0, hud_height, self.screen_width, self.screen_height)
        pygame.draw.rect(screen, self.background_color, game_area)

        # Teken decoratieve vloertegels
        for tile_rect in self.floor_tiles:
            pygame.draw.rect(screen, DUNGEON_FLOOR_TILE_COLOR, tile_rect)

        # Teken muren rondom het scherm

        # Bovenmuur
        if self.exits['north']:
            # Muur met deur/exit in het midden
            pygame.draw.rect(screen, self.wall_color,
                            (0, hud_height, self.screen_width // 2 - 50, self.wall_thickness))
            pygame.draw.rect(screen, self.wall_color,
                            (self.screen_width // 2 + 50, hud_height, self.screen_width // 2 - 50, self.wall_thickness))
            # Deur kleur: bruin als locked, zwart als unlocked
            door_color = self.locked_door_color if self.locked_exits['north'] else self.door_color
            door_x = self.screen_width // 2 - 50
            pygame.draw.rect(screen, door_color,
                            (door_x, hud_height, 100, self.wall_thickness))
            # Teken slot als deur locked is
            if self.locked_exits['north']:
                self.draw_lock(screen, door_x, hud_height, 100, 'north')
        else:
            pygame.draw.rect(screen, self.wall_color,
                            (0, hud_height, self.screen_width, self.wall_thickness))

        # Ondermuur
        if self.exits['south']:
            pygame.draw.rect(screen, self.wall_color,
                            (0, hud_height + self.screen_height - self.wall_thickness,
                             self.screen_width // 2 - 50, self.wall_thickness))
            pygame.draw.rect(screen, self.wall_color,
                            (self.screen_width // 2 + 50, hud_height + self.screen_height - self.wall_thickness,
                             self.screen_width // 2 - 50, self.wall_thickness))
            door_color = self.locked_door_color if self.locked_exits['south'] else self.door_color
            door_x = self.screen_width // 2 - 50
            door_y = hud_height + self.screen_height - self.wall_thickness
            pygame.draw.rect(screen, door_color, (door_x, door_y, 100, self.wall_thickness))
            if self.locked_exits['south']:
                self.draw_lock(screen, door_x, door_y, 100, 'south')
        else:
            pygame.draw.rect(screen, self.wall_color,
                            (0, hud_height + self.screen_height - self.wall_thickness,
                             self.screen_width, self.wall_thickness))

        # Linkermuur
        if self.exits['west']:
            pygame.draw.rect(screen, self.wall_color,
                            (0, hud_height, self.wall_thickness, self.screen_height // 2 - 50))
            pygame.draw.rect(screen, self.wall_color,
                            (0, hud_height + self.screen_height // 2 + 50,
                             self.wall_thickness, self.screen_height // 2 - 50))
            door_color = self.locked_door_color if self.locked_exits['west'] else self.door_color
            door_y = hud_height + self.screen_height // 2 - 50
            pygame.draw.rect(screen, door_color, (0, door_y, self.wall_thickness, 100))
            if self.locked_exits['west']:
                self.draw_lock(screen, 0, door_y, 100, 'west')
        else:
            pygame.draw.rect(screen, self.wall_color,
                            (0, hud_height, self.wall_thickness, self.screen_height))

        # Rechtermuur
        if self.exits['east']:
            pygame.draw.rect(screen, self.wall_color,
                            (self.screen_width - self.wall_thickness, hud_height,
                             self.wall_thickness, self.screen_height // 2 - 50))
            pygame.draw.rect(screen, self.wall_color,
                            (self.screen_width - self.wall_thickness, hud_height + self.screen_height // 2 + 50,
                             self.wall_thickness, self.screen_height // 2 - 50))
            door_color = self.locked_door_color if self.locked_exits['east'] else self.door_color
            door_x = self.screen_width - self.wall_thickness
            door_y = hud_height + self.screen_height // 2 - 50
            pygame.draw.rect(screen, door_color, (door_x, door_y, self.wall_thickness, 100))
            if self.locked_exits['east']:
                self.draw_lock(screen, door_x, door_y, 100, 'east')
        else:
            pygame.draw.rect(screen, self.wall_color,
                            (self.screen_width - self.wall_thickness, hud_height,
                             self.wall_thickness, self.screen_height))

        # Render barrier blocks (donkerblauwe blokken)
        if hasattr(self, 'barrier_blocks'):
            for block in self.barrier_blocks:
                pygame.draw.rect(screen, DUNGEON_WALL_COLOR, block)

        # Render pushable block (als deze bestaat)
        if hasattr(self, 'pushable_block'):
            self.pushable_block.render(screen)

        # Render vuren
        for fire in self.fires:
            fire.render(screen)

        # Render slimes
        for slime in self.slimes:
            if slime.alive:
                slime.render(screen)

        # Render vleermuizen
        for bat in self.bats:
            if bat.alive:
                bat.render(screen)

        # Render boss
        if self.boss and self.boss.alive:
            self.boss.render(screen)

        # Render sleutel (als deze bestaat en niet collected is)
        if self.key and not self.key.collected and self.key_revealed:
            self.key.render(screen)

        # Render heart container (als deze bestaat en niet collected is)
        if self.heart_container and not self.heart_container.collected and self.heart_container_revealed:
            self.heart_container.render(screen)

        # Render triforce (als deze bestaat en niet collected is)
        if self.triforce and not self.triforce.collected and self.triforce_revealed:
            self.triforce.render(screen)

        # Render health drops
        for health_drop in self.health_drops:
            health_drop.render(screen)

class DungeonManager:
    def __init__(self, screen_width=GAME_WIDTH, screen_height=GAME_HEIGHT):
        self.rooms = {}
        self.current_room = (0, 0)  # Start room van dungeon
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visited_rooms = set()
        self.create_dungeon()

    def create_dungeon(self):
        # Dungeon layout (kruisvorm):
        #     [N] (0, -1)
        #      |
        # [W]-[M]-[E]  (-1,0) (0,0) (1,0)
        #      |
        #     [S] (0, 1) - start room

        # Start room (0, 1) - zuidelijk, entry point vanuit overworld
        start_room = DungeonRoom(0, 1, self.screen_width, self.screen_height)
        start_room.add_exit('south')  # Exit naar overworld
        start_room.add_exit('north')  # Exit naar center room

        # Voeg decoratieve vuren toe bij de ingang (zuidelijke deur)
        south_door_x = self.screen_width // 2
        fire_offset = 60  # Afstand van deur
        fire1_x = south_door_x - fire_offset
        fire2_x = south_door_x + fire_offset - 20
        fire_y = HUD_HEIGHT + self.screen_height - WALL_THICKNESS - 60
        start_room.fires.append(Fire(fire1_x, fire_y))
        start_room.fires.append(Fire(fire2_x, fire_y))

        # Voeg decoratieve vloertegels toe in groepjes
        tile_size = 32
        wall_margin = 80  # Afstand van de muur

        # Linksboven - 2x2 tegel patroon
        for i in range(2):
            for j in range(2):
                tile_x = wall_margin + (i * tile_size * 2)
                tile_y = HUD_HEIGHT + wall_margin + (j * tile_size * 2)
                start_room.floor_tiles.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))

        # Rechtsboven - 2x2 tegel patroon
        for i in range(2):
            for j in range(2):
                tile_x = self.screen_width - wall_margin - tile_size - (i * tile_size * 2)
                tile_y = HUD_HEIGHT + wall_margin + (j * tile_size * 2)
                start_room.floor_tiles.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))

        # Midden van de kamer - 2x2 tegel patroon (exact gecentreerd)
        # Totale breedte van het patroon is 3*tile_size (2 tegels breed met spacing)
        pattern_width = tile_size * 3
        pattern_height = tile_size * 3
        center_x = (self.screen_width - pattern_width) // 2
        center_y = HUD_HEIGHT + (self.screen_height - pattern_height) // 2
        for i in range(2):
            for j in range(2):
                tile_x = center_x + (i * tile_size * 2)
                tile_y = center_y + (j * tile_size * 2)
                start_room.floor_tiles.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))

        # Linksonder - 2x2 tegel patroon
        for i in range(2):
            for j in range(2):
                tile_x = wall_margin + (i * tile_size * 2)
                tile_y = self.screen_height - wall_margin - tile_size + (j * tile_size * 2)
                start_room.floor_tiles.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))

        # Rechtsonder - 2x2 tegel patroon
        for i in range(2):
            for j in range(2):
                tile_x = self.screen_width - wall_margin - tile_size - (i * tile_size * 2)
                tile_y = self.screen_height - wall_margin - tile_size + (j * tile_size * 2)
                start_room.floor_tiles.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))

        self.rooms[(0, 1)] = start_room

        # Center room (0, 0) - 4 exits naar alle kanten, MET VLEERMUIZEN
        center_room = DungeonRoom(0, 0, self.screen_width, self.screen_height)
        center_room.add_exit('north', locked=True)  # Locked door naar north!
        center_room.add_exit('south')
        center_room.add_exit('east')
        center_room.add_exit('west')
        center_room.add_bats(2)  # vleermuizen in center room
        self.rooms[(0, 0)] = center_room

        # North room (0, -1) - Boss room met afgeschermd gedeelte
        north_room = DungeonRoom(0, -1, self.screen_width, self.screen_height)
        north_room.add_exit('south')

        # Voeg boss toe (draak in rechter bovenste gedeelte)
        boss_x = self.screen_width - WALL_THICKNESS - 200  # Rechts boven
        boss_y = HUD_HEIGHT + WALL_THICKNESS + 50
        north_room.boss = Boss(boss_x, boss_y)

        # Voeg donkerblauwe blokken toe voor afgeschermd gedeelte in noordwestelijke hoek
        # Maak een L-vormig patroon met een gat
        block_size = TILE_SIZE
        north_room.barrier_blocks = []  # Nieuwe lijst voor barriers

        # Start posities
        start_x = WALL_THICKNESS
        start_y = HUD_HEIGHT + WALL_THICKNESS

        # Bovenmuur barriers (van links naar rechts) - 5 blokken
        for i in range(5):
            if i == 1:
                continue # Sla het tweede blok over om een gat te creëren
            block_x = start_x + (i * block_size)
            block_y = start_y + (4 * block_size)
            north_room.barrier_blocks.append(pygame.Rect(block_x, block_y, block_size, block_size))

        # Linker muur barriers (van boven naar beneden) - 4 blokken
        for i in range(0, 4):
            block_x = start_x + (4 * block_size)
            block_y = start_y + (i * block_size)
            north_room.barrier_blocks.append(pygame.Rect(block_x, block_y, block_size, block_size))

        # GAT in de barriers: op positie (start_x + block_size, start_y + 4*block_size)
        # Dit is één grid positie naast de linker muur

        # Voeg pushable block toe dat het gat blokkeert (1 grid positie boven het gat)
        from items.pushable_block import PushableBlock
        pushable_x = start_x + block_size
        pushable_y = start_y + 3 * block_size  # 1 positie boven het gat
        north_room.pushable_block = PushableBlock(pushable_x, pushable_y, block_size)
        north_room.pushable_block.color = DUNGEON_WALL_COLOR  # Donkerblauw zoals muren
        north_room.pushable_block_pushable = False  # Kan nog niet geduwd worden

        # Voeg triforce toe in het afgeschermde gedeelte (gecentreerd, meer noordelijk)
        triforce_x = start_x + block_size * 2 - 20  # Gecentreerd in het afgeschermde gebied
        triforce_y = start_y + block_size * 1 - 10  # Meer noordelijk
        north_room.triforce = Triforce(triforce_x, triforce_y)
        north_room.triforce_revealed = True  # Triforce is altijd zichtbaar

        self.rooms[(0, -1)] = north_room

        # East room (1, 0) - alleen exit naar center, MET SLEUTEL EN VLEERMUIZEN
        east_room = DungeonRoom(1, 0, self.screen_width, self.screen_height)
        east_room.add_exit('west')
        # Plaats sleutel in het midden van de kamer
        east_room.key = Key(
            self.screen_width // 2 - 15,
            HUD_HEIGHT + self.screen_height // 2 - 15
        )
        east_room.add_bats(3)  # vleermuizen in east room - moet eerst verslaan!
        self.rooms[(1, 0)] = east_room

        # West room (-1, 0) - alleen exit naar center, MET SLIMES
        west_room = DungeonRoom(-1, 0, self.screen_width, self.screen_height)
        west_room.add_exit('east')
        west_room.add_slimes(3)  # slimes in west room - splitsen in kleine slimes!
        # Plaats heart container in het midden van de kamer
        west_room.heart_container = HeartContainer(
            self.screen_width // 2 - 15,
            HUD_HEIGHT + self.screen_height // 2 - 15
        )
        self.rooms[(-1, 0)] = west_room

        # Start in de start room
        self.current_room = (0, 1)
        self.visited_rooms.add((0, 1))

    def get_current_room(self):
        return self.rooms[self.current_room]

    def change_room(self, direction):
        x, y = self.current_room
        if direction == 'north':
            y -= 1
        elif direction == 'south':
            y += 1
        elif direction == 'east':
            x += 1
        elif direction == 'west':
            x -= 1

        if (x, y) in self.rooms:
            self.current_room = (x, y)
            self.visited_rooms.add((x, y))
            return True
        return False
