import tkinter
from tkinter import *
from tkinter import ttk
import time

import Windmill_Functions_No_COR as WmF
import GUI_Config as GUIc

ACTIVE = "#ff0000"
INACTIVE = "#ffffff"

BUTTONLIST = []
COMBOBOXVALUE = None
ALLWINDMILLS = WmF.windmill_fill_list()
ALLWINDMILLNAMES = WmF.windmillObjToNames(ALLWINDMILLS)


def click(button) -> None:
    """ When we click the button, the background color changes from white to red, or vice versa.
        They are mentioned here as "ACTIVE" and "INACTIVE" variables.
    """
    if (button["bg"] != ACTIVE):
        button["bg"] = ACTIVE
    else:
        button["bg"] = INACTIVE


def startKnop(button):
    """[When the "startknop" is pushed, first of all we call the function in the Windmill_classes.py file to get the windmill list.
    Then we convert the list with Windmill objects into a list with only windlill names/codes.
    When passing through the Buttonlist, we check the ones that have satus "INACTIVE" and delete them from the name list.
    Then we go through the windmill objects in the Windmilllist and check whether the name of the Windmillobject is in the namelist.
    If this is the case, then we add Windmill-object to the resultlist. 
    Finally we call the "writeTo()"-function. This will write the resultst of the Genetic Algorithm to the especially created .md-file.]
    """
    start_time = time.time()
    button["bg"] = "#3dbf26"
    windmillList = ALLWINDMILLS
    resultList = []
    namelist = WmF.windmillObjToNames(windmillList)

    for btn in BUTTONLIST:
        if btn["bg"] == INACTIVE and btn["text"] in namelist:
            namelist.remove(btn["text"])

    for windmill in windmillList:
        if windmill.name in namelist:
            resultList.append(windmill)

    if len(resultList) > 1:
        if COMBOBOXVALUE != None:
            if COMBOBOXVALUE in WmF.windmillObjToNames(resultList):
                sortRoute = WmF.sortBestRoute(WmF.geneticAlgorithm(
                    population=resultList, popSize=100, eliteSize=20, mutationRate=0.01, generations=500), COMBOBOXVALUE)
                WmF.writeTo(f"{', '.join(WmF.windmillObjToNames(sortRoute))} |")
                WmF.writeTo(f"{round(time.time() - start_time, 4)} |")
                WmF.writeTo() 
            else:
                print(
                    "Please select a windmill that is part of the list!")
        else:
            print("Please select a windmill first!")
    else:
        print("Please select at least 2 windmills!")


def main(height=5, width=5):
    index = 1
    for y in range(height):
        for x in range(width):
            btn = tkinter.Button(GUIc.FRAME, bg=INACTIVE,
                                 width=GUIc.BUTTONWIDTH)
            if x == width - 1 and y == height - 1:
                btn["text"] = "Start"
                btn.grid(column=x, row=y, sticky=N+S+E+W)
                btn["command"] = lambda btn=btn: startKnop(btn)
            elif x == int(width) - 2 and y == int(height) - 1:
                wmcombo = ttk.Combobox(GUIc.FRAME, width=GUIc.BUTTONWIDTH)
                wmcombo['values'] = ALLWINDMILLNAMES

                def comboBoxClick(event):
                    global COMBOBOXVALUE
                    COMBOBOXVALUE = wmcombo.get()
                    print(f"Je hebt {wmcombo.get()} geselecteerd")

                wmcombo.bind("<<ComboboxSelected>>", comboBoxClick)
                wmcombo.grid(column=x, row=y, sticky=N+S+E+W)
            else:
                if len(ALLWINDMILLNAMES) >= index:
                    btn["text"] = ALLWINDMILLNAMES[index - 1]
                else:
                    btn["text"] = ""
                btn.grid(column=x, row=y, sticky=N+S+E+W)
                btn["command"] = lambda btn=btn: click(btn)
                BUTTONLIST.append(btn)
            index = index+1

    for x in range(width):
        Grid.columnconfigure(GUIc.FRAME, x, weight=1)

    for y in range(height):
        Grid.rowconfigure(GUIc.FRAME, y, weight=1)

    return GUIc.FRAME


if __name__ == "__main__":
    w = main(5, 7)
    tkinter.mainloop()
