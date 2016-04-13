from copy import copy
from random import choice

from directions import Side
from cell import Cell
from branch import Branch
from path_creators import path_length_maximum, cells_remaining


def permeate_grid(grid, visited_cells):
    """
    Depth-first search v2.0
    This version does not work without PTF.
    """

    path_to_finish = copy(visited_cells)
    top_branch = Branch(None)
    top_branch.cells = path_to_finish
    
    current_cell = choice(visited_cells)
    path_to_finish.remove(current_cell)
    current_branch = Branch(current_cell)
    top_branch.add_branch(current_branch)
    path_length_max = path_length_maximum(grid)


    print("Starting algorithm\nNumber of cells remaining: ", end="")
    while cells_remaining(grid):
        #print(cells_remaining(grid), end=", ")

        for side in Side.random_all():
            if current_cell.get_neighbour(side).is_not_visited():
                if current_cell in current_branch.cells:
                    next_branch = Branch(current_cell)
                    current_branch.add_branch(next_branch)
                    current_branch = next_branch
                    print("Diving into new branch")
                current_cell.knock_wall(side)
                current_cell = current_cell.get_neighbour(side)
                current_branch.cells.append(current_cell)
                break

        else:
            try:
                current_cell = current_branch.prev(current_cell)
                print("Moving backwards once")
            except IndexError:
                if current_branch is top_branch:
                    path_to_finish.remove(current_cell)
                    current_cell = choice(path_to_finish)
                else:
                    current_cell = current_branch.parent
                    current_branch = top_branch.find(current_cell)
                    print("Moving up one branch")

    return top_branch



