from random import sample
from cell import Cell
from cell import Side





def create_grid(size_x, size_y):
    grid = []
    outer_walled = []
    for x in range(size_x):
        grid.append([])
        for y in range(size_y):
            cell = Cell(x, y)
            if x == 0:
                cell.make_outer_wall(Side.LEFT)
            if y == 0:
                cell.make_outer_wall(Side.UP)
            if x == size_x-1:
                cell.make_outer_wall(Side.RIGHT)
            if y == size_y-1:
                cell.make_outer_wall(Side.DOWN)
            grid[x].append(cell)
            if cell.has_outer_walls():
                outer_walled.append(cell)
    return [grid, outer_walled]


def create_endpoints(grid, outer_walled):
    s_point, f_point = sample(outer_walled, 2)
    s_point.is_start = True
    f_point.is_finish = True
    return (s_point, f_point)


def run_algorithm(grid, endpoints):
    visit_order = []
    s_point, f_point = endpoints
    current_cell = s_point
    visit_order.append(current_cell)

    while unvisited_cells_remaining(grid) > 0:
        #print("Visited cells: {}".format(visited_cells,))
        if unvisited_cells_remaining(grid) == 3:
            break
        side_list = Side.random_all()
        while len(side_list) > 0:
            direction = side_list.pop()
            coords = current_cell.get_neighbour_coords(direction)
            try:
                next_cell = grid[coords[0]][coords[1]]
                print("Attempting to create neighbour")
                if current_cell.make_neighbour(
                next_cell, direction):
                    visit_order.append(current_cell)
                    current_cell = next_cell
                    break
                
                elif len(visit_order) == 0 and len(side_list) > 1:
                    print("Attempting to force neighbour")
                    if current_cell.make_neighbour(
                    next_cell, direction, True):
                        visit_order.append(current_cell)
                        current_cell = next_cell
                        break
                
                elif len(visit_order) > 0 and len(side_list) == 0:
                    #print("Going backwards")
                    current_cell = visit_order.pop()

            except IndexError as e:
                print(e)
                #print("Grid index out of range, coords: ", coords)
                

def unvisited_cells_remaining(grid):
    number = 0
    for l in grid:
        for cell in l:
            if cell.is_not_visited():
                number += 1
    print("Cells remaining:",number)
    return number

if __name__ == '__main__':
    size_x = 5
    size_y = 5
    grid, outer_walled = create_grid(size_x, size_y)
    endpoints = create_endpoints(grid, outer_walled)
    run_algorithm(grid, endpoints)
    for x in grid:
        for y in x:
            print(y)




        
