import pygame
import random
from world.obstacle import Obstacle
from entities.monster import Monster
from entities.archer import Archer
from items.item import Item
from items.pushable_block import PushableBlock
from world.hidden_stairs import HiddenStairs
from constants import (
    GAME_WIDTH, GAME_HEIGHT, HUD_HEIGHT, WALL_THICKNESS, EXIT_SIZE,
    WALL_COLOR, EXIT_COLOR, BACKGROUND_COLOR, TILE_SIZE,
    MIN_OBSTACLES_PER_ROOM, MAX_OBSTACLES_PER_ROOM,
    MIN_MONSTERS_PER_ROOM, MAX_MONSTERS_PER_ROOM,
    SAFE_DISTANCE_FROM_EXIT, MONSTER_WIDTH, MONSTER_HEIGHT,
    ARCHER_WIDTH, ARCHER_HEIGHT
)

class Room:
    def __init__(self, x, y, screen_width=GAME_WIDTH, screen_height=GAME_HEIGHT):
        self.grid_x = x
        self.grid_y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.exits = {'north': False, 'south': False, 'east': False, 'west': False}
        self.monsters = []
        self.archers = []
        self.walls = []
        self.obstacles = []
        self.items = []
        self.pushable_block = None
        self.hidden_stairs = None
        self.health_drops = []  # Health drops die verschijnen bij enemy deaths
        self.rupee_drops = []  # Rupee drops die verschijnen bij enemy deaths

        # Monster respawn systeem
        self.initial_monster_configs = []  # Bewaar oorspronkelijke monster posities
        self.initial_archer_configs = []  # Bewaar oorspronkelijke archer posities
        self.respawn_timer = 0  # Timer voor monster respawn
        self.respawn_delay = 180  # 3 seconden @ 60 FPS
        self.all_monsters_dead = False  # Track of alle monsters dood zijn

        self.wall_thickness = WALL_THICKNESS
        self.wall_color = WALL_COLOR
        self.exit_color = EXIT_COLOR

        # Grid systeem voor obstacle plaatsing
        self.tile_size = TILE_SIZE
        self.grid_width = (screen_width - 2 * self.wall_thickness) // self.tile_size
        self.grid_height = (screen_height - 2 * self.wall_thickness) // self.tile_size
        self.occupied_tiles = set()  # Houdt bij welke tiles bezet zijn

        # NIET hier genereren - eerst moeten exits worden ingesteld!
        # Deze worden later aangeroepen vanuit RoomManager
        
    def add_exit(self, direction):
        self.exits[direction] = True
        
    def add_monster(self, monster):
        self.monsters.append(monster)

    def is_near_exit(self, grid_x, grid_y):
        """Check of een grid positie te dichtbij een exit is"""
        center_x = self.grid_width // 2
        center_y = self.grid_height // 2
        safe_distance = SAFE_DISTANCE_FROM_EXIT

        # Check north exit (midden bovenaan)
        if self.exits['north']:
            # Breder gebied rondom exit (2 tiles breed aan elke kant)
            if grid_y < safe_distance and abs(grid_x - center_x) <= 2:
                return True

        # Check south exit (midden onderaan)
        if self.exits['south']:
            if grid_y >= self.grid_height - safe_distance and abs(grid_x - center_x) <= 2:
                return True

        # Check west exit (midden links)
        if self.exits['west']:
            if grid_x < safe_distance and abs(grid_y - center_y) <= 2:
                return True

        # Check east exit (midden rechts)
        if self.exits['east']:
            if grid_x >= self.grid_width - safe_distance and abs(grid_y - center_y) <= 2:
                return True

        return False

    def generate_obstacles(self, hud_height=HUD_HEIGHT, cave_rect=None):
        # Voeg random obstakels toe aan elke room (op grid)
        num_obstacles = random.randint(MIN_OBSTACLES_PER_ROOM, MAX_OBSTACLES_PER_ROOM)
        max_attempts = 100  # Maximaal aantal pogingen per obstakel

        for _ in range(num_obstacles):
            placed = False
            attempts = 0

            while not placed and attempts < max_attempts:
                attempts += 1

                # Kies random grid positie
                grid_x = random.randint(0, self.grid_width - 1)
                grid_y = random.randint(0, self.grid_height - 1)

                # Skip als deze tile al bezet is
                if (grid_x, grid_y) in self.occupied_tiles:
                    continue

                # Skip als deze tile te dichtbij een exit is
                if self.is_near_exit(grid_x, grid_y):
                    continue

                # Converteer grid positie naar pixel positie (met HUD offset)
                x = self.wall_thickness + (grid_x * self.tile_size)
                y = hud_height + self.wall_thickness + (grid_y * self.tile_size)

                # Skip als obstakel zou overlappen met cave entrance
                if cave_rect:
                    temp_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                    # Voeg wat extra ruimte toe rondom de cave
                    expanded_cave_rect = cave_rect.inflate(self.tile_size * 2, self.tile_size * 2)
                    if temp_rect.colliderect(expanded_cave_rect):
                        continue

                # Random type: 40% rots, 30% water, 30% boom/bosje
                rand = random.random()
                if rand < 0.4:
                    obstacle_type = 'rock'
                elif rand < 0.7:
                    obstacle_type = 'water'
                else:
                    obstacle_type = 'tree'

                # Maak obstakel met vaste tile grootte
                obstacle = Obstacle(x, y, self.tile_size, self.tile_size, obstacle_type)
                self.obstacles.append(obstacle)

                # Markeer deze tile als bezet
                self.occupied_tiles.add((grid_x, grid_y))
                placed = True

    def generate_monsters(self, hud_height=HUD_HEIGHT):
        # Special case voor starting room (1,1): maximaal 2 monsters, ver van centrum
        if self.grid_x == 1 and self.grid_y == 1:
            num_monsters = random.randint(1, 2)  # 1 of 2 monsters
        else:
            num_monsters = random.randint(MIN_MONSTERS_PER_ROOM, MAX_MONSTERS_PER_ROOM)

        max_attempts = 50

        for _ in range(num_monsters):
            placed = False
            attempts = 0

            while not placed and attempts < max_attempts:
                attempts += 1

                # Voor starting room: spawn monsters ver van het centrum
                if self.grid_x == 1 and self.grid_y == 1:
                    # Bereken centrum van het scherm
                    center_x = self.screen_width // 2
                    center_y = hud_height + self.screen_height // 2

                    # Kies een positie ver van het centrum (in de hoeken)
                    # Random hoek kiezen: 0=linksboven, 1=rechtsboven, 2=linksonder, 3=rechtsonder
                    corner = random.randint(0, 3)

                    if corner == 0:  # Linksboven
                        x = random.randint(self.wall_thickness + 50, center_x - 150)
                        y = random.randint(hud_height + self.wall_thickness + 50, center_y - 100)
                    elif corner == 1:  # Rechtsboven
                        x = random.randint(center_x + 150, self.screen_width - self.wall_thickness - 100)
                        y = random.randint(hud_height + self.wall_thickness + 50, center_y - 100)
                    elif corner == 2:  # Linksonder
                        x = random.randint(self.wall_thickness + 50, center_x - 150)
                        y = random.randint(center_y + 100, hud_height + self.screen_height - self.wall_thickness - 100)
                    else:  # Rechtsonder
                        x = random.randint(center_x + 150, self.screen_width - self.wall_thickness - 100)
                        y = random.randint(center_y + 100, hud_height + self.screen_height - self.wall_thickness - 100)
                else:
                    # Random positie binnen de speelbare ruimte (met HUD offset)
                    x = random.randint(self.wall_thickness + 50, self.screen_width - self.wall_thickness - 100)
                    y = random.randint(hud_height + self.wall_thickness + 50, hud_height + self.screen_height - self.wall_thickness - 100)

                # Maak tijdelijk rect om overlap te checken
                temp_rect = pygame.Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)

                # Check overlap met obstakels
                overlap = False
                for obstacle in self.obstacles:
                    if temp_rect.colliderect(obstacle.rect):
                        overlap = True
                        break

                # Check overlap met andere monsters
                if not overlap:
                    for monster in self.monsters:
                        padded_rect = monster.rect.inflate(40, 40)
                        if temp_rect.colliderect(padded_rect):
                            overlap = True
                            break

                # Check overlap met archers
                if not overlap:
                    for archer in self.archers:
                        padded_rect = archer.rect.inflate(40, 40)
                        if temp_rect.colliderect(padded_rect):
                            overlap = True
                            break

                if not overlap:
                    # Voor starting room (1,1): alleen normale monsters, geen archers
                    # Voor andere rooms: 30% kans op archer, 70% kans op normaal monster
                    if self.grid_x == 1 and self.grid_y == 1:
                        # Alleen normale monsters in starting room
                        monster = Monster(x, y)
                        self.monsters.append(monster)
                        # Bewaar configuratie voor respawn
                        self.initial_monster_configs.append({'x': x, 'y': y})
                    elif random.random() < 0.3:
                        archer = Archer(x, y)
                        self.archers.append(archer)
                        # Bewaar configuratie voor respawn
                        self.initial_archer_configs.append({'x': x, 'y': y})
                    else:
                        monster = Monster(x, y)
                        self.monsters.append(monster)
                        # Bewaar configuratie voor respawn
                        self.initial_monster_configs.append({'x': x, 'y': y})
                    placed = True


    def generate_secret_stairs(self, hud_height=HUD_HEIGHT):
        """Genereer verborgen trap met duwbaar blok in room (2,2)"""
        if self.grid_x == 2 and self.grid_y == 2:
            # Zoek een vrije positie voor de trap en blok
            max_attempts = 50
            for _ in range(max_attempts):
                stairs_grid_x = random.randint(2, self.grid_width - 3)
                stairs_grid_y = random.randint(2, self.grid_height - 3)

                # Check of deze positie vrij is
                if (stairs_grid_x, stairs_grid_y) not in self.occupied_tiles:
                    # Converteer naar pixel positie
                    stairs_x = self.wall_thickness + (stairs_grid_x * self.tile_size)
                    stairs_y = hud_height + self.wall_thickness + (stairs_grid_y * self.tile_size)

                    # Maak de trap
                    self.hidden_stairs = HiddenStairs(stairs_x, stairs_y, self.tile_size)

                    # Plaats het duwbare blok OP de trap
                    self.pushable_block = PushableBlock(stairs_x, stairs_y, self.tile_size)

                    # Markeer deze tile als bezet
                    self.occupied_tiles.add((stairs_grid_x, stairs_grid_y))
                    break

    def respawn_monsters(self):
        """Respawn monsters als genoeg tijd is verstreken"""
        if self.all_monsters_dead and self.respawn_timer >= self.respawn_delay:
            # Clear oude dode monsters
            self.monsters.clear()
            self.archers.clear()
            # Clear drops
            self.health_drops.clear()
            self.rupee_drops.clear()

            # Spawn nieuwe monsters op oorspronkelijke posities
            for config in self.initial_monster_configs:
                monster = Monster(config['x'], config['y'])
                self.monsters.append(monster)

            # Spawn nieuwe archers op oorspronkelijke posities
            for config in self.initial_archer_configs:
                archer = Archer(config['x'], config['y'])
                self.archers.append(archer)

            # Reset respawn tracking
            self.all_monsters_dead = False
            self.respawn_timer = 0

    def on_player_exit(self):
        """Aangeroepen wanneer de speler de room verlaat"""
        # Als alle monsters dood zijn, start respawn timer
        if self.all_monsters_dead:
            # Timer loopt al door in update()
            pass

    def on_player_enter(self):
        """Aangeroepen wanneer de speler de room binnenkomt"""
        # Check of we moeten respawnen
        self.respawn_monsters()

    def update(self, screen_width, screen_height, hud_height=HUD_HEIGHT, player=None):
        # Update alle monsters
        for monster in self.monsters:
            if monster.alive:
                monster.update(self.obstacles, screen_width, screen_height, hud_height, self.pushable_block)

        # Update alle archers (hebben player nodig om te mikken)
        if player:
            for archer in self.archers:
                if archer.alive:
                    archer.update(self.obstacles, screen_width, screen_height, hud_height, self.pushable_block, player)

        # Check of alle monsters EN archers dood zijn
        all_enemies_dead = (len(self.monsters) + len(self.archers) > 0 and
                           all(not m.alive for m in self.monsters) and
                           all(not a.alive for a in self.archers))

        if all_enemies_dead:
            if not self.all_monsters_dead:
                # Alle vijanden zijn net doodgegaan
                self.all_monsters_dead = True
                self.respawn_timer = 0

        # Update respawn timer als alle monsters dood zijn
        if self.all_monsters_dead:
            self.respawn_timer += 1

        # Update hidden stairs timer (als deze bestaat)
        if self.hidden_stairs:
            self.hidden_stairs.update()

        # Update health drops
        for health_drop in self.health_drops[:]:
            health_drop.update()
            # Verwijder drops die gecollecteerd of verlopen zijn
            if health_drop.collected:
                self.health_drops.remove(health_drop)

        # Update rupee drops
        for rupee_drop in self.rupee_drops[:]:
            rupee_drop.update()
            # Verwijder drops die gecollecteerd of verlopen zijn
            if rupee_drop.collected:
                self.rupee_drops.remove(rupee_drop)

    def render(self, screen, hud_height=HUD_HEIGHT):
        # Teken achtergrond alleen in game field gebied (onder HUD)
        game_area = pygame.Rect(0, hud_height, self.screen_width, self.screen_height)
        pygame.draw.rect(screen, BACKGROUND_COLOR, game_area)

        # Teken muren rondom het scherm (met HUD offset)

        # Bovenmuur
        if self.exits['north']:
            pygame.draw.rect(screen, self.wall_color,
                            (0, hud_height, self.screen_width // 2 - 50, self.wall_thickness))
            pygame.draw.rect(screen, self.wall_color,
                            (self.screen_width // 2 + 50, hud_height, self.screen_width // 2 - 50, self.wall_thickness))
            pygame.draw.rect(screen, self.exit_color,
                            (self.screen_width // 2 - 50, hud_height, 100, self.wall_thickness))
        else:
            pygame.draw.rect(screen, self.wall_color,
                            (0, hud_height, self.screen_width, self.wall_thickness))
        
        # Ondermuur
        if self.exits['south']:
            pygame.draw.rect(screen, self.wall_color,
                            (0, hud_height + self.screen_height - self.wall_thickness, self.screen_width // 2 - 50, self.wall_thickness))
            pygame.draw.rect(screen, self.wall_color,
                            (self.screen_width // 2 + 50, hud_height + self.screen_height - self.wall_thickness,
                             self.screen_width // 2 - 50, self.wall_thickness))
            pygame.draw.rect(screen, self.exit_color,
                            (self.screen_width // 2 - 50, hud_height + self.screen_height - self.wall_thickness, 100, self.wall_thickness))
        else:
            pygame.draw.rect(screen, self.wall_color,
                            (0, hud_height + self.screen_height - self.wall_thickness, self.screen_width, self.wall_thickness))

        # Linkermuur
        if self.exits['west']:
            pygame.draw.rect(screen, self.wall_color,
                            (0, hud_height, self.wall_thickness, self.screen_height // 2 - 50))
            pygame.draw.rect(screen, self.wall_color,
                            (0, hud_height + self.screen_height // 2 + 50, self.wall_thickness, self.screen_height // 2 - 50))
            pygame.draw.rect(screen, self.exit_color,
                            (0, hud_height + self.screen_height // 2 - 50, self.wall_thickness, 100))
        else:
            pygame.draw.rect(screen, self.wall_color,
                            (0, hud_height, self.wall_thickness, self.screen_height))

        # Rechtermuur
        if self.exits['east']:
            pygame.draw.rect(screen, self.wall_color,
                            (self.screen_width - self.wall_thickness, hud_height, self.wall_thickness, self.screen_height // 2 - 50))
            pygame.draw.rect(screen, self.wall_color,
                            (self.screen_width - self.wall_thickness, hud_height + self.screen_height // 2 + 50,
                             self.wall_thickness, self.screen_height // 2 - 50))
            pygame.draw.rect(screen, self.exit_color,
                            (self.screen_width - self.wall_thickness, hud_height + self.screen_height // 2 - 50, self.wall_thickness, 100))
        else:
            pygame.draw.rect(screen, self.wall_color,
                            (self.screen_width - self.wall_thickness, hud_height, self.wall_thickness, self.screen_height))
        
        # Render obstakels
        for obstacle in self.obstacles:
            obstacle.render(screen)

        # Render verborgen trap (als deze onthuld is)
        if self.hidden_stairs:
            self.hidden_stairs.render(screen)

        # Render duwbaar blok
        if self.pushable_block:
            self.pushable_block.render(screen)

        # Render items
        for item in self.items:
            item.render(screen)

        # Render health drops
        for health_drop in self.health_drops:
            health_drop.render(screen)

        # Render rupee drops
        for rupee_drop in self.rupee_drops:
            rupee_drop.render(screen)

        # Render monsters en archers
        for monster in self.monsters:
            monster.render(screen)

        for archer in self.archers:
            archer.render(screen)

class RoomManager:
    def __init__(self, screen_width=GAME_WIDTH, screen_height=GAME_HEIGHT, world_width=3, world_height=3, cave_entrances=None):
        self.rooms = {}
        self.current_room = (1, 1) # spawn in het middelste scherm
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        self.cave_entrances = cave_entrances or {}
        self.create_world()

    def create_world(self):
        for x in range(self.world_width):
            for y in range(self.world_height):
                room = Room(x, y, self.screen_width, self.screen_height)
                # Voeg exits toe (simpel: alle aangrenzende kamers)
                if x > 0:
                    room.add_exit('west')
                if x < self.world_width - 1:
                    room.add_exit('east')
                if y > 0:
                    room.add_exit('north')
                if y < self.world_height - 1:
                    room.add_exit('south')

                # Geef cave entrance rect door als deze room een cave heeft
                cave_rect = None
                if (x, y) in self.cave_entrances:
                    cave_entrance, _ = self.cave_entrances[(x, y)]
                    cave_rect = cave_entrance.rect

                # NU genereren we de content, nadat exits zijn ingesteld
                room.generate_obstacles(cave_rect=cave_rect)
                room.generate_monsters()
                room.generate_secret_stairs()

                self.rooms[(x, y)] = room
    
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
            return True
        return False