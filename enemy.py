import random
from algoviz.svg import Image, Rect, SVGView
from dungeon import Dungeon  # Assuming dungeon is in a separate module

class Enemy:
    def __init__(self, e_health: int, e_dmg: int):
        self.max_health = 500
        self.e_health = self.max_health
        self.e_dmg = 200
        self.enemy1 = None
        self.x = 0
        self.y = 0
        self.spawn_legal = False
        self.width = 20
        self.hBar = None
        self.hBar2 = None
        self.dx = 0
        self.dy = 0
        self.pos_x = 0
        self.pos_y = 0

    def spawn_enemy(self, A, D):
        while not self.spawn_legal:
            self.spawn_legal = False
            self.x = random.randrange(20, 580, 10)
            self.y = random.randrange(20, 580, 10)
            # fit to the grid
            #self.x = self.x // 10 * 10
            #self.y = self.y // 10 * 10
            if (
                D.inner_wall_layout[self.x][self.y] == 0
                and D.inner_wall_layout[self.x + 10][self.y] == 0
                and D.inner_wall_layout[self.x][self.y + 10] == 0
                and D.inner_wall_layout[self.x - 10][self.y] == 0
                and D.inner_wall_layout[self.x][self.y - 10] == 0
                and D.inner_wall_layout[self.x + 10][self.y + 10] == 0
                and D.inner_wall_layout[self.x - 10][self.y - 10] == 0
            ):
                self.spawn_legal = True

        self.enemy1 = Image("Frankenstein.svg", self.x, self.y, self.width, self.width, A)
        self.hBar = Rect(self.enemy1.get_x() - 10, self.enemy1.get_y() + 15, 20, 7, A)
        self.hBar2 = Rect(self.enemy1.get_x() - 10, self.enemy1.get_y() + 15, 20, 7, A)
        self.hBar.set_color("black")
        self.hBar.set_fill("red")
        self.hBar2.set_fill("green")

    def get_width(self):
        return self.width

    def get_x(self):
        return self.enemy1.get_x()

    def get_y(self):
        return self.enemy1.get_y()

    def get_dmg(self):
        return self.e_dmg

    def set_e_health(self, e_health):
        self.e_health = e_health
        # healthbar
        # works only if health is divisible by 20 (integer division)
        self.hBar2.set_width(e_health * 100 // self.max_health // 10 * 2)
        # if enemy dies
        if e_health <= 0:
            self.enemy1.__del__()
            self.hBar.__del__()
            self.hBar2.__del__()
            self.enemy1.move_to(0, 0)  # somehow the player collides with the enemy even if the enemy is not in the SVG

    def get_e_health(self):
        return self.e_health

    # if collides...
    def collides(self, D):
        return True

    def enemy_move(self, A, D):
        direction = random.randint(0, 3)
        wall_size = D.get_wall_size()
        if self.collides(D):
            if direction == 0 and not D.inner_wall_layout[self.x + wall_size // 2][self.y]:
                self.dy = 0
                self.dx = 1
            elif direction == 1 and not D.inner_wall_layout[self.x - wall_size // 2][self.y]:
                self.dy = 0
                self.dx = -1
            elif direction == 2 and not D.inner_wall_layout[self.x][self.y - wall_size // 2]:
                self.dy = -1
                self.dx = 0
            elif direction == 3 and not D.inner_wall_layout[self.x][self.y + wall_size // 2]:
                self.dy = 1
                self.dx = 0

        self.enemy1.move_to(self.enemy1.get_x() + self.dx, self.enemy1.get_y() + self.dy)
        # move healthBar
        self.hBar.move_to(self.enemy1.get_x() - 10, self.enemy1.get_y() + 15)
        self.hBar2.move_to(self.enemy1.get_x() - 10, self.enemy1.get_y() + 15)
