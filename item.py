import random
from algoviz.svg import Image, SVGView
from dungeon import Dungeon  # Assuming dungeon is in a separate module

class Item:
    def __init__(self):
        self.pic_source = ""
        self.item1 = None
        self.kind = random.randint(0, 2)
        self.x = 0  # Spawn coords
        self.y = 0
        self.spawn_legal = False
        self.width = 20

    def move_to(self, x, y):
        self.item1.move_to(x, y)

    def get_kind(self):
        return self.kind

    def remove_from_view(self):
        self.item1.__del__()

    def get_x(self):
        return self.item1.get_x()

    def get_y(self):
        return self.item1.get_y()

    def get_width(self):
        return self.width

    def spawn_item(self, svg_view, dungeon):
        if self.kind == 0:
            # Speed
            self.pic_source = "flash.svg"
        elif self.kind == 1:
            # Health
            self.pic_source = "Heart.svg"
        elif self.kind == 2:
            # Barrier
            self.pic_source = "shield.svg"

        while not self.spawn_legal:
            self.x = random.randrange(20, 580, 10)
            self.y = random.randrange(20, 580, 10)
            # fit to the grid
            self.x = self.x // 10 * 10
            self.y = self.y // 10 * 10
            # Testing whether it matches the wall layout so that items spawn in empty spaces
            if (
                dungeon.inner_wall_layout[self.x][self.y] == 0
                and dungeon.inner_wall_layout[self.x + 10][self.y] == 0
                and dungeon.inner_wall_layout[self.x][self.y + 10] == 0
                and dungeon.inner_wall_layout[self.x - 10][self.y] == 0
                and dungeon.inner_wall_layout[self.x][self.y - 10] == 0
                and dungeon.inner_wall_layout[self.x + 10][self.y + 10] == 0
                and dungeon.inner_wall_layout[self.x - 10][self.y - 10] == 0
            ):
                self.spawn_legal = True

        self.item1 = Image(self.pic_source, self.x, self.y, self.width, self.width, svg_view)
