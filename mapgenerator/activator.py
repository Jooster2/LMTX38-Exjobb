from car import Car

class Activator:
    """
    An Activator is any item that the cars can interface with to
    activate a Module. This is a base class for all activators.
    NOTE:
        It is not abstract (because abstract classes and methods 
        are strange in python), but it should never be instantiated.
    """
    all_cars = [Car.BIG, Car.CAM, Car.GRAB]
    
    def __init__(self, module, *a_req, continuous_needed=False):
        """
        continuous_needed -- whether the activator resets on release
        module -- the module that this activator binds to
        *a_req -- a list of cars that can use the activator
        """

        self.continuous_needed = continuous_needed
        self.module = module
        self.possible_cars = []
        self.possible_cars.extend(a_req)
        self.active = False
        module.add_activators(self)


    def activate(self, unit):
        """
        Attempt to activate this activator with unit.
        unit -- a car attempting to activate
        """
        if unit in self.possible_cars:
            self.active = True

    def deactivate(self):
        """Attempt to deactivate this activator."""
        if self.continuous_needed:
            self.active = False

    def is_active(self):
        """Return whether this activator is active or not."""
        return self.active
        
