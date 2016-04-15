from random import sample, randrange
from directions import Side



class Cell:
    """Cell is a square that represents a section of the map."""

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
        """
        Pair this cell with another, declaring them neighbours.
        neighbour -- another cell to pair this one with
        side -- the side on which the other cell is located
        """

        self.neighbours[side] = neighbour
        if neighbour.neighbours[Side.opposite(side)] is None:
            neighbour.set_neighbour(self, Side.opposite(side))

    def get_neighbour(self, side):
        """Return the neighbour located on specified side."""

        if self.neighbours[side] is not None:
            return self.neighbours[side]
        else:
            return self
    
    def is_neighbour(self, other):
        """Check whether this cell and the other are neighbours."""
        if other in self.neighbours.values():
            return True
        else:
            return False

    def has_unvisited_neighbours(self):
        """Return whether this cell has unvisited neighbours."""
        for neighbour in self.neighbours.values():
            if neighbour is not None and neighbour.is_not_visited():
                return True
        return False

    def remove_as_neighbour(self):
        for side, cell in self.neighbours.items():
            cell.neighbours[Side.opposite(side)] = None

    def add_outer_wall(self, side):
        """Add an outer wall to this cell on specified side."""
        self.outer_walls.append(side)

    def is_not_visited(self):
        """Return whether this cell has all walls intact."""
        return all(x is True for x in self.walls.values())

    def has_outer_walls(self):
        """Return whether this cell has any outer walls."""
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
        """
        Return a list of all walls (not outer) this cell has.
        intact -- whether to return a list of intact walls
        """

        wall_list = []
        for key, value in self.walls.items():
            if intact == value:
                wall_list.append(key)
        return wall_list

    def calc_steps(self, other):
        """
        Return a tuple, containing the x and y distances to
        the other cell.
        """
        return (other.pos_x - self.pos_x, \
                other.pos_y - self.pos_y)

    def distance_to(self, other):
        """
        Return the amount of cells between this cell and the other,
        in absolute terms.
        """
        return (abs(other.pos_x - self.pos_x) + \
                abs(other.pos_y - self.pos_y))


    def transmute(self, other):
        """Transmute this cell into another."""
        self.pos_x = other.pos_x
        self.pos_y = other.pos_y
        self.is_start = other.is_start
        self.is_finish = other.is_finish
        self.outer_walls = other.outer_walls

        other.remove_as_neighbour()
        for side, cell in other.neighbours.items():
            self.set_neighbour(cell, side)
        for side, value in other.walls.items():
            self.walls[side] = value





    def coords(self):
        """
        Return a formatted string with some info about this cells
        position.
        """
        me = "Cell at {}.{}".format(self.pos_x, self.pos_y)
        if self.is_start:
            me += " Is Start"
        elif self.is_finish:
            me += " Is Finish"
        return me

    def __str__(self):
        """
        Return a formatted string with all relevant info about this
        cell.
        """
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
