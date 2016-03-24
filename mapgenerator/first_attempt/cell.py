



class Cell:
    """A cell is a square in the map-grid"""
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.walls = {"UP" : True,
                      "RIGHT" : True,
                      "DOWN" : True,
                      "LEFT" : True }
        self.is_start = False
        self.is_finish = False
        self.visited = False
        self.outer_walls = []

    def make_outer_wall(self, direction):
        self.outer_walls.append(direction)
        self.knock_wall(direction)

    def visit(self, from_dir):
        self.visited = True
        self.knock_wall(from_dir)
        

    def knock_wall(self, direction):
        """Knock down the wall in specified direction.
            Return True if there was a valid wall to 
            knock down."""
        try:
            if self.walls[direction.upper()] == True and
            direction.upper() not in self.outer_walls:
                self.walls[direction.upper()] = False
                return True
            else:
                return False
        except KeyError as e:
            print(e)

    def print_info(self):
        print("X: {} Y: {} {}".format(self.pos_x, self.pos_y,
            self.is_start or self.is_finish))
                

    def make_endpoint(self, is_start):
        if is_start:
            self.is_start = True
        else:
            self.is_finish = True
        self.knock_wall(self.outer_wall)

    def is_start(self):
        return self.is_start

    
