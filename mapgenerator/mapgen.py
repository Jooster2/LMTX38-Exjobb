from random import sample
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from cmath import sqrt

from cell import Cell
from directions import Side
from algorithm import generate_maze, find_solution
from graphical import create_cell_images, display
from car import Car
from door_module import DoorModule
from button_act import ButtonActivator
from puzzle_maker import PuzzleMaker


def create_grid(size_x, size_y):
    """
    Create a grid of size_x * size_y, and fill it with Cells. All 
    Cells added to the grid knows about their respective neighbours.
    Returns both the grid, and a list of all Cells that have outer 
    walls (i.e. those who do not have neighbours on all sides).
    """
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
            cell = Cell(x, y, nb_up=prev_y, nb_left=prev_x)
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
    """
    Mark two Cells as start point and finish point respectively, 
    randomly chosen out of the list supplied as parameter.
    """
    distance = 0
    min_distance_allowed = int(abs(sqrt(len(outer_walled))))
    while distance < min_distance_allowed:
        s_pt, f_pt = sample(outer_walled, 2)
        distance = s_pt.distance_to(f_pt)
    s_pt.is_start = True
    f_pt.is_finish = True
    return [s_pt, f_pt]



if __name__ == '__main__':
    size_x = 8
    size_y = 8
    grid, outer_walled = create_grid(size_x, size_y)
    s_pt, f_pt = create_endpoints(outer_walled)
    branch = generate_maze(grid, s_pt, f_pt)
    puzzle_maker = PuzzleMaker(grid, branch, None, None)
    puzzle_maker.make_levels()

    print("Starting solving algorithm")
    solution = find_solution(s_pt)
    if solution:
        img_grid = create_cell_images(grid, solution)
        display(img_grid)
        print("Solving algorithm finished successfully")
        for cell in solution:
            if cell.is_start:
                print("{}, is start".format(cell.coords(),))
            elif cell.is_finish:
                print("{}, is finish".format(cell.coords(),))
            else:
                print(cell.coords())
    else:
        print("Failed to solve maze, algorithm has produced \
                impossible maze")

