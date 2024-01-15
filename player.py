import random
from algoviz.svg import Circle, Rect, SVGView
from dungeon import Dungeon  # Assuming dungeon is in a separate module

class Player:
    def __init__(self, max_health, p_speed, dmg, damage_enable):
        self.max_health = max_health
        self.p_health = self.max_health
        self.dmg = dmg
        self.p_speed = p_speed
        self.damage_enable = damage_enable
        self.player1 = None
        self.hBar = None
        self.hBar2 = None
        self.x = 0  # Coords for spawn
        self.y = 0
        self.spawn_legal = False
        self.key = ""
        self.p_key = [self.key]
        self.direction_x = 0
        self.direction_y = 0

    def set_p_health(self, h):
        if self.p_health > self.max_health:
            self.p_health = self.max_health
        else:
            self.p_health = h
        # healthbar
        # works only if health is divisible by 20 (integer division)
        self.hBar2.set_width(self.p_health * 100 // self.max_health // 10 * 2)
        return self.hBar2.get_width()

    def get_p_health(self):
        return self.p_health

    def get_dmg(self):
        return self.dmg

    def get_x(self):
        return self.player1.get_x()

    def get_y(self):
        return self.player1.get_y()

    def get_radius(self):
        return self.player1.get_radius()

    # speed
    def get_p_speed(self):
        return self.p_speed

    def inc_p_speed(self, inc):
        self.p_speed = self.p_speed + inc  # increase Speed

    def dec_p_speed(self, dec):
        self.p_speed = self.p_speed - dec  # decrease Speed

    # color
    def set_color(self, color):
        self.player1.set_fill(color)

    # damage_enable
    def set_damage_enable(self, b):
        self.damage_enable = b

    def get_damage_enable(self):
        return self.damage_enable

    def spawn_player(self, svg_view, dungeon):
        while not self.spawn_legal:
            self.spawn_legal = False
            self.x = random.randrange(0, 600)
            self.y = random.randrange(0, 600)
            # fit to the grid
            self.x = self.x // 10 * 10
            self.y = self.y // 10 * 10
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

        self.player1 = Circle(self.x, self.y, 10, svg_view)
        self.player1.set_fill("black")
        self.hBar = Rect(self.player1.get_x() - 10, self.player1.get_y() + 15, 20, 7, svg_view)
        self.hBar2 = Rect(self.player1.get_x() - 10, self.player1.get_y() + 15, 20, 7, svg_view)
        self.hBar.set_color("black")
        self.hBar.set_fill("red")
        self.hBar2.set_fill("green")

    def player_move(self, svg_view:SVGView, dungeon:Dungeon):
        self.key = svg_view.last_key()
        pos_x = self.player1.get_x()
        pos_y = self.player1.get_y()
        wall_size = dungeon.get_wall_size()

        if (
            self.key == "ArrowUp"
            and dungeon.inner_wall_layout[pos_x][pos_y - self.p_speed] == False
        ):
            self.direction_x = 0
            self.direction_y = self.p_speed * -1
        elif (
            self.key == "ArrowDown"
            and dungeon.inner_wall_layout[pos_x][pos_y + self.p_speed] == False
        ):
            self.direction_x = 0
            self.direction_y = self.p_speed
        elif (
            self.key == "ArrowLeft"
            and dungeon.inner_wall_layout[pos_x - self.p_speed][pos_y] == False
        ):
            self.direction_x = self.p_speed * -1
            self.direction_y = 0
        elif (
            self.key == "ArrowRight"
            and dungeon.inner_wall_layout[pos_x + self.p_speed][pos_y] == False
        ):
            self.direction_x = self.p_speed
            self.direction_y = 0

        # move Player
        self.player1.move_to(
            self.player1.get_x() + self.direction_x, self.player1.get_y() + self.direction_y
        )
        self.direction_x = 0
        self.direction_y = 0
        # move healthBar
        self.hBar.move_to(self.player1.get_x() - 10, self.player1.get_y() + 15)
        self.hBar2.move_to(self.player1.get_x() - 10, self.player1.get_y() + 15)

    def game_over(self):
        if self.p_health >= 0:
            return True
        else:
            return False
