from activator import Activator

class ButtonActivator(Activator):
    """A Button"""

    def __init__(self, pos_x, pos_y,
            nb_up=None, nb_right=None, nb_down=None, nb_left=None,
            continuous_needed=False, *a_req = Activator.all_cars):
        """
        A default button does not need continuous pressing, and
        can be activated by any car.
        """

        super().__init__(pos_x,pos_y,
            np_up,nb_right,nb_down,nb_left,
            continuous_needed, a_req)

