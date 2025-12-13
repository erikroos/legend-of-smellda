"""
Game constants - alle magic numbers op één plek
"""

# Screen en layout dimensies
GAME_WIDTH = 800
GAME_HEIGHT = 600
HUD_HEIGHT = 60
SCREEN_WIDTH = GAME_WIDTH
SCREEN_HEIGHT = GAME_HEIGHT + HUD_HEIGHT

# Grid en tile systeem
TILE_SIZE = 50
WALL_THICKNESS = 40
EXIT_SIZE = 100

# FPS
FPS = 60

# Player settings
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_SPEED = 3
PLAYER_MAX_HEALTH = 6
PLAYER_ATTACK_COOLDOWN = 30
PLAYER_INVINCIBILITY_FRAMES = 90
SWORD_LENGTH = 40
SWORD_WIDTH = 40
SWORD_WIDTH_RENDER = 10
HALF_PLAYER_WIDTH_MINUS_SWORD = PLAYER_WIDTH // 2 - SWORD_WIDTH_RENDER // 2

# Monster settings
MONSTER_WIDTH = 30
MONSTER_HEIGHT = 30
MONSTER_SPEED = 1.5
MONSTER_HEALTH = 2
MONSTER_DIRECTION_CHANGE_INTERVAL = 120
MONSTER_DAMAGE_COOLDOWN = 60

# Item settings
ITEM_WIDTH = 30
ITEM_HEIGHT = 30

# Room generation
MIN_OBSTACLES_PER_ROOM = 5
MAX_OBSTACLES_PER_ROOM = 8
MIN_MONSTERS_PER_ROOM = 2
MAX_MONSTERS_PER_ROOM = 4
SAFE_DISTANCE_FROM_EXIT = 3

# World settings
WORLD_WIDTH = 3
WORLD_HEIGHT = 3
SPAWN_ROOM = (1, 1)

# Kleuren
WALL_COLOR = (100, 70, 50)
EXIT_COLOR = (240, 235, 230) #(0, 0, 0) voor zwarte exits
CAVE_EXIT_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (240, 235, 230)
HUD_BG_COLOR = (40, 40, 40)
HUD_BORDER_COLOR = (80, 80, 80)

# Player kleuren
TUNIC_COLOR = (50, 180, 50)
SKIN_COLOR = (255, 220, 177)
HAIR_COLOR = (150, 100, 50)
BELT_COLOR = (139, 69, 19)
SWORD_BLADE_COLOR = (192, 192, 192)
SWORD_HANDLE_COLOR = (218, 165, 32)
SHIELD_COLOR = (101, 67, 33)  # Bruin voor schild
SHIELD_EDGE_COLOR = (70, 45, 20)  # Donkerder bruin voor rand

# Monster kleuren
MONSTER_BODY_COLOR = (150, 50, 50)
MONSTER_EYE_COLOR = (255, 255, 255)
MONSTER_PUPIL_COLOR = (0, 0, 0)

# Obstacle kleuren
ROCK_COLOR = (100, 70, 50)
WATER_COLOR = (50, 100, 200)
TREE_COLOR = (34, 139, 34)  # Forest green voor bomen/bosjes

# Item kleuren
HEALTH_POTION_COLOR = (255, 50, 100)
HEALTH_POTION_ACCENT = (255, 150, 180)
POTION_CAP_COLOR = (100, 50, 50)

# Pushable block kleuren
BLOCK_COLOR = (139, 90, 43)
BLOCK_LINE_COLOR = (120, 80, 50)

# Hidden stairs kleuren
STAIRS_DARK_COLOR = (50, 50, 50)
STAIRS_STEP_COLOR = (80, 70, 60)

# Minimap settings
MINIMAP_ROOM_SIZE = 12
MINIMAP_ROOM_SPACING = 2
MINIMAP_START_X = 15
MINIMAP_VISITED_ROOM_COLOR = (100, 100, 100)
MINIMAP_CURRENT_ROOM_COLOR = (255, 255, 255)

# Heart rendering
HEART_SIZE = 20
HEART_SPACING = 25
HEART_FULL_COLOR = (220, 20, 60)
HEART_EMPTY_COLOR = (100, 100, 100)
HEART_CONTAINER_OUTLINE_COLOR = (255, 255, 255)  # Wit voor outline

# Dungeon kleuren
DUNGEON_BACKGROUND_COLOR = (25, 35, 55)  # Donkerblauw
DUNGEON_WALL_COLOR = (40, 60, 90)  # Lichtere donkerblauwe tint
DUNGEON_DOOR_COLOR = (0, 0, 0)  # Zwarte deuren/exits
DUNGEON_LOCKED_DOOR_COLOR = (101, 67, 33)  # Bruin voor locked doors
DUNGEON_LOCK_COLOR = (50, 50, 50)  # Donkergrijs voor het slot
DUNGEON_LOCK_BORDER_COLOR = (70, 70, 70)  # Lichtgrijs voor slot rand
DUNGEON_KEYHOLE_COLOR = (30, 30, 30)  # Zwart voor sleutelgat
DUNGEON_FLOOR_TILE_COLOR = (35, 50, 75)  # Lichtere blauwe tint voor vloertegels

# Bat kleuren
BAT_BODY_COLOR = (5, 5, 5)  # Pikzwart
BAT_WING_COLOR = (10, 10, 10)  # Bijna zwart voor vleugels
BAT_EYE_COLOR = (255, 0, 0)  # Rode oogjes

# Slime kleuren
SLIME_LARGE_COLOR = (128, 128, 128)  # Grijs voor grote slimes
SLIME_SMALL_COLOR = (160, 160, 160)  # Lichter grijs voor kleine slimes
SLIME_HIGHLIGHT_COLOR = (180, 180, 180)  # Highlight kleur

# Cave kleuren
CAVE_BACKGROUND_COLOR = (0, 0, 0)  # Zwart
CAVE_ENTRANCE_COLOR = (0, 0, 0)  # Zwart

# Fire kleuren
FIRE_COLOR_1 = (255, 69, 0)  # Oranje-rood
FIRE_COLOR_2 = (255, 140, 0)  # Donker oranje
FIRE_COLOR_3 = (255, 215, 0)  # Goud

# Key kleuren
KEY_COLOR = (255, 215, 0)  # Goud
KEY_DARK_COLOR = (180, 150, 0)  # Donker goud

# Old man kleuren
OLD_MAN_ROBE_COLOR = (139, 69, 19)  # Bruin voor mantel
OLD_MAN_SKIN_COLOR = (255, 220, 177)  # Huid kleur
OLD_MAN_BEARD_COLOR = (200, 200, 200)  # Wit/grijs voor baard
OLD_MAN_TEXT_COLOR = (255, 255, 255)  # Wit voor tekst

# UI kleuren
MINIMAP_UNVISITED_ROOM_COLOR = (60, 60, 60)  # Onbezochte rooms donkerder
GAME_OVER_TEXT_COLOR = (255, 0, 0)  # Rood voor game over tekst
GAME_OVER_SUBTITLE_COLOR = (255, 255, 255)  # Wit voor subtitle
OVERLAY_COLOR = (0, 0, 0)  # Zwart voor overlay

# Archer settings
ARCHER_WIDTH = 30
ARCHER_HEIGHT = 30
ARCHER_SPEED = 1.0
ARCHER_HEALTH = 2
ARCHER_SHOOT_COOLDOWN = 120  # 2 seconden @ 60 FPS
ARROW_SPEED = 4
ARROW_WIDTH = 12
ARROW_HEIGHT = 4

# Archer kleuren
ARCHER_BODY_COLOR = (32, 140, 128)  # Donker turkoois
ARCHER_EYE_COLOR = (255, 255, 255)
ARCHER_PUPIL_COLOR = (0, 0, 0)
ARCHER_BOW_COLOR = (139, 69, 19)  # Bruin voor boog
ARROW_COLOR = (160, 82, 45)  # Bruin voor pijl
ARROW_TIP_COLOR = (128, 128, 128)  # Grijs voor pijlpunt
