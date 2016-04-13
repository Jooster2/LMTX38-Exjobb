from cell import Cell
from directions import Side, Corner

class ActivatorCell(Cell):
    """An ActivatorCell is a Cell with additional data about activators."""
    
    def __init__(self, pos_x, pos_y,
            nb_up=None, nb_right=None, nb_down=None, nb_left=None):

        super().__init__(pos_x, pos_y, nb_up, nb_right, nb_down, nb_left)
        self.activators = {Corner.TOP_L: None,
                           Corner.TOP_R: None,
                           Corner.BOT_L: None,
                           Corner.BOT_R: None}

    def set_activator(self, corner, activator):
        """Place an Activator in a Corner."""
        self.activators[corner] = activator

    def get_activators(self):
        """Return all activators (no None)."""
        return [x for x in self.activators.values() \
                if x is not None] 



    


