from random import sample, randint, choice
from copy import copy
from cmath import sqrt
from math import ceil

from cell import Cell
from leveled_cell import LeveledCell
from activator_cell import ActivatorCell
from complex_cell import ComplexCell
from directions import Side, Corner
from algorithm import Branch
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
        print("Branch-len1:",len(branches))
        branches.remove(self.top_branch)
        print("Branch-len2:",len(branches))

        
        # Choose up to a third of the branches for levels.
        chosen_branches = sample(branches, 
                randint(1, int(len(branches)/3)))

        for branch in chosen_branches:
            if len(branch.cells) <= 2:
                continue
            start = choice(branch.cells[:int(len(branch.cells)/2)])
            cells_to_start = branch.cells.index(start)+1
            length = randint(2, len(branch.cells) - \
                    cells_to_start)
            goal_height = randint(1, min(3, cells_to_start))
            height = 1

            chosen_cells = branch.cells[cells_to_start: \
                    cells_to_start + length]
            leveled_cells = self.to_leveled(chosen_cells, branch)

            for idx, cell in enumerate(leveled_cells):

                # Get previous and next cells.
                if idx > 0:
                    prev = leveled_cells[idx-1]
                if idx+1 < len(leveled_cells):
                    nxt = leveled_cells[idx+1]

                if idx == 0:
                    # First cell special case.
                    next_side = cell.get_side(nxt)
                    corner = choice(Side.convert_to_corner(next_side))
                    cell.set_levels(corner, height)

                elif idx == len(leveled_cells)-1:
                    # Last cell special case.
                    prev_side = cell.get_side(prev)
                    # TODO fill in with some randomized ending.

                else:
                    # All cells between first and last.
                    prev_side = cell.get_side(prev)
                    next_side = cell.get_side(nxt)
                    prev_corner = prev.get_level_corner( \
                            Side.opposite(prev_side))
                    if next_side is Side.opposite(prev_side):
                        # If we are going straight across this cell.
                        # Get the first corner.
                        corners = [Corner.neighbour_single( \
                                prev_corner, prev_side)]
                        # Get the second corner.
                        corners.append(Corner.neighbour_single( \
                                corners[0], next_side))

                        # Check that no path is cut of with levels.
                        broken_walls = cell.get_walls(intact=False)
                        if len(broken_walls) > 2:
                            # This is a three or four way crossing.
                            broken_walls.remove(next_side)
                            broken_walls.remove(prev_side)
                            if Corner.convert_to_side(corners) in \
                                    broken_walls:
                                break
                        # Make levels.
                        cell.set_levels(corners, height)

                    elif prev_corner in Side.convert_to_corner(next_side):
                        # If we are doing an "inner" turn.
                        corner = Corner.neighbour_single(prev_corner, next_side)
                        cell.set_levels(corner, height)

                    else:
                        # Check that no path is cut of with levels.
                        if len(cell.get_walls(intact=False)) > 2:
                            break
                        # If we are doing an "outer" turn.
                        # Get all corners.
                        corners = list(Corner)
                        # Remove the one that is not part of the turn.
                        good_corner = Corner.neighbour_single( \
                                prev_corner, prev_side)
                        bad_corners = Side.convert_to_corner(prev_side)
                        bad_corners.remove(good_corner)
                        corners.remove(bad_corners[0])


                        cell.set_levels(corners, height)

                # TODO Height incrementation should maybe be smarter.
                if height < goal_height:
                    height += 1
                                 
                

    def to_leveled(self, chosen_cells, branch):
        """Remake cells in list into LeveledCells."""
        leveled_cells = []
        for cell in chosen_cells:
            lvl_cell = LeveledCell(0,0)
            lvl_cell.transmute(cell)
            branch.cells[branch.cells.index(cell)] = lvl_cell
            leveled_cells.append(lvl_cell)
            self.grid[cell.pos_x][cell.pos_y] = lvl_cell
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

        





