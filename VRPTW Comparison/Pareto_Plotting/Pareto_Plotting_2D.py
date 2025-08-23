from tkinter import TRUE
import numpy as np
from matplotlib import pyplot as plt

def pareto_frontier(Xs, Ys, maxX = True, maxY = True):
# Sort the list in either ascending or descending order of X
    myList = sorted([[Xs[i], Ys[i]] for i in range(len(Xs))], reverse=maxX)
# Start the Pareto frontier with the first value in the sorted list
    p_front = [myList[0]]    
# Loop through the sorted list
    for pair in myList[1:]:
        if maxY: 
            if pair[1] >= p_front[-1][1]: # Look for higher values of Y…
                p_front.append(pair) # … and add them to the Pareto frontier
        else:
            if pair[1] <= p_front[-1][1]: # Look for lower values of Y…
                p_front.append(pair) # … and add them to the Pareto frontier
# Turn resulting pairs back into a list of Xs and Ys
    p_frontX = [pair[0] for pair in p_front]
    p_frontY = [pair[1] for pair in p_front]
    return p_frontX, p_frontY

Xs = 2037, 4444, 2032, 2436, 2128, 2156
Ys = 4200, 3180, 4200, 3900, 3600, 4080

p_front = pareto_frontier(Xs, Ys, maxX = True, maxY = True) 

plt.title('Pareto Front for VRPTW and JSS')
plt.xlabel('VRPTW Total Distance (km)')
plt.ylabel('Total time-span (min)')

plt.plot(p_front[0], p_front[1], c="r")
plt.show()