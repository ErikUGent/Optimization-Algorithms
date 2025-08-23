from tkinter import *

ROOT = Tk()
ROOT.title("Windmill application")
FRAME = Frame(ROOT)
Grid.rowconfigure(ROOT, 0, weight=1)
Grid.columnconfigure(ROOT, 0, weight=1)
FRAME.grid(row=0, column=0, sticky=N+S+E+W)
GRID = Frame(FRAME)
GRID.grid(sticky=N+S+E+W, column=0, row=7, columnspan=2)
Grid.rowconfigure(FRAME, 7, weight=1)
Grid.columnconfigure(FRAME, 0, weight=1)
BUTTONWIDTH = 8