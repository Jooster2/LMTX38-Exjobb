"""
Testing functions for the Map Generator are here. They are run in serial at the bottom. 
All functions run for a number of iterations, specified by their only parameter. The 
standard argument to this parameter is a somewhat sane upper limit (time-wise).
"""

from contextlib import contextmanager
import os, sys

from mapgen import create_grid, create_endpoints
from cell import Cell, Side
from algorithm import generate_maze, find_solution

def outer_walls_test(iterations=50000):
    """Test that start and finish always have outer walls (are on the sides)"""
    x = 5
    y = 5
    i = 0
    while i < iterations:
        if i % 10000 == 0:
            print("Iteration: {}".format(i,)) 
        grid, outer_walled = create_grid(x,y)
        s_pt, f_pt = create_endpoints(outer_walled)
        assert s_pt.has_outer_walls() == True, "Start has no outer walls"
        assert f_pt.has_outer_walls() == True, "Finish has no outer walls"
        i += 1
    print("Outer walls test finished successfully, {} iterations".format(i,))

def solver_test(iterations=300):
    """Test that algorithms are always solvable, for many sizes."""
    x = 3
    y = 3
    i = 0
    size_change = True
    while i < iterations:
        if size_change:
            print("Size is currently: {}.{}".format(x, y))
            size_change = False
        with suppress_stdout():
            grid, outer_walled = create_grid(x,y)
            s_pt, f_pt = create_endpoints(outer_walled)
            generate_maze(grid, outer_walled, s_pt, f_pt)
            solution = find_solution(s_pt)
        assert solution != False, "Solution was False"
        assert solution[0] is s_pt, "Solution has faulty starting position"
        assert solution[-1] is f_pt, "Solution has faulty finish position"
        i += 1
        if i % 10 == 0:
            x += 1
            size_change = True
        if i % 15 == 0:
            y += 1
            size_change = True
    print("Find solution test finished successfully, {} iterations".format(i,))

@contextmanager
def suppress_stdout():
    """Used to suppress any unwanted output to console. This is used by the tests to stop any
       called method from cluttering the console, thus ensuring only test-relevant data is
       outputted."""
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

if __name__ == '__main__':
    """Call all testing methods here. Pass number of iterations as argument if desired."""
    outer_walls_test()
    solver_test()


