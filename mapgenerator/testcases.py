"""
Testing functions for the Map Generator are here. They are run according to command line 
arguments. All tests run for a specified number of iterations, but also have a fairly sane
standard argument.
"""

from contextlib import contextmanager
import os, sys

from mapgen import create_grid, create_endpoints
from cell import Cell, Side
from algorithm import generate_maze, find_solution



def outer_walls_test(iterations=50000):
    """
    Test that start and finish always have outer walls (are on the sides).
    """
    try:
        iterations = int(iterations)
    except:
        print("Error, outer walls test, wrong argument type")
        return
    print("Starting outer walls test, running {} iterations".format(iterations,))
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

def solver_test(iterations=300, algo="DFS", expand="True"):
    """
    Test that algorithms are always solvable. Parameter algo is which algorithm to use,
    while expand is whether to make the maze larger over time.
    """
    try:
        iterations = int(iterations)
        algo = str(algo).upper()
        expand = str(expand).lower()
    except:
        print("Error, solver test, wrong argument type")
        return
    print("Starting solver test, running {} iterations, {} algorithm".format(iterations, algo))
    x = 3
    y = 3
    i = 0
    size_change = True
    while i < iterations:
        if i % 10000 == 0:
            print("Iteration: {}".format(i,)) 
        if size_change:
            print("Size is currently: {}.{}".format(x, y))
            size_change = False
        with suppress_stdout():
            grid, outer_walled = create_grid(x,y)
            s_pt, f_pt = create_endpoints(outer_walled)
            generate_maze(grid, s_pt, f_pt, algo)
            solution = find_solution(s_pt)
        assert solution != False, "Solution was False"
        assert solution[0] is s_pt, "Solution has faulty starting position"
        assert solution[-1] is f_pt, "Solution has faulty finish position"
        i += 1
        if i % 10 == 0 and expand == "true":
            x += 1
            size_change = True
        if i % 15 == 0 and expand == "true":
            y += 1
            size_change = True
    print("Find solution test finished successfully, {} iterations".format(i,))

@contextmanager
def suppress_stdout():
    """
    Used to suppress any unwanted output to console. This is used by the tests to stop any
    called method from cluttering the console, thus ensuring only test-relevant data is
    outputted.
    """
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

if __name__ == '__main__':
    """
    Add tests to available_tests as they are constructed. This allows calling from the
    command line. Example:
        $ python testcases.py sot 5500 PTF False
        will call solver test for 5500 iterations, with path to finish algorithm, 
        and no enlargening maze

    """

    # Dictionary of all available tests
    available_tests = {"owt": outer_walls_test,
                       "sot": solver_test }

    # Default behaviour if no cmd-line arguments were specified
    if len(sys.argv) == 1:
        print("No arguments specified, running default tests...")
        outer_walls_test()
        solver_test()
        print("Default tests finished, exiting...")
        sys.exit()

    for idx,x in enumerate(sys.argv):
        # First element in sys.argv is always the name of the file, skip it
        if x == "testcases.py":
            continue
        if x in available_tests.keys():
            args = []
            # Any data found between function name x and the next are used as arguments
            for i in range(idx+1, len(sys.argv)):
                if sys.argv[i] not in available_tests.keys():
                    args.append(sys.argv[i])
                else:
                    break
            # Call function with name x, and pass the arguments in args
            available_tests[x](*args)




