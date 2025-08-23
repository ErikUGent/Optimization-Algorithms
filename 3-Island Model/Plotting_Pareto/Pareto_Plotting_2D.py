from tkinter import TRUE, Label, LabelFrame
import numpy as np
from matplotlib import pyplot as plt

'''
Method to take two equally-sized lists and return just the elements which lie 
on the Pareto frontier, sorted into order.
Default behaviour is to find the maximum for both X and Y, but the option is
available to specify maxX = False or maxY = False to find the minimum for either
or both of the parameters.
'''
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

#Xs = 552.399, 573.162, 570.441, 573.096, 566.218, 551.527, 552.363, 544.728, 551.001, 555.247, 558.558, 555.831, 554.704, 554.642, 555.945, 556.976, 543.762, 558.768, 565.400, 565.663, 1528.289, 1744.133, 1676.524, 1587.176, 1535.32, 1500.968, 1599.195, 1743.962, 1598.201, 1681.214, 1948.782, 1476.887, 1775.074, 1412.388, 1791.971, 1796.079, 1721.398, 1668.313, 1805.871, 1634.085, 710.356, 725.870, 776.097, 756.267, 761.166, 775.543, 717.072, 693.115, 732.046, 594.689, 731.725, 839.773, 769.081, 746.297, 705.860, 667.059, 693.795, 822.060, 700.223, 786.874
Xs = 194.423, 200.962, 193.654, 208.462, 212.308, 180.385, 191.346, 187.115, 193.077, 190.192, 199.423, 199.038, 197.500, 167.692, 210.000, 211.538, 198.654, 180.000, 200.962, 185.000, 121.731, 119.808, 126.346, 124.038, 121.346, 120.962, 119.038, 121.731, 117.50, 122.500, 119.808, 121.346, 124.038, 120.962, 119.808, 120.962, 119.808, 119.231, 122.500, 122.500, 193.462, 183.269, 205.192, 244.808, 224.423, 209.231, 205.385, 214.808, 216.346, 214.038, 195.962, 207.500, 227.500, 175.962, 191.923, 201.346, 186.346, 198.462, 196.538, 222.115
Ys = 420859.329, 468045.928, 468884.984, 503444.808, 413118.505, 452099.598, 460502.631, 457898.937, 431217.596, 494802.095, 450013.508, 421626.618, 437563.851, 475284.512, 485466.912, 426611.508, 440060.078, 441698.162, 449890.495, 408527.011, 1337705.892, 1700920.811, 1410367.190, 1480340.031, 983949.957, 905699.713, 1301547.776, 1510284.518, 1385586.094, 1547183.896, 1376433.352, 1129943.041, 1248825.175, 957572.780, 1247021.305, 1632218.433, 1577443.985, 1201911.803, 1435398.518, 1257774.799, 346996.624, 366737.608, 327107.354, 330468.727, 363931.384, 339768.333, 349109.419, 347446.897, 347160.737, 342348.879, 335691.061, 361824.886, 359326.170, 336262.736, 356612.003, 339545.129, 324450.874, 354218.366, 336393.322, 361202.055
Ls = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60
# get your data from somewhere to go here
# Find lowest values for cost and highest for savings
p_front = pareto_frontier(Xs, Ys, maxX = False, maxY = False) 
# Plot a scatter graph of all results
plt.title('Pareto Front for TSP and Lateness')
plt.xlabel('TSP Distance (km)')
plt.ylabel('Lateness (min)')
plt.scatter(Xs, Ys, marker="d", c="b")

# Then plot the Pareto frontier on top
plt.plot(p_front[0], p_front[1], c="r")
plt.show()