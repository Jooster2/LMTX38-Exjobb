



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

    def knock_wall(self, direction):
        try:
            self.walls[direction.upper()] = False
        except KeyError as e:
            print(e)

    def print_info(self):
        print("X: {} \nY: {}".format(self.pos_x, self.pos_y))

    def make_endpoint(self, is_start, direction):
        if is_start:
            self.is_start = True
        else:
            self.is_finish = True
        knock_wall(direction)

    def is_start(self):
        return self.is_start

    
