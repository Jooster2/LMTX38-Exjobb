from leveled_cell import LeveledCell
from activator_cell import ActivatorCell

class ComplexCell(LeveledCell, ActivatorCell):
    """A ComplexCell is a Cell with both levels and Activators."""

    
    def __init__(self, pos_x, pos_y,
            nb_up=None, nb_right=None, nb_down=None, nb_left=None):

        super().__init__(pos_x, pos_y, nb_up, nb_right, nb_down, nb_left)

