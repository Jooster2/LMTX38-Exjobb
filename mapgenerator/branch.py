from random import choice
from copy import copy

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

    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.cells = []
        self.childless_cells = []
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
        they are in order. This also removes the cell from
        the childless cells list.
        """
        try:
            i = self.cells.index(other.parent)
            try:
                self.childless_cells.remove(other.parent)
            except ValueError:
                # This may already be removed by another add
                pass
            for idx,branch in enumerate(self.children):
                if i < self.cells.index(branch.parent):
                    self.children.insert(idx, other)
                    break
            else:
                self.children.append(other)
        except ValueError as e:
            print(e)
            print(other.parent)

    def add_cell(self, cell):
        """
        Add a cell to this branch and to the childless 
        cells list.
        """
        self.cells.append(cell)
        self.childless_cells.append(cell)

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

    def get_parent(self):
        """
        Return the parent of this branch. If there is no parent 
        (i.e. this is top branch), return random cell in this
        branch, that has at least one unvisited neighbour.
        """
        if self.parent is None:
            temp = [cell for cell in self.cells \
                    if cell.has_unvisited_neighbours()]
            if temp:
                return choice(temp)
            else:
                return False
        else:
            return self.parent

    def get_by_name(self, name):
        """Recursively find and return a specific branch."""
        name = int(name)
        print("NS, entering",self.name)
        if self.name == name:
            print("NS, returning self")
            return self
        elif not self.children:
            return None
        else:
            for branch in self.children:
                chosen = branch.get_by_name(name)
                if chosen:
                    print("NS, got",chosen.name)
                if chosen is not None:
                    print("Name-searching, returning",chosen.name)
                    return chosen
            print("Name-searching, returning None (bad child)")
            return None

    def shortest(self, length=100):
        """
        Recursively find and return the branch with the fewest
        amount of cells.
        """
        length = int(length)
        if not self.children: 
            if len(self.cells) >= length:
                return None
            else:
                return self
        else:
            chosen = self
            length = len(self.cells)
            for branch in self.children:
                other = branch.shortest(length)
                if other:
                    if len(other.cells) < len(chosen.cells):
                        chosen = other
            return chosen
                
    def prev(self, cell):
        """Return the cell that is before specified cell."""
        if cell in self.cells:
            idx = self.cells.index(cell)
            if idx >= 1:
                return self.cells[idx-1]
            else:
                return False
        else:
            return False

    def next(self, cell):
        """Return the cell that is after specified cell."""
        if cell in self.cells:
            idx = self.cells.index(cell)
            if idx < len(self.cells):
                return self.cells[idx+1]
            else:
                return False
        else:
            return False

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
        """
        Recursively find and return the total amount of branches
        in this tree.
        """
        length = len(self.children)
        for branch in self.children:
            length += len(branch)
        return length




