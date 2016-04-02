from enum import IntEnum
from random import sample, randrange

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

    def convert(number):
        if type(number) is Side:
            return {Side.UP: 0,
                    Side.RIGHT: 1,
                    Side.DOWN: 2,
                    Side.LEFT: 3}[number]
        elif type(number) is int:
            return {0: Side.UP,
                    1: Side.RIGHT,
                    2: Side.DOWN,
                    3: Side.LEFT}[number]
        else:
            return None

    def biased_random(side_1, side_2, side_3=None, side_4=None,
            p_1=1, p_2=1, p_3=0, p_4=0):
        interval_1 = range(p_1)
        pool = p_1
        interval_2 = range(pool, pool+p_2)
        pool += p_2
        interval_3 = range(pool, pool+p_3)
        pool += p_3
        interval_4 = range(pool, pool+p_4)
        pool += p_4
        choice = randrange(pool)
        if choice in interval_1:
            return side_1
        elif choice in interval_2:
            return side_2
        elif choice in interval_3:
            return side_3
        elif choice in interval_4:
            return side_4



        """rand_list = []
        side1 = Side.convert(side1)
        side2 = Side.convert(side2)
        for x in range(level):
            rand_list.append(side1)
        rand_list.append(side2)
        return sample..."""

        
        
    def random_all():
        return sample(list(Side), 4)

    def convert_sides(x, y):
        res = []
        if x < 0:
            res.append(Side.LEFT)
        else:
            res.append(Side.RIGHT)
        if y < 0:
            res.append(Side.UP)
        else:
            res.append(Side.DOWN)
        return res



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
        if len(self.outer_walls) > 0:
            return True
        else:
            return False

    def knock_wall(self, side):
        if self.walls[side] and self.neighbours[side] is not None:
            self.walls[side] = False
            self.neighbours[side].knock_wall(Side.opposite(side))
            return True
        else:
            return False

    def get_walls(self, intact=True):
        wall_list = []
        for key, value in self.walls.items():
            if intact == value:
                wall_list.append(key)
        return wall_list

    def calc_steps(self, other):
        return (other.pos_x - self.pos_x, \
                other.pos_y - self.pos_y)

    def distance_to(self, other):
        return (abs(other.pos_x - self.pos_x) + \
                abs(other.pos_y - self.pos_y))


    def coords(self):
        me = "Cell at {}.{}".format(self.pos_x, self.pos_y)
        if self.is_start:
            me += " Is Start"
        elif self.is_finish:
            me += " Is Finish"
        return me

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
