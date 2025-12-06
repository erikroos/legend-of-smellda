from entities.old_man import OldMan
from items.sword_item import SwordItem
from rooms.base_cave_room import BaseCaveRoom

class CaveRoom(BaseCaveRoom):
    def __init__(self):
        super().__init__()

        # NPC en items (specifiek voor sword cave)
        self.old_man = OldMan(self.center_x - 20, self.center_y - 60)
        self.sword = SwordItem(self.center_x - 6, self.center_y + 20)

    def render_content(self, screen):
        """Render sword cave specific content"""
        # Render sword
        self.sword.render(screen)

        # Render old man
        self.old_man.render(screen)
