from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

from cell import Cell
from leveled_cell import LeveledCell
from directions import Side, Corner

root = Tk()
root.attributes("-fullscreen", True)
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

def display(img_grid):
    """Take a 2d-grid of images and display them as labels."""
    for idx, col in enumerate(img_grid):
        for idy,img in enumerate(col):
            Label(root, image=img, bd=0).grid(
                    row=idy, column=idx)
    root.mainloop()



def create_cell_images(cell_grid, solution=[]):
    """Take a grid of cells, and create images for each of them.
       Draw black borders for any intact walls found."""
    img_grid = []
    # s_x = int(screen_w/len(cell_grid))
    s_y = int(screen_h/len(cell_grid[0]))
    # s_x is s_y so all cells are squares
    s_x = s_y
    e_x = int(s_x/2)
    e_y = int(s_y/2)
    w_x = int(s_x/16)
    w_y = int(s_y/16)

    for idx,col in enumerate(cell_grid):
        img_grid.append([])
        for cell in col:
            img = Image.new("RGB", (s_x, s_y), "blue")
            # Mark special cells with some nice colors
            if cell in solution:
                img.paste("purple", (e_x-20,e_y-20,e_x+20,e_y+20))
            if cell.is_start:
                img.paste("red", (e_x-20,e_y-20,e_x+20,e_y+20))
            if cell.is_finish:
                img.paste("green", (e_x-20,e_y-20,e_x+20,e_y+20))

            # Handle leveled cells.
            if isinstance(cell, LeveledCell):
                for key, value in cell.levels.items():
                    coords = corner_conversion(s_x, key)
                    if value == 0:
                        continue
                    elif value == 1:
                        img.paste("yellow", coords)
                    elif value == 2:
                        img.paste("orange", coords)
                    elif value == 3:
                        img.paste("brown", coords)

            # Handle walls.
            for wall in cell.get_walls():
                if wall is Side.UP:
                    img.paste("black", (0,0,s_x,w_y))
                elif wall is Side.RIGHT:
                    img.paste("black", (s_x-w_x,0,s_x,s_y))
                elif wall is Side.DOWN:
                    img.paste("black", (0,s_y-w_y,s_x,s_y))
                elif wall is Side.LEFT:
                    img.paste("black", (0,0,w_x,s_y))

            img_grid[idx].append(ImageTk.PhotoImage(img))
    return img_grid
    
def corner_conversion(size, corner):
    """Return a quad-tuple representing specified corner."""
    h_size = int(size/2)
    if corner is Corner.TOP_R:
        return (h_size,0,size,h_size)
    elif corner is Corner.BOT_R:
        return (h_size,h_size,size,size)
    elif corner is Corner.BOT_L:
        return (0,h_size,h_size,size)
    elif corner is Corner.TOP_L:
        return (0,0,h_size,h_size)


