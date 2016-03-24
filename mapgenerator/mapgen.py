from random import sample

from cell import Cell
from cell import Side


def create_grid(size_x, size_y):
    grid = []
    outer_walled = []
    for x in range(size_x):
        grid.append([])
        for y in range(size_y):
            if x > 0:
                prev_x_cell = grid[x-1][y]
            if y > 0:
                prev_y_cell = grid[x][y-1]
            cell = Cell(x, y, prev_y_cell, None, None, prev_x_cell)
            try:
                prev_x_cell.set_neighbour(cell, Side.RIGHT)
            except:
                pass
            try:
                prev_y_cell.set_neighbour(cell, Side.UP)
            except:
                pass
            if x == 0: 
                cell.add_outer_wall(Side.LEFT)
            if x == size_x-1:
                cell.add_outer_wall(Side.RIGHT)
            if y == 0:
                cell.add_outer_wall(Side.UP)
            if y == size_y:
                cell.add_outer_wall(Side.DOWN)
            if cell.has_outer_walls:
                outer_walled.append(cell)

            grid.append(cell)
    return [grid, outer_walled]



if __name__ == '__main__':
    size_x = 5
    size_y = 5

