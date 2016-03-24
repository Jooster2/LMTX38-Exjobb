#Standard Modules
from random import sample

#Other Modules
from cell import Cell


def create_grid(size_x, size_y):
    grid = []
    for x in range(size_x):
        grid.append([])
        for y in range(size_y):
            grid[x].append(Cell(x, y))
            if x == 0:
                grid[x][y].make_outer_wall("LEFT")
            if y == 0:
                grid[x][y].make_outer_wall("DOWN")
            if x == size_x-1:
                grid[x][y].make_outer_wall("RIGHT")
            if y == size_y-1:
                grid[x][y].make_outer_wall("UP")
            # grid[i][j].print_info()
    return grid

def create_endpoints(grid, size_x, size_y):
    outer_cells = []
    for x in range(size_x):
        for y in range(size_y):
            #Check if x,y is on the border of the grid
            if x in (0, size_x-1) or y in (0, size_y-1):
                #If it is, save it as a tuple
                outer_cells.append((x, y))
    start_point, finish_point = sample(outer_cells, 2)
    grid[start_point[0]][start_point[1]].make_endpoint(True)
    grid[finish_point[0]][finish_point[1]].make_endpoint(False)
    return [grid, start_point, finish_point]
    

def maze_algorithm(grid, endpoints):
    sp, fp = endpoints

    current_cell = grid[sp[0]][sp[1]]
    directions = ["UP", "RIGHT", "DOWN", "LEFT"]
    
    while True:
        move_dir = sample(directions, 4)
        knocked_wall = knock_wall(move_dir)
        if knocked_wall == True:






if __name__ == "__main__":
    #size_x = input("X-size: ")
    #size_y = input("Y-size: ")
    size_x = 3
    size_y = 3
    grid = create_grid(size_x, size_y)
    grid, endpoints = create_endpoints(grid, size_x, size_y)
    for x in grid:
        for y in x:
            y.print_info()



    

