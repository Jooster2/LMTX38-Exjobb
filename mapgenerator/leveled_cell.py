from cell import Cell
from directions import Side, Corner


class LeveledCell(Cell):
    """LeveledCell is a Cell with additional data about levels."""

    def __init__(self, pos_x, pos_y,
            nb_up=None, nb_right=None, nb_down=None, nb_left=None):

        super().__init__(pos_x, pos_y, nb_up, nb_right, 
                nb_down, nb_left)
        self.levels = {Corner.TOP_L: 0,
                       Corner.TOP_R: 0,
                       Corner.BOT_L: 0,
                       Corner.BOT_R: 0}

    def set_levels(self, corners, level):
        """
        Set a list of corners to a common level. Call multiple 
        times if different levels are wanted.
        """
        if type(corners) is list:
            for corner in corners:
                self.levels[corner] = level
        elif type(corners) is Corner:
            self.levels[corners] = level

    def get_levels(self):
        """Return a list of corners that have a height > 0."""
        temp = []
        for key, value in self.levels.items():
            if value > 0:
                temp.append(key)
        return temp

    def get_level_corner(self, side):
        """
        Return the corner, if any, that belongs to parameter side
        and has a height > 0. In theory this could be two corners,
        but in practice it never should be.
        """
        corners = Side.convert_to_corner(side)
        for corner in corners:
            if self.levels[corner] > 0:
                return corner

    def is_flat(self):
        """
        Return whether this cell is flat or not (all levels 
        are the same).
        """
        w,x,y,z = self.levels.values()
        return w == x == y == z

    
