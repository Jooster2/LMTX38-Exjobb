from module import Module
from side import Side

class DoorModule(Module):
    """
    DoorModule is a door that can be either open or closed. 
    """
 
    def __init__(self, pos_x, pos_y,
            nb_up=None, nb_right=None, nb_down=None, nb_left=None,
            facing, *activators):

        super().__init__(pos_x,pos_y,
            np_up,nb_right,nb_down,nb_left,
            facing, *activators)



