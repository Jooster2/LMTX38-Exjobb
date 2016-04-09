from activator import Activator

class ButtonActivator(Activator):
    """A Button"""

    def __init__(self, continuous_needed=False, *a_req = Activator.all_cars):
        """
        A default button does not need continuous pressing, and
        can be activated by any car.
        """

        super().__init__(continuous_needed, a_req)

