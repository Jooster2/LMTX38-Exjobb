from random import sample

from cell import Cell
from cell import Side
from algorithm import generate_maze
from algorithm import find_solution


def create_grid(size_x, size_y):
    grid = []
    outer_walled = []
    for x in range(size_x):
        grid.append([])
        for y in range(size_y):
            prev_x = None
            prev_y = None
            if x > 0:
                prev_x = grid[x-1][y]
            if y > 0:
                prev_y = grid[x][y-1]
            cell = Cell(x, y, np_up=prev_y, nb_left=prev_x)
            try:
                prev_x.set_neighbour(cell, Side.RIGHT)
            except:
                pass
            try:
                prev_y.set_neighbour(cell, Side.DOWN)
            except:
                pass
            if x == 0: 
                cell.add_outer_wall(Side.LEFT)
            if x == size_x-1:
                cell.add_outer_wall(Side.RIGHT)
            if y == 0:
                cell.add_outer_wall(Side.UP)
            if y == size_y-1:
                cell.add_outer_wall(Side.DOWN)
            if cell.has_outer_walls():
                outer_walled.append(cell)

            grid[x].append(cell)
    return [grid, outer_walled]

def create_endpoints(outer_walled):
    is_neighbour = True
    while is_neighbour:
        s_pt, f_pt = sample(outer_walled, 2)
        is_neighbour = s_pt.is_neighbour(f_pt)
    s_pt.is_start = True
    f_pt.is_finish = True
    return [s_pt, f_pt]



if __name__ == '__main__':
    size_x = 5
    size_y = 5
    grid, outer_walled = create_grid(size_x, size_y)
    s_pt, f_pt = create_endpoints(outer_walled)
    grid = generate_maze(grid, outer_walled, s_pt, f_pt)
    print(s_pt)
    
    print("Starting solving algorithm")
    solution = find_solution(s_pt)
    if solution:
        print("Solving algorithm finished successfully")
        for cell in solution:
            if cell.is_start:
                print("{}, is start".format(cell.coords(),))
            elif cell.is_finish:
                print("{}, is finish".format(cell.coords(),))
            else:
                print(cell.coords())
    else:
        print("Failed to solve maze, algorithm has produced impossible maze")

    """The following has never produced output (ie, there are no
       unvisited cells).
    for x in grid:
        for y in x:
            if y.is_not_visited():
                print("I have not been visited", y)
                """

    """print("Solution is as follows:")
    for cell in solution:
        if cell.is_start:
            print(cell.coords(), "Is start")
        elif cell.is_finish:
            print(cell.coords(), "Is finish")
        else:
            print(cell.coords())
   """ 

