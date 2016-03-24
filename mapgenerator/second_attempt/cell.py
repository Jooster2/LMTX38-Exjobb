from enum import Enum
from random import sample

class Side(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def opposite(direction):
        if direction is Side.UP:
            return Side.DOWN
        elif direction is Side.DOWN:
            return Side.UP
        elif direction is Side.RIGHT:
            return Side.LEFT
        elif direction is Side.LEFT:
            return Side.RIGHT

    def random_all():
        return sample(list(Side), 4)



class Cell:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.outer_walls = []
        self.neighbours = {Side.UP: None,
                           Side.RIGHT: None,
                           Side.DOWN: None,
                           Side.LEFT: None}
        self.is_start = False
        self.is_finish = False

    def is_not_visited(self):
        return all(x is None for x in self.neighbours.values())

    def make_outer_wall(self, direction):
        self.outer_walls.append(direction)

    def has_outer_walls(self):
        if len(self.outer_walls) > 0:
            return True
        else:
            return False

    def make_neighbour(self, cell, direction, force=False):
        try:
            #print("Assigning neighbour")
            if self.neighbours[direction] is None: 
                if cell.is_not_visited() or force:
                    self.neighbours[direction] = cell
                    cell.make_neighbour(self, 
                            Side.opposite(direction))
                    return True
                else:
                    return False
            else:
                return False
        except KeyError as e:
            print(e)
            return False

    def get_neighbour_coords(self, direction):
        if direction == Side.UP: 
            return (self.pos_x, self.pos_y-1)
        elif direction == Side.RIGHT: 
            return (self.pos_x+1, self.pos_y)
        elif direction == Side.DOWN:
            return (self.pos_x, self.pos_y+1)
        elif direction == Side.LEFT:
            return (self.pos_x-1, self.pos_y)

    def position(self):
        return "{}:{}".format(self.pos_x, self.pos_y)
    
    def __str__(self):
        me = "X.Y: {}.{} ".format(
                self.pos_x, self.pos_y)
        me += "Connected to: {}".format(
                [x.position() for i,x in enumerate(
                    self.neighbours.values())
                    if x is not None],)
        if self.is_start: me += " Starting Point"
        elif self.is_finish: me += " Finish Point"
        return me

