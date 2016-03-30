from tkinter import *
from tkinter import ttk


def display(grid):
    for column in grid:
        for cell in column:

            

    for x in range(5):
        for y in range(5):
            Label(text=(x,y), height=5, width=5).grid(row=y, column=x)


if __name__ == '__main__':
    display(5)
    root = Tk()

    root.mainloop()
