from enum import IntEnum
from random import randrange, sample

class Side(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def opposite(side):
        if side is Side.UP: 
            return Side.DOWN
        elif side is Side.DOWN: 
            return Side.UP
        elif side is Side.RIGHT:
            return Side.LEFT
        elif side is Side.LEFT:
            return Side.RIGHT

    def convert(number):
        if type(number) is Side:
            return {Side.UP: 0,
                    Side.RIGHT: 1,
                    Side.DOWN: 2,
                    Side.LEFT: 3}[number]
        elif type(number) is int:
            return {0: Side.UP,
                    1: Side.RIGHT,
                    2: Side.DOWN,
                    3: Side.LEFT}[number]
        else:
            return None

    def biased_random(side_1, side_2, side_3=None, side_4=None,
            p_1=1, p_2=1, p_3=0, p_4=0):
        interval_1 = range(p_1)
        pool = p_1
        interval_2 = range(pool, pool+p_2)
        pool += p_2
        interval_3 = range(pool, pool+p_3)
        pool += p_3
        interval_4 = range(pool, pool+p_4)
        pool += p_4
        choice = randrange(pool)
        if choice in interval_1:
            return side_1
        elif choice in interval_2:
            return side_2
        elif choice in interval_3:
            return side_3
        elif choice in interval_4:
            return side_4

        
    def random_all():
        return sample(list(Side), 4)


    def convert_sides(x, y):
        res = []
        if x < 0:
            res.append(Side.LEFT)
        else:
            res.append(Side.RIGHT)
        if y < 0:
            res.append(Side.UP)
        else:
            res.append(Side.DOWN)
        return res


class Partition(IntEnum):
    """
    Parted Cell uses Partitions to keep track of it's internal
    "storage".
    """
    TOP_R = 0
    BOT_R = 1
    BOT_L = 2
    TOP_L = 3

    
