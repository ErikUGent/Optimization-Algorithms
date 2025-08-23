import math, numpy as np
import json
from math import radians, cos, sin, asin, sqrt

class Windmill:
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name

    def distance(self, windmill):
        r = 6373
        xDis = abs(radians(windmill.x) - radians(self.x))
        yDis = abs(radians(windmill.y) - radians(self.y))

        firstdis = abs(sin(xDis / 2) ** 2 + cos(self.x) * cos(windmill.x) * sin(yDis / 2) ** 2)
        secdistance = 2 * asin(sqrt(firstdis))

        distance = secdistance * r
        return distance

    def __repr__(self):
        
        return self.name

def jsonToData(file='Windmills.json', datasetName='Windmill_dataset'):
    with open(file, 'r') as f:
        datasetsdict = json.load(f)
    jsondata = datasetsdict[datasetName]
    
    return jsondata

data = jsonToData()

list_with_windmill_names = [x['name'] for x in data]
list_with_windmill_cords = [[x['x-cord'], x['y-cord']] for x in data]

Aantal_WM = int(input("How many windmills are serviced?: "))
increment = 0
list_with_windmill_objects = []

while(increment < Aantal_WM):
    windmill = input('Please input the windmill to be serviced: ');
    if windmill in list_with_windmill_names:
        index = list_with_windmill_names.index(windmill)
        list_with_windmill_objects.append(Windmill(windmill, list_with_windmill_cords[index][0], list_with_windmill_cords[index][1]))
    else:
        print("Given windmill not in data")
        increment -= 1
    
    increment += 1
        
print(list_with_windmill_objects)

route_distance = 0

if route_distance == 0:
    pathDistance = 0

    for i in range(0, len(list_with_windmill_objects)):
        fromWindmill = list_with_windmill_objects[i]
        toWindmill = None

        if i + 1 < len(list_with_windmill_objects):
            toWindmill = list_with_windmill_objects[i + 1]

        else:
            toWindmill = list_with_windmill_objects[i]

        pathDistance += fromWindmill.distance(toWindmill)
             
        route_distance = pathDistance
    

print(route_distance)
