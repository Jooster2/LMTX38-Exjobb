from cell import Cell
from directions import Side

class Module(Cell):
    """
    Module is a base class for all different modules. 
    NOTE:
        It is not abstract (because abstract classes and methods 
        are strange in python), but it should never be instantiated.
    """
    
    def __init__(self, pos_x, pos_y,
            nb_up=None, nb_right=None, nb_down=None, nb_left=None,
            facing, *activators):
        """
        facing -- a side that should be the modules front
        *activators -- a list of relevant activators
        """

        super().__init__(pos_x,pos_y,
            np_up,nb_right,nb_down,nb_left)

        if self.walls[facing] == True:
            raise ValueError("Wall in the way of module facing")
        else:
            self.facing = facing
            self.activators = []
            self.activators.extend(activators)

            

    def is_crossable(self):
        """Return whether the module can be driven over or not."""
        return self.check_activators()

    def set_facing_side(self, side):
        """
        Tell the module which way it should face itself. The side
        faced is always the front, i.e. the side the cars should
        be coming from.
        """
        if self.walls[side] == True:
            return False
        else:
            self.facing = side

    def add_activators(self, *activators):
        """Add any number of activators for this module."""
        self.activators = []
        self.activators.extend(activators)

    def check_activators(self):
        """
        Returns whether all activators are activated or not. Use
        this to check if the module should activate.
        """
        return all(x is True for x in self.activators.is_active())
