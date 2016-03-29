from enum import IntEnum
from random import sample

class Side(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def opposite(side):
        if side is Side.UP: 
            return Side.DOWN
        elif side is Side.DOWN: 
            return Side.UP
        elif side is Side.RIGHT:
            return Side.LEFT
        elif side is Side.LEFT:
            return Side.RIGHT


    def random_all():
        return sample(list(Side), 4)


class Cell:

    def __init__(self, pos_x, pos_y,
            nb_up=None, nb_right=None, nb_down=None, nb_left=None):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.neighbours = {Side.UP: nb_up,
                           Side.RIGHT: nb_right,
                           Side.DOWN: nb_down,
                           Side.LEFT: nb_left }

        self.walls = {Side.UP: True,
                      Side.RIGHT: True,
                      Side.DOWN: True,
                      Side.LEFT: True }

        self.outer_walls = []
        self.is_start = False
        self.is_finish = False

    def set_neighbour(self, neighbour, side):
        self.neighbours[side] = neighbour
        if neighbour.neighbours[Side.opposite(side)] is None:
            neighbour.set_neighbour(self, Side.opposite(side))

    def get_neighbour(self, side):
        if self.neighbours[side] is not None:
            return self.neighbours[side]
        else:
            return self
    
    def is_neighbour(self, other):
        if other in self.neighbours.values():
            return True
        else:
            return False

    def add_outer_wall(self, side):
        self.outer_walls.append(side)

    def is_not_visited(self):
        return all(x is True for x in self.walls.values())

    def has_outer_walls(self):
        if len(self.outer_walls) > 0: return True
        else: return False

    def knock_wall(self, side):
        if self.walls[side] and self.neighbours[side] is not None:
            self.walls[side] = False
            self.neighbours[side].knock_wall(Side.opposite(side))
            return True
        else:
            return False

    def get_walls(self, intact=True):
        walls = []
        for key, value in self.walls.items():
            if intact == value:
                walls.append(key)
        return walls


    def coords(self):
        return "Cell at {}.{}".format(self.pos_x, self.pos_y)

    def __str__(self):
        me = "X.Y: {}.{}\n".format(self.pos_x, self.pos_y)
        me += "Neighbours:\n"
        for key, value in sorted(self.neighbours.items()):
            try:
                me += "\tOn side {}: {}\n".format(
                        key.name, value.coords())
            except:
                me += "\tOn side {}: None\n".format(key.name,)
        if len(self.outer_walls) > 0:
            me += "Outer walls:\n"
            for wall in self.outer_walls:
                me += "{}\n".format(wall.name,)
        if self.is_start:
            me += "Is start point\n"
        if self.is_finish:
            me += "Is finish point\n"
        return me
