import random
from algoviz.svg import Circle, Rect, SVGView
from dungeon import Dungeon

class Player:
    def __init__(self, max_health: int, movement_speed: int, dps: int, damage_enable: bool):
        self.max_health = max_health
        self.health = self.max_health
        self.dps = dps
        self.movement_speed = movement_speed
        self.damage_enable = damage_enable
        self.player1 = None
        self.hBar = None
        self.hBar2 = None
        # Coordinates for spawn
        self.x = 0  
        self.y = 0
        self.spawn_legal = False
        self.key = ""
        self.p_key = [self.key]
        self.direction_x = 0
        self.direction_y = 0

    def set_health(self, health: int):
        if self.health > self.max_health:
            self.health = self.max_health
        else:
            self.health = health
        # healthbar
        # works only if health is divisible by 20 (integer division)
        self.hBar2.set_width(self.health * 100 // self.max_health // 10 * 2)
        return self.hBar2.get_width()

    def get_health(self):
        return self.health

    def get_dps(self):
        return self.dps

    def get_x(self):
        return self.player1.get_x()

    def get_y(self):
        return self.player1.get_y()

    def get_radius(self):
        return self.player1.get_radius()

    def get_movement_speed(self):
        return self.movement_speed

    def inc_movement_speed(self, increment: int):
        self.movement_speed = self.movement_speed + increment  # increase speed

    def dec_movement_speed(self, decrement: int):
        self.movement_speed = self.movement_speed - decrement  # decrease speed

    def set_color(self, color: str):
        self.player1.set_fill(color)

    def set_damage_enable(self, is_enabled):
        self.damage_enable = is_enabled

    def get_damage_enable(self):
        return self.damage_enable

    def spawn_player(self, svg_view: SVGView, dungeon: Dungeon):
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

        # Checks hitbox of dungeon walls: If the next movement does not land the player
        # within the walls, it is legal
        if (
            self.key == "ArrowUp"
            and dungeon.inner_wall_layout[pos_x][pos_y - self.movement_speed] == False
        ):
            self.direction_x = 0
            self.direction_y = self.movement_speed * -1
        elif (
            self.key == "ArrowDown"
            and dungeon.inner_wall_layout[pos_x][pos_y + self.movement_speed] == False
        ):
            self.direction_x = 0
            self.direction_y = self.movement_speed
        elif (
            self.key == "ArrowLeft"
            and dungeon.inner_wall_layout[pos_x - self.movement_speed][pos_y] == False
        ):
            self.direction_x = self.movement_speed * -1
            self.direction_y = 0
        elif (
            self.key == "ArrowRight"
            and dungeon.inner_wall_layout[pos_x + self.movement_speed][pos_y] == False
        ):
            self.direction_x = self.movement_speed
            self.direction_y = 0

        # Move Player
        self.player1.move_to(
            self.player1.get_x() + self.direction_x, self.player1.get_y() + self.direction_y
        )
        self.direction_x = 0
        self.direction_y = 0
        # Move healthBar
        self.hBar.move_to(self.player1.get_x() - 10, self.player1.get_y() + 15)
        self.hBar2.move_to(self.player1.get_x() - 10, self.player1.get_y() + 15)

    def game_over(self):
        if self.health >= 0:
            return True
        else:
            return False
