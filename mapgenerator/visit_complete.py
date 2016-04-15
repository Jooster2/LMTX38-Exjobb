from copy import copy
from random import choice

from directions import Side
from cell import Cell
from branch import Branch
from path_creators import path_length_maximum, cells_remaining


def visit_complete(grid, visited_cells):
    """
    Generate a maze out of all the remaining cells in the grid.
    This generator has built-in bias towards generating many
    branches with similar length.
    See path_creators.path_length_maximum for explanation on how
    the preferred length is determined.
    Requires input from a completed PTF to run.
    Return the top of the tree.
    """

    b_name = 0
    top_branch = Branch(None, b_name)
    b_name += 1
    top_branch.cells = list(visited_cells)
    
    current_cell = choice(visited_cells)
    current_branch, b_name = new_branch(current_cell, top_branch, \
            b_name)
    path_length_max = path_length_maximum(grid)

    print("Starting algorithm\nNumber of cells remaining: ",end="")
    while cells_remaining(grid):
        print(cells_remaining(grid), end=", ")
        if len(current_branch.cells) >= path_length_max and \
                top_branch.childless_cells():
            # Limit the length of branches
            current_cell = choice(top_branch.childless_cells())
            current_branch, b_name = new_branch(current_cell, \
                    top_branch, b_name)

        for side in Side.random_all():
            if current_cell.get_neighbour(side).is_not_visited():
                print("Knocking wall")
                current_cell.knock_wall(side)
                current_cell = current_cell.get_neighbour(side)
                current_branch.cells.append(current_cell)
                break

        else:
            current_cell = current_branch.prev(current_cell)
            if not current_cell:
                current_cell = current_branch.get_parent()
                if current_cell:
                    current_branch = top_branch.find(current_cell)
                else:
                    current_cell, current_branch, b_name = \
                            find_sane(b_name, top_branch)

            if current_cell.has_unvisited_neighbours():
                current_branch, b_name = new_branch(current_cell, \
                        current_branch, b_name)
    return top_branch

def find_sane(b_name, top_branch):
    """Find a branch by name, used when all else fails."""
    do = True
    while do:
        b_name -= 1
        print("Branch_name out:",b_name)
        current_branch = top_branch.get_by_name(b_name)
        if len(current_branch.cells) > 0:
            do = False
    current_cell = current_branch.cells[-1]
    return (current_cell, current_branch, b_name)

def new_branch(parent_cell, parent_branch, b_name):
    """Create and link a new branch."""
    next_branch = Branch(parent_cell, b_name)
    parent_branch.add_branch(next_branch)
    b_name += 1
    return (next_branch, b_name)


