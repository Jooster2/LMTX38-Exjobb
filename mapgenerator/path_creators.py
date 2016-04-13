from random import sample, choice
from copy import copy
from cmath import sqrt
from math import ceil

from cell import Cell
from directions import Side
from branch import Branch

def cells_remaining(grid):
    """
    Return the number of cells in the grid that have all
    four walls intact.
    """
    number = 0
    for vertical in grid:
        for cell in vertical:
            if cell.is_not_visited():
                number += 1
    return number


def path_length_maximum(grid):
    """
    Calculate the maximum length of each path the algorithm takes
    before resetting to a cell in the solution list. 
    This is the minimum required to have enough "steps available"
    to visit all the cells. 
    """
    
    # Calculate the solutions minimum length.
    # See mapgen.create_endpoints() for explanation of what this is.
    sol_min_dist = int(abs(sqrt(len(grid)*2+(len(grid[0])-2)*2)))
    
    """
    The amount of cells, minus the minimum the solution has visited,
    gives the remaining cells to visit. Each branch can extend for
    up to two 'lengths' from each of the solution's cells.
    """
    path_length_max = (len(grid)*len(grid[0]) - sol_min_dist) / \
                        (2*sol_min_dist)
    path_length_max = int(ceil(path_length_max))
    return path_length_max



def depth_first(grid, s_pt, visited_cells):
    """
    Start at s_pt, and knock down walls in a depth-first search.
    Only stop when all cells in the grid have been visited.
    Third argument, visited_cells, is optional, but can be used
    to inform DFS on the previously visited cells.
    """

    path_to_finish = copy(visited_cells) 
    dead_ends = []
    running_dead_ends = False
    path_length = 0
    path_length_max = path_length_maximum(grid)
    branches = []

    if len(visited_cells) > 0:
        print("Given a list of cells as argument,", \
                "starting from one of them")
        current_cell = choice(visited_cells)
        branches.append(Branch(visited_cells, None))
    else:
        current_cell = s_pt
    parent = current_cell
    print("Starting algorithm\nNumber of cells remaining: ", end="")

    while cells_remaining(grid):
        print(cells_remaining(grid), end=", ")

        if path_length >= path_length_max:
            dead_ends.append(current_cell)
            new_branch.append(current_cell) 
            branches.append(Branch(new_branch, parent))
            if path_to_finish:
                # If there are still cells in the solution we 
                # haven't visited.
                current_cell = choice(path_to_finish)
                path_to_finish.remove(current_cell)
            else:
                # If all cells in the solution have been visited, we
                # restart at the ends of previous branches.
                current_cell = dead_ends.pop(0)
            path_length = 0
            parent = current_cell
            new_branch = []

        for side in Side.random_all():
            if current_cell.get_neighbour(side).is_not_visited():
                visited_cells.append(current_cell)
                current_cell.knock_wall(side)
                current_cell = current_cell.get_neighbour(side)
                new_branch.append(current_cell)
                path_length += 1
                break
            
        # If there were no unvisited cells on any side
        else:
            try:
                # Backtrack one step, and remove cell from solution
                current_cell = visited_cells.pop()
            except IndexError as e:
                print(e)
                path_length = path_length_max

    return branches

def path_to_finish(grid, s_pt, f_pt, visited_cells=[]):
    """
    Find a straightforward path from start to finish. Some randomization included,
    but not much.
    NOTE: 
        This algorithm does not visit all cells, it only finds the straighest path 
        from start to finish. Combine it with other algorithms to make a complete maze.
    """
    path_x, path_y = s_pt.calc_steps(f_pt)
    print("PathX: {}, PathY: {}".format(path_x, path_y))
    if abs(path_x) == abs(path_y):
        m_p, s_p = sample((path_x, path_y), 2)
    else:
        m_p = max(abs(path_x), abs(path_y))
        if abs(m_p) == abs(path_x):
            m_p = path_x
            s_p = path_y
            print("X is main")
        else:
            m_p = path_y
            s_p = path_x
            print("Y is main")

    if m_p == path_x:
        main_side, sec_side = Side.convert_sides(path_x, path_y)
    else:
        sec_side, main_side = Side.convert_sides(path_x, path_y)

    print("Main side: {}, Secondary side: {}".format(main_side.name, sec_side.name))
    current_cell = s_pt
    print(current_cell)
    while current_cell is not f_pt:
        distance = current_cell.distance_to(f_pt)
        #for side in Side.biased_random(main_side, sec_side, p_1=5):
        
        side = Side.biased_random(main_side, sec_side, p_1=5)
        if current_cell.get_neighbour(side).distance_to(f_pt) > distance:
            if side is main_side:
                side = sec_side
            else:
                side = main_side
        if current_cell.get_neighbour(side).is_not_visited():
            visited_cells.append(current_cell)
            current_cell.knock_wall(side)
            current_cell = current_cell.get_neighbour(side)
            print(current_cell)

    return visited_cells









