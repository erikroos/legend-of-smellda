from entities.old_man import OldMan
from rooms.base_cave_room import BaseCaveRoom

class HintCaveRoom(BaseCaveRoom):
    def __init__(self):
        super().__init__()

        # NPC - oude man met hint tekst (specifiek voor hint cave)
        self.old_man = OldMan(self.center_x - 20, self.center_y - 60)
        # Verander de tekst van de oude man naar de hint
        self.old_man.text = "THERE IS HEALTH IN THE SOUTHWEST"
        self.old_man.text2 = "AND THERE IS A SECRET IN THE SOUTHEAST."

    def render_content(self, screen):
        """Render hint cave specific content"""
        # Render old man (altijd zichtbaar, geen zwaard om op te pakken)
        self.old_man.render(screen)
