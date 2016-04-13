from cell import Cell
from activator import Activator
from activator_cell import ActivatorCell
from module import Module

class Branch:
    """
    A Branch is a list of cells, and contains a list of other
    branches that branch out from this branch. They also know
    which cell (in another branch) they are connected to.
    """

    def __init__(self, parent):
        self.parent = parent
        self.cells = []
        self.children = []
        self.activators = []

    def update_activators(self):
        """
        Updates the list of contained activators. Call this
        after changing a Cell into an ActivatorCell.
        """
        for cell in self.cells:
            if isinstance(cell, ActivatorCell):
                self.activators.extend(cell.get_activators)

    def add_branch(self, other):
        """
        Add a branch to this branch's children, and make sure
        they are in order.
        """
        i = self.cells.index(other.parent)
        for idx,branch in enumerate(self.children):
            if i < self.cells.index(branch.parent):
                self.children.insert(idx, other)
                break
        else:
            self.children.append(other)

    def find(self, cell):
        """Return the branch that contains cell."""
        if cell in self.cells:
            return self
        elif not self.children:
            return None
        else:
            for branch in self.children:
                result = branch.find(cell)
                if result is not None:
                    return result


    def sub_branch(self, module):
        """
        Return the part of the branch that is 
        behind given module (including the module).
        Return this as a new Branch. If module is not
        found in this branch, return False.
        """
        try:
            idx = self.children.index(module)
            children = self.children[idx:]
            if idx >= 1:
                parent = self.children[idx-1]
            else:
                parent = self.parent
            branch = Branch(children, parent)
        except ValueError:
            return False

    def get_basic_tree(self):
        """Recursively find all branches in this branch."""
        if not self.children:
            return []
        else:
            temp = []
            for branch in self.children:
                temp.extend(get_basic_tree(branch))
            return temp

    def get_extensive_tree(self):
        """
        Find all branches in this branch, and for all activators
        in these branches, find their modules branches.
        """
        branches = self.get_basic_tree()
        for b in branches:
            for cell in b.activators:
                branches.extend(cell.module.branch.get_basic_tree())
        return branches

    def prev(self, cell):
        """Return the cell that is before specified cell."""
        idx = self.cells.index(cell)
        if idx <= 0:
            raise IndexError("No cell before this")
        else:
            return self.cells[idx-1]

    def next(self, cell):
        """Return the cell that is after specified cell."""
        idx = self.cells.index(cell)
        if idx >= len(self.cells):
            raise IndexError("No cell after this")
        else:
            return self.cells[idx+1]

    def __str__(self):
        """
        Return a formatted string with all relevant data about
        this branch.
        """
        me = "Branch is connected to {}\n".format(self.parent,)
        me += "Branch length is {}\n".format(len(self.cells),)
        me += "Cells: \n"
        for cell in self.cells:
            me += cell.coords()
            me += '\n'

        me += "\n----------"
        return me


    def __len__(self):
        return len(self.children)




