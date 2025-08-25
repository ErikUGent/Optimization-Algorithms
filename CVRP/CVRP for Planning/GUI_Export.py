import tkinter as TK
from CVRP_Planning_for_One_Week_AIO import *

Routewind = TK.Tk()
Routewind.title("Planning results Qurtinz")

load_var=TK.StringVar()

r_dist = print_solution()

def getroute():
    load_total=load_var.get(r_dist)
    return load_total


TK.Label(Routewind, text = "Start and end vehicle 1").grid(row = 0) #'username' is placed on position 00 (row - 0 and column - 0)
TK.Entry(Routewind, textvariable = load_var).grid(row = 0, column = 1) # first input-field is placed on position 01 (row - 0 and column - 1)
button_1 = TK.Button(Routewind, text = "import", fg = "green", bg = "red", activebackground="green", command = getroute).grid(row = 0, column = 2)

Routewind.mainloop()
