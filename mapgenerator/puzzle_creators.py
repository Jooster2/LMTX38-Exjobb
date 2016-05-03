from random import sample, randint, choice
from copy import copy
from cmath import sqrt
from math import ceil

from cell import Cell
from leveled_cell import LeveledCell
from activator_cell import ActivatorCell
from complex_cell import ComplexCell
from directions import Side, Corner
from algorithms import Branch
from car import Car


class PuzzleMaker:
    """PuzzleMaker creates puzzles of all kinds on the map."""

    def __init__(self, grid, branch, modules, activators):
        """
        Constructor

        grid -- the map grid
        branch -- the top branch (from visit_complete)
        modules -- dict with module-class-objects as keys and 
        amount as value
        activators -- dict with activator-class-objects as keys
        and amount as value
        """

        self.grid = grid
        self.top_branch = branch
        self.modules = modules
        self.activators = activators

        # Dict of cars to keep track of which is in use.
        self.cars = {Car.BIG: False,
                     Car.CAM: False,
                     Car.GRAB: False}

    def make_levels(self):
        """Create levels on some branches."""

        # Get all branches except for the top.
        branches = self.top_branch.get_basic_tree()
        branches.remove(self.top_branch)
        
        # Choose up to a third of the branches for levels.
        chosen_branches = sample(branches, 
                randint(len(branches)/3))

        for branch in chosen_branches:
            start = choice(branch.cells)
            cells_to_start = branch.cells.index(start)
            length = randint(1, len(branch.cells) - \
                    cells_to_start)
            height = randint(1, min(3, cells_to_start))
            start_height = 1

            chosen_cells = branch.cells[branch.cells.index(start):]
            leveled_cells = self.to_leveled(chosen_cells, branch)

            for idx, cell in enumerate(leveled_cells):
                if idx > 0:
                    prev = leveled_cells[idx-1]
                if idx < len(leveled_cells):
                    nxt = leveled_cells[idx+1]

                if idx == 0:
                    side = cell.get_side(nxt)
                    corner = choice(Side.convert_to_corner(side))
                    cell.set_levels(corner, start_height)
                    start_height += 1

                else:
                    prev_side = cell.get_side(prev)
                    next_side = cell.get_side(nxt)
                    if next_side is Side.opposite(prev_side):







                

    def to_leveled(self, chosen_cells, branch):
        """Remake cells in list into LeveledCells."""
        leveled_cells = []
        for cell in chosen_cells:
            lvl_cell = LeveledCell(0,0)
            lvl_cell.transmute(cell)
            branch.cells[branch.cells.index(cell)] = lvl_cell
            leveled_cells.append(lvl_cell)
        return leveled_cells


    def make_puzzles(self):
        """
        Place modules and activators in the grid, in such a way that
        they don't block each other. The rules of placement are as
        follows:
            1. an activator must not be placed behind the module 
            it's connected to.
            2. an activator must not be placed in any of the 
            branches that are located behind the module it's 
            connected to.
            3. for every branch found when checking 2, if there are
            other activators in there, rule 2 must be run on the
            modules these other activators are connected to, and the
            new module may not be placed in any of those branches 
            either.
        Rule 1 is a subset of rule 2 is a subset of rule 3.
        """
        branch = self.top_branch
        while modules and activators:
            module = self.place_module(branch)
            activators = self.place_activators(module, branch)


    def place_module(self, branch):
        """Place modules in a branch."""

        # First choose a spot on the path, for module placement.
        for cell in branch.cells:
            # Special case when dealing with the main path 
            # (contains finish point).
            if cell.is_finish:
                placement = cell
                break
        else:
            placement = choice(branch.cells)

        # Choose a random module type, and make sure the dictionary 
        # is kept clean.
        module = choice(modules.keys())
        modules[module] -= 1
        if modules[module] <= 0:
            del modules[module]

        # Replace the chosen cell with a new module
        mod = module(0,0)
        mod.transmute(placement)
        grid[mod.pos_x][mod.pos_y] = mod
        
        return mod


    def place_activators(mod, branch, amount=(1,3)):
        """
        Place activators anywhere in the grid not behind a module.
        
        mod -- the module that will get activators
        branch -- the branch the module is located in
        amount -- tuple with a minimum and maximum of activators 
        to place
        """

        





