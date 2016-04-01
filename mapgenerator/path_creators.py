from random import sample
from cell import Cell, Side

def cells_remaining(grid):
    """Return the number of cells in the grid that have all
       four walls intact."""
    number = 0
    for vertical in grid:
        for cell in vertical:
            if cell.is_not_visited():
                number += 1
    return number



def depth_first(grid, s_pt, visited_cells=[]):
    """Start at s_pt, and knock down walls in a depth-first search.
       Only stop when all cells in the grid have been visited."""
    current_cell = s_pt
    print("Starting algorithm\nNumber of cells remaining: ", end="")
    while cells_remaining(grid):
        print(cells_remaining(grid), end=", ")
        for side in Side.random_all():
            if current_cell.get_neighbour(side).is_not_visited():
                visited_cells.append(current_cell)
                current_cell.knock_wall(side)
                current_cell = current_cell.get_neighbour(side)
                break
            
        # If there were no unvisited cells on any side
        else:
            try:
                # Backtrack one step, and remove cell from solution
                current_cell = visited_cells.pop()
            except IndexError as e:
                print(e)

def path_finish_first(grid, s_pt, f_pt, visited_cells=[]):
    path_x, path_y = s_pt.calc_steps(f_pt)
    if abs(path_x) == abs(path_y):
        m_p, s_p = sample((path_x, path_y), 2)
    else:
        m_p = max(abs(path_x), abs(path_y))
        if abs(m_p) == abs(path_x):
            m_p = path_x
            s_p = path_y
        else:
            m_p = path_y
            s_p = path_x

    if m_p == path_x:
        main_side, sec_side = Side.convert_sides(path_x, path_y)
    else:
        sec_side, main_side = Side.convert_sides(path_x, path_y)

    current_cell = s_pt
    while True:
        if current_cell == f_pt:
            break
        for side in Side.biased_random(main_side, sec_side):
            if current_cell.get_neighbour(side).is_not_visited():
                visited_cells.append(current_cell)
                current_cell.knock_wall(side)
                current_cell = current_cell.get_neighbour(side)
                break

    return visited_cells









