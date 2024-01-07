import random
from algoviz import AlgoViz
from algoviz.svg import SVGView, Image

class Dungeon:
    def __init__(self):
        self.interior_walls = []
        self.debug_layout = []
        self.random_x = 0
        self.random_y = 0
        self.dungeon_size_x = 600
        self.dungeon_size_y = 600
        self.wall_size = 20
        self.boundary_walls = 120

        # Layout variable used for collision detection with walls
        self.inner_wall_layout = [[True] * 600 for _ in range(600)]

        self.wall_background = []
        self.dungeon = SVGView(600, 600, "Dungeon Crawler")

    def get_dungeon_size_x(self):
        return self.dungeon_size_x

    def get_dungeon_size_y(self):
        return self.dungeon_size_y

    def get_wall_size(self):
        return self.wall_size

    def get_interior_walls(self):
        return self.interior_walls

    def set_dungeon_size_x(self, dungeon_size_x):
        self.dungeon_size_x = dungeon_size_x

    def set_dungeon_size_y(self, dungeon_size_y):
        self.dungeon_size_y = dungeon_size_y

    def set_wall_size(self, wall_size):
        self.wall_size = wall_size

    def initialize_layout_array(self):
        self.inner_wall_layout = [[True] * 600 for _ in range(600)]

    def random_walker_algorithm(self, m_tunnels, m_tunnel_length):
        self.initialize_layout_array()
        fill_color = "#5F9EA0"
        x = random.randrange(0, 600, self.wall_size)
        y = random.randrange(0, 600, self.wall_size)
        max_tunnels = m_tunnels
        max_tunnel_length = m_tunnel_length
        last_direction = 0
        rand_direction = 0

        while max_tunnels > 0:
            rand_direction = random.randint(1, 4)
            random_tunnel_length = random.randint(1, max_tunnel_length)
            tunnel_length = 0

            while tunnel_length < random_tunnel_length:
                rand_direction = random.randint(1, 4)
                while (
                    (x <= self.wall_size and rand_direction == 3)
                    or (x >= 600 - self.wall_size and rand_direction == 4)
                    or (y <= self.wall_size and rand_direction == 1)
                    or (y >= 600 - self.wall_size and rand_direction == 2)
                    or (last_direction == 1 and rand_direction == 2)
                    or (last_direction == 2 and rand_direction == 1)
                    or (last_direction == 3 and rand_direction == 4)
                    or (last_direction == 4 and rand_direction == 3)
                ):
                    rand_direction = random.randint(1, 4)

                while (
                    rand_direction == 1
                    and (y - random_tunnel_length * self.wall_size) >= 0
                    and tunnel_length < random_tunnel_length
                ):
                    for d in range(random_tunnel_length * self.wall_size):
                        if (y - d) % self.wall_size == 0:
                            tunnel_length += 1
                            self.interior_walls.append(
                                (x, y - d, self.wall_size, self.wall_size)
                            )
                            for i in range(self.wall_size):
                                for j in range(self.wall_size):
                                    self.inner_wall_layout[x + j][y - d - i] = False
                    y -= random_tunnel_length * self.wall_size
                    last_direction = rand_direction

                while (
                    rand_direction == 2
                    and (y + random_tunnel_length * self.wall_size) < 600
                    and tunnel_length < random_tunnel_length
                ):
                    for d in range(random_tunnel_length * self.wall_size):
                        if (y + d) % self.wall_size == 0:
                            tunnel_length += 1
                            self.interior_walls.append(
                                (x, y + d, self.wall_size, self.wall_size)
                            )
                            for i in range(self.wall_size):
                                for j in range(self.wall_size):
                                    self.inner_wall_layout[x + j][y + d + i] = False
                    y += random_tunnel_length * self.wall_size
                    last_direction = rand_direction

                while (
                    rand_direction == 3
                    and (x - random_tunnel_length * self.wall_size) >= 0
                    and tunnel_length < random_tunnel_length
                ):
                    for d in range(random_tunnel_length * self.wall_size):
                        if (x - d) % self.wall_size == 0:
                            tunnel_length += 1
                            self.interior_walls.append(
                                (x - d, y, self.wall_size, self.wall_size)
                            )
                            for i in range(self.wall_size):
                                for j in range(self.wall_size):
                                    self.inner_wall_layout[x - d - i][y + j] = False
                    x -= random_tunnel_length * self.wall_size
                    last_direction = rand_direction

                while (
                    rand_direction == 4
                    and (x + random_tunnel_length * self.wall_size) < 600
                    and tunnel_length < random_tunnel_length
                ):
                    for d in range(random_tunnel_length * self.wall_size):
                        if (x + d) % self.wall_size == 0:
                            tunnel_length += 1
                            self.interior_walls.append(
                                (x + d, y, self.wall_size, self.wall_size)
                            )
                            for i in range(self.wall_size):
                                for j in range(self.wall_size):
                                    self.inner_wall_layout[x + d + i][y + j] = False
                    x += random_tunnel_length * self.wall_size
                    last_direction = rand_direction

                max_tunnels -= 1

    def spawn_dungeon(self):
        for x in range(0, 600, 20):
            for y in range(0, 600, 20):
                self.wall_background.append(Image("wall5.png", x, y, 20, 20, self.dungeon))
        self.random_walker_algorithm(200, 6)

# Example usage:
# dungeon = Dungeon()
# dungeon.spawn_dungeon()
# print(dungeon.get_interior_walls())
