import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()

        self.audio_muted = False
        self.overworld_music_playing = False

        # Laad muziek en geluiden
        self.load_music()
        self.load_sounds()

    def load_music(self):
        """Laad achtergrondmuziek"""
        try:
            pygame.mixer.music.load('assets/music/zelda-theme.ogg')
            pygame.mixer.music.set_volume(0.2)  # Volume 0.0 tot 1.0
            pygame.mixer.music.play(-1)  # -1 = loop oneindig
            self.overworld_music_playing = True
        except pygame.error as e:
            print(f"Kon muziek niet laden: {e}")

    def load_sounds(self):
        """Laad sound effects"""
        try:
            self.push_sound = pygame.mixer.Sound('assets/sounds/secret.wav')
            self.push_sound.set_volume(0.3)
        except pygame.error as e:
            print(f"Kon push sound niet laden: {e}")
            self.push_sound = None

        try:
            self.sword_sound = pygame.mixer.Sound('assets/sounds/sword-slash.wav')
            self.sword_sound.set_volume(0.3)
        except pygame.error as e:
            print(f"Kon sword sound niet laden: {e}")
            self.sword_sound = None

        try:
            self.get_item_sound = pygame.mixer.Sound('assets/sounds/get-item.wav')
            self.get_item_sound.set_volume(0.4)
        except pygame.error as e:
            print(f"Kon get-item sound niet laden: {e}")
            self.get_item_sound = None

        try:
            self.hurt_sound = pygame.mixer.Sound('assets/sounds/hurt.wav')
            self.hurt_sound.set_volume(0.4)
        except pygame.error as e:
            print(f"Kon hurt sound niet laden: {e}")
            self.hurt_sound = None

        try:
            self.boss_sound = pygame.mixer.Sound('assets/sounds/boss.wav')
            self.boss_sound.set_volume(0.5)
        except pygame.error as e:
            print(f"Kon boss sound niet laden: {e}")
            self.boss_sound = None

        try:
            self.get_heart_sound = pygame.mixer.Sound('assets/sounds/get-heart.wav')
            self.get_heart_sound.set_volume(0.4)
        except pygame.error as e:
            print(f"Kon get-heart sound niet laden: {e}")
            self.get_heart_sound = None

        try:
            self.get_rupee_sound = pygame.mixer.Sound('assets/sounds/get-rupee.wav')
            self.get_rupee_sound.set_volume(0.4)
        except pygame.error as e:
            print(f"Kon get-rupee sound niet laden: {e}")
            self.get_rupee_sound = None

        try:
            self.shield_sound = pygame.mixer.Sound('assets/sounds/shield.wav')
            self.shield_sound.set_volume(0.4)
        except pygame.error as e:
            print(f"Kon shield sound niet laden: {e}")
            self.shield_sound = None

    def switch_to_dungeon_music(self):
        """Switch naar dungeon muziek"""
        if self.overworld_music_playing:
            try:
                pygame.mixer.music.load('assets/music/dungeon-theme.ogg')
                pygame.mixer.music.set_volume(0.0 if self.audio_muted else 0.2)
                pygame.mixer.music.play(-1)
                self.overworld_music_playing = False
            except pygame.error as e:
                print(f"Kon dungeon muziek niet laden: {e}")

    def switch_to_overworld_music(self):
        """Switch terug naar overworld muziek"""
        if not self.overworld_music_playing:
            try:
                pygame.mixer.music.load('assets/music/zelda-theme.ogg')
                pygame.mixer.music.set_volume(0.0 if self.audio_muted else 0.2)
                pygame.mixer.music.play(-1)
                self.overworld_music_playing = True
            except pygame.error as e:
                print(f"Kon overworld muziek niet laden: {e}")

    def toggle_mute(self):
        """Toggle alle audio aan/uit"""
        self.audio_muted = not self.audio_muted

        if self.audio_muted:
            # Mute alles
            pygame.mixer.music.set_volume(0.0)
            if self.push_sound:
                self.push_sound.set_volume(0.0)
            if self.sword_sound:
                self.sword_sound.set_volume(0.0)
            if self.get_item_sound:
                self.get_item_sound.set_volume(0.0)
            if self.hurt_sound:
                self.hurt_sound.set_volume(0.0)
            if self.boss_sound:
                self.boss_sound.set_volume(0.0)
            if self.get_heart_sound:
                self.get_heart_sound.set_volume(0.0)
            if self.get_rupee_sound:
                self.get_rupee_sound.set_volume(0.0)
            if self.shield_sound:
                self.shield_sound.set_volume(0.0)
        else:
            # Unmute alles - herstel originele volumes
            pygame.mixer.music.set_volume(0.2)
            if self.push_sound:
                self.push_sound.set_volume(0.3)
            if self.sword_sound:
                self.sword_sound.set_volume(0.3)
            if self.get_item_sound:
                self.get_item_sound.set_volume(0.4)
            if self.hurt_sound:
                self.hurt_sound.set_volume(0.4)
            if self.boss_sound:
                self.boss_sound.set_volume(0.5)
            if self.get_heart_sound:
                self.get_heart_sound.set_volume(0.4)
            if self.get_rupee_sound:
                self.get_rupee_sound.set_volume(0.4)
            if self.shield_sound:
                self.shield_sound.set_volume(0.4)

    def stop(self):
        """Stop de muziek netjes"""
        pygame.mixer.music.stop()
