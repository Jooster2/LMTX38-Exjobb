#Standard Modules
from random import random

#Other Modules
from cell import Cell


def create_grid(size_x, size_y):
    grid = []
    for x in range(size_x):
        grid.append([])
        for y in range(size_y):
            grid[i].append(Cell(x, y))
            grid[i][j].print_info()
    return grid

def create_endpoints(grid, size_x, size_y):
    outer_cells = []
    for x in range(size_x):
        for y in range(size_y):
            #Check if x,y is on the border of the grid
            if x in (0, size_x-1) || y in (0, size_y-1):
                #If it is, save it as a tuple
                outer_cells.append((x, y))
    start_point, finish_point = random.sample(outer_cells, 2)
    
    



if __name__ == "__main__":
    #size_x = input("X-size: ")
    #size_y = input("Y-size: ")
    size_x = 3
    size_y = 3
    grid = create_grid(size_x, size_y)



    

