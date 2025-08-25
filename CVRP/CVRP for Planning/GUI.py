import tkinter as tk

window = tk.Tk()
window.title("Vehicle Routing Planning for Qurtinz")

veh1 = 0
veh1_var=tk.StringVar()
veh2_var=tk.StringVar()
veh3_var=tk.StringVar()
veh4_var=tk.StringVar()
veh5_var=tk.StringVar()
veh6_var=tk.StringVar()

def submit_veh1():
    veh1=veh1_var.get()
    if int(veh1) in range(0, 3):
        return veh1
    else:
        button_1.configure(text = "NOK")
        top= tk.Toplevel(window)
        top.geometry("310x75")
        top.title("Verkeerde waarde")
        tk.Label(top, text= "Kies als waarde 0, 1 of 2", font=('Code 18 bold'), foreground = "red").place(x=10,y=20)

def submit_veh2():
    veh2=veh2_var.get()
    if int(veh2) in range(0, 3):
        return veh2
    else:
        button_2.configure(text = "NOK")
        top= tk.Toplevel(window)
        top.geometry("310x75")
        top.title("Verkeerde waarde")
        tk.Label(top, text= "Kies als waarde 0, 1 of 2", font=('Code 18 bold'), foreground = "red").place(x=10,y=20)

def submit_veh3():
    veh3=veh3_var.get()
    if int(veh3) in range(0, 3):
        return veh3
    else:
        button_3.configure(text = "NOK")
        top= tk.Toplevel(window)
        top.geometry("310x75")
        top.title("Verkeerde waarde")
        tk.Label(top, text= "Kies als waarde 0, 1 of 2", font=('Code 18 bold'), foreground = "red").place(x=10,y=20)

def submit_veh4():
    veh4=veh4_var.get()
    if int(veh4) in range(0, 3):
        return veh4
    else:
        button_4.configure(text = "NOK")
        top= tk.Toplevel(window)
        top.geometry("310x75")
        top.title("Verkeerde waarde")
        tk.Label(top, text= "Kies als waarde 0, 1 of 2", font=('Code 18 bold'), foreground = "red").place(x=10,y=20)

def submit_veh5():
    veh5=veh5_var.get()
    if int(veh5) in range(0, 3):
        return veh5
    else:
        button_5.configure(text = "NOK")
        top= tk.Toplevel(window)
        top.geometry("310x75")
        top.title("Verkeerde waarde")
        tk.Label(top, text= "Kies als waarde 0, 1 of 2", font=('Code 18 bold'), foreground = "red").place(x=10,y=20)

def submit_veh6():
    veh6=veh6_var.get()
    if int(veh6) in range(0, 3):
        return veh6
    else:
        button_6.configure(text = "NOK")
        top= tk.Toplevel(window)
        top.geometry("310x75")
        top.title("Verkeerde waarde")
        tk.Label(top, text= "Kies als waarde 0, 1 of 2", font=('Code 18 bold'), foreground = "red").place(x=10,y=20)

# Text labels for depot vehicles
tk.Label(window, text = "Start and end vehicle 1").grid(row = 0)
tk.Entry(window, textvariable = veh1_var).grid(row = 0, column = 1)
button_1 = tk.Button(window, text="Submit", foreground="white", background="grey", command = submit_veh1)
button_1.grid(row = 0, column = 2)

tk.Label(window, text = "Start and end vehicle 2").grid(row = 1)
tk.Entry(window, textvariable = veh2_var).grid(row = 1, column = 1)
button_2 = tk.Button(window, text="Submit", foreground="white", background="gray", command = submit_veh2)
button_2.grid(row = 1, column = 2)

tk.Label(window, text = "Start and end vehicle 3").grid(row = 2)
tk.Entry(window, textvariable = veh3_var).grid(row = 2, column = 1) 
button_3 = tk.Button(window, text="Submit", foreground="white", background="gray", command = submit_veh3)
button_3.grid(row = 2, column = 2)

tk.Label(window, text = "Start and end vehicle 4").grid(row = 3) 
tk.Entry(window, textvariable = veh4_var).grid(row = 3, column = 1) 
button_4 = tk.Button(window, text="Submit", foreground="white", background="gray", command = submit_veh4)
button_4.grid(row = 3, column = 2)

tk.Label(window, text = "Start and end vehicle 5").grid(row = 4) 
tk.Entry(window, textvariable = veh5_var).grid(row = 4, column = 1) 
button_5 = tk.Button(window, text="Submit", foreground="white", background="gray", command = submit_veh5)
button_5.grid(row = 4, column = 2)

tk.Label(window, text = "Start and end vehicle 6").grid(row = 5) 
tk.Entry(window, textvariable = veh6_var).grid(row = 5, column = 1) 
button_6 = tk.Button(window, text="Submit", foreground="white", background="gray", command = submit_veh6)
button_6.grid(row = 5, column = 2)

tk.Label(window, text = "").grid(row = 6, columnspan = 3)
tk.Label(window, text = "0 = Evergem - 1 = Roeselare - 2 = Indy", foreground = "white", background = "red").grid(row = 7, columnspan = 3)
tk.Label(window, text = "").grid(row = 8, columnspan = 3)
tk.Button(window, text="Start Planning", fg = "red", command=window.destroy).grid(columnspan = 3) #button to close the window

window.mainloop()
