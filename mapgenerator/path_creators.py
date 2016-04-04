from random import sample, choice
from cell import Cell
from directions import Side

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



def depth_first(grid, s_pt, visited_cells):
    """
    Start at s_pt, and knock down walls in a depth-first search.
    Only stop when all cells in the grid have been visited.
    Third argument, visited_cells, is optional, but can be used
    to inform DFS on the previously visited cells.
    """
    if len(visited_cells) > 0:
        print("Given a list of cells as argument,", \
                "starting from one of them")
        current_cell = choice(visited_cells)
    else:
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









