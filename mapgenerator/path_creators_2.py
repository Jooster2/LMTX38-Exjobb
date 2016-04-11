from random import sample, choice
from copy import copy
from cmath import sqrt
from math import ceil

from cell import Cell
from leveled_cell import LeveledCell
from activator_cell import ActivatorCell
from complex_cell import ComplexCell
from directions import Side, Corner




def module_placer(grid, path, modules):
    """
    Place modules along a path.

    grid -- the maze grid
    path -- list of cells that have been chosen to eventually get a module
    modules -- dict of available modules
    """

    # First choose a spot on the path, where we should put a module.
    for cell in path:
        # Special case when dealing with the main path (contains finish point).
        if cell.is_finish:
            placement = cell
            break
    else:
        placement = choice(path)

    # Choose a random module type, and make sure the dictionary is kept clean.
    module = choice(modules.keys())
    modules[module] -= 1
    if modules[module] <= 0:
        del modules[module]

    # Replace the chosen cell with a new module
    mod = module(0,0)
    mod.transmute(placement)
    grid[mod.pos_x][mod.pos_y] = mod
    
    return mod


def activator_placer(grid, main_path, mod, activators, amount = (1, 3)):
    """
    Place activators anywhere in the grid not behind a module.
    
    grid -- the maze grid
    main_path -- the path from start to finish
    mod -- the module that will get activators
    activators -- dict of available activators
    amount -- tuple with a minimum and maximum of activators to place
    """

    for cell in reversed(main_path):
       


    




