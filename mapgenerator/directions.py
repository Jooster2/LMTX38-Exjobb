from enum import IntEnum
from random import randrange, sample

class Side(IntEnum):
    """
    Sides are used by Cells to keep track of neighbours and walls.
    """
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def opposite(side):
        """Return the Side opposite of the argument side."""
        if side is Side.UP: 
            return Side.DOWN
        elif side is Side.DOWN: 
            return Side.UP
        elif side is Side.RIGHT:
            return Side.LEFT
        elif side is Side.LEFT:
            return Side.RIGHT

    def convert(number):
        """
        Convert back and forth between a Side and an integer 0-3.
        """
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
        """
        Return a Side, chosen with biased random.
        Set the sides corresponding p-values to some value, that 
        is relative to the other sides p-value.
        Example:
            p_1 = 5, p_2 = 2, means there is a 5:2 ratio, or 
            ~71.4% chance, that side_1 is returned.
        """
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
        """Return a list of all four Sides, in random order."""
        return sample(list(Side), 4)


    def convert_sides(x, y):
        """Convert two integers to a Side."""
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

    def convert_to_corner(side):
        """
        Return a tuple of Corners that together form the given 
        Side.
        """
        if side is Side.UP:
            return (Corner.TOP_R, Corner.TOP_L)
        elif side is Side.RIGHT:
            return (Corner.TOP_R, Corner.BOT_R)
        elif side is Side.DOWN:
            return (Corner.BOT_L, Corner.BOT_R)
        elif side is Side.LEFT:
            return (Corner.TOP_L, Corner.BOT_L)


class Corner(IntEnum):
    """
    Corners are like Sides, but they keep track of the quadrants.
    """
    TOP_R = 0
    BOT_R = 1
    BOT_L = 2
    TOP_L = 3

    
    def convert_to_side(corners: tuple):
        """
        Return a Side if the two corners are next to each other, 
        otherwise None.
        """
        if set(corners).issubset(Side.convert_to_corner(Side.UP)):
            return Side.UP
        elif set(corners).issubset(Side.convert_to_corner(
            Side.RIGHT)):
            return Side.RIGHT
        elif set(corners).issubset(Side.convert_to_corner(
            Side.DOWN)):
            return Side.DOWN
        elif set(corners).issubset(Side.convert_to_corner(
            Side.LEFT)):
            return Side.LEFT
        
    def random_all():
        """Return a list of all four Corners, in random order."""
        return sample(list(Corner), 4)



