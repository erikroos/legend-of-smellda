import random
from items.health_drop import HealthDrop
from items.rupee import Rupee

class CombatManager:
    def __init__(self, collision_manager, hurt_sound=None):
        self.collision_manager = collision_manager
        self.hurt_sound = hurt_sound

    def _try_spawn_drop(self, x, y, room):
        """Probeer een drop te spawnen op deze positie
        Een vijand geeft OF een health drop OF een rupee drop (niet beide)"""
        rand = random.randint(1, 20)
        if rand <= 3:  # 1-3 = health drop (15% kans)
            health_drop = HealthDrop(x, y)
            room.health_drops.append(health_drop)
        elif rand <= 9:  # 4-9 = 1-rupee (30% kans)
            rupee = Rupee(x, y, value=1)
            room.rupee_drops.append(rupee)
        elif rand <= 12:  # 10-12 = 5-rupee (15% kans)
            rupee = Rupee(x, y, value=5)
            room.rupee_drops.append(rupee)

    def check_sword_hits(self, player, room):
        """Check of het zwaard monsters raakt"""
        hit_monsters = self.collision_manager.check_sword_hits(player, room.monsters)
        for monster in hit_monsters:
            monster.take_damage()
            # Als monster dood is, probeer een drop te spawnen (health OF rupee)
            if not monster.alive:
                self._try_spawn_drop(monster.x, monster.y, room)

    def check_monster_damage(self, player, room):
        """Check of monsters de speler raken"""
        damaged, damage_amount, monster = self.collision_manager.check_monster_damage(player, room.monsters)

        if damaged:
            hurt = player.take_damage(damage_amount)
            monster.reset_damage_cooldown()
            # Speel hurt-geluid af
            if hurt and self.hurt_sound:
                self.hurt_sound.play()

    def check_bat_sword_collision(self, player, dungeon_room):
        """Check of het zwaard een vleermuis raakt"""
        if not player.attacking:
            return

        sword_rect = player.get_attack_rect()
        if not sword_rect:
            return

        # Check collision met alle vleermuizen
        for bat in dungeon_room.bats:
            if bat.alive and sword_rect.colliderect(bat.rect):
                bat.take_damage(1)  # Vleermuizen sterven in 1 slag
                # Als bat dood is, probeer een drop te spawnen (health OF rupee)
                if not bat.alive:
                    self._try_spawn_drop(bat.x, bat.y, dungeon_room)

    def check_bat_player_collision(self, player, dungeon_room):
        """Check of een vleermuis de speler raakt"""
        for bat in dungeon_room.bats:
            if not bat.alive:
                continue

            if player.rect.colliderect(bat.rect):
                # Vleermuis raakt speler als cooldown voorbij is
                if bat.damage_cooldown == 0:
                    player.take_damage(1)  # Een half hartje schade
                    bat.damage_cooldown = bat.damage_cooldown_max
                    # Speel hurt geluid
                    if self.hurt_sound:
                        self.hurt_sound.play()

    def _find_safe_slime_positions(self, center_x, center_y, player, dungeon_room):
        """Vind veilige posities voor twee kleine slimes"""
        from entities.slime import Slime
        from constants import WALL_THICKNESS, HUD_HEIGHT

        # Kleine slime afmetingen
        small_width = 20
        small_height = 18

        # Probeer verschillende offset combinaties (links/rechts, boven/onder)
        offset_options = [
            [(-40, 0), (40, 0)],      # Links en rechts
            [(0, -40), (0, 40)],      # Boven en onder
            [(-30, -30), (30, 30)],   # Diagonaal links-boven en rechts-onder
            [(-30, 30), (30, -30)],   # Diagonaal links-onder en rechts-boven
        ]

        for offsets in offset_options:
            positions = []
            valid = True

            for offset_x, offset_y in offsets:
                new_x = center_x + offset_x
                new_y = center_y + offset_y

                # Check muren
                if (new_x < WALL_THICKNESS or
                    new_x + small_width > dungeon_room.screen_width - WALL_THICKNESS):
                    valid = False
                    break

                top_boundary = HUD_HEIGHT + WALL_THICKNESS
                bottom_boundary = HUD_HEIGHT + dungeon_room.screen_height - WALL_THICKNESS
                if (new_y < top_boundary or
                    new_y + small_height > bottom_boundary):
                    valid = False
                    break

                # Check player overlap
                slime_rect = Slime(new_x, new_y, is_large=False).rect
                if player.rect.colliderect(slime_rect):
                    valid = False
                    break

                positions.append((new_x, new_y))

            if valid:
                return positions

        # Fallback: spawn ze gewoon een beetje verder weg
        return [(center_x - 50, center_y), (center_x + 50, center_y)]

    def check_slime_sword_collision(self, player, dungeon_room):
        """Check of het zwaard een slime raakt - grote slimes splitsen!"""
        if not player.attacking:
            return

        sword_rect = player.get_attack_rect()
        if not sword_rect:
            return

        # Import Slime hier om circular import te voorkomen
        from entities.slime import Slime

        # Check collision met alle slimes
        slimes_to_add = []
        for slime in dungeon_room.slimes[:]:  # Copy list to modify during iteration
            if slime.alive and sword_rect.colliderect(slime.rect):
                should_split = slime.take_damage(1)

                # Als het een grote slime is die moet splitsen
                if should_split and slime.is_large:
                    # Vind veilige posities voor de kleine slimes
                    positions = self._find_safe_slime_positions(
                        slime.x, slime.y, player, dungeon_room)

                    # Maak twee kleine slimes op veilige posities
                    small_slime1 = Slime(positions[0][0], positions[0][1], is_large=False)
                    small_slime2 = Slime(positions[1][0], positions[1][1], is_large=False)
                    slimes_to_add.append(small_slime1)
                    slimes_to_add.append(small_slime2)

                    # Verwijder de grote slime (GEEN drops voor grote slimes)
                    slime.alive = False

                # Als KLEINE slime dood is, probeer een drop te spawnen (health OF rupee)
                elif not slime.alive and not slime.is_large:
                    self._try_spawn_drop(slime.x, slime.y, dungeon_room)

                # Stop na eerste hit (anders raakt het zwaard meerdere slimes tegelijk)
                break

        # Voeg nieuwe kleine slimes toe
        dungeon_room.slimes.extend(slimes_to_add)

    def check_slime_player_collision(self, player, dungeon_room):
        """Check of een slime de speler raakt"""
        for slime in dungeon_room.slimes:
            if not slime.alive:
                continue

            if player.rect.colliderect(slime.rect):
                # Slime raakt speler als cooldown voorbij is
                if slime.damage_cooldown == 0:
                    player.take_damage(1)  # Een half hartje schade
                    slime.damage_cooldown = slime.damage_cooldown_max
                    # Speel hurt geluid
                    if self.hurt_sound:
                        self.hurt_sound.play()

    def check_boss_sword_collision(self, player, dungeon_room, secret_sound=None):
        """Check of het zwaard de boss raakt"""
        if not dungeon_room.boss or not dungeon_room.boss.alive:
            return False

        if not player.attacking:
            return False

        sword_rect = player.get_attack_rect()
        if not sword_rect:
            return False

        # Check collision met boss
        if sword_rect.colliderect(dungeon_room.boss.rect):
            boss_died = dungeon_room.boss.take_damage()
            # Als boss dood is, maak pushable block pushable en speel secret geluid
            if not dungeon_room.boss.alive and hasattr(dungeon_room, 'pushable_block'):
                dungeon_room.pushable_block_pushable = True
                # Speel secret geluid af
                if secret_sound:
                    secret_sound.play()
            return boss_died
        return False

    def check_boss_player_collision(self, player, dungeon_room):
        """Check of de boss de speler raakt (body collision)"""
        if not dungeon_room.boss or not dungeon_room.boss.alive:
            return

        if player.rect.colliderect(dungeon_room.boss.rect):
            # Boss raakt speler = 1 HP schade (half hartje)
            hurt = player.take_damage(1)
            if hurt and self.hurt_sound:
                self.hurt_sound.play()

    def check_fireball_player_collision(self, player, dungeon_room):
        """Check of een vuurbal de speler raakt"""
        if not dungeon_room.boss or not dungeon_room.boss.alive:
            return

        for fireball in dungeon_room.boss.fireballs[:]:
            if player.rect.colliderect(fireball.rect):
                # Vuurbal raakt speler = 2 HP schade (heel hartje)
                hurt = player.take_damage(2)
                if hurt and self.hurt_sound:
                    self.hurt_sound.play()
                # Verwijder vuurbal na hit
                dungeon_room.boss.fireballs.remove(fireball)
