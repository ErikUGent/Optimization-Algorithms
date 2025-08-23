import math, numpy as np
import json
from math import radians, cos, sin, asin, sqrt

rho = 1.225
alpha = math.radians(90)
num_birds = 26

num_birds_ref = num_birds/2
ER_ref = 0.9
A_bird = 0.5
A_vert = A_bird
A_horz = A_bird*num_birds
A_squa = A_bird*np.sqrt(num_birds)
A_diam = A_bird*np.sqrt(num_birds)
A_vsha = (1.5*A_bird + (num_birds-3)*(A_bird/8))
sur_ref = A_vsha
CW_ref = 0.50

class Windmill:
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name

    def fuelcon(self, windmill):
        if self.x < windmill.x:
        #    if int(self.y) == int(windmill.y):
                r = 6373
                v_f = 10
                v_w = -5
                v_sq = (v_f + v_w)**2
                xDis = abs(math.radians(self.x) - math.radians(windmill.x))
                yDis = abs(math.radians(self.y) - math.radians(windmill.y))

                firstdis = abs(math.sin(xDis / 2)**2 + math.cos(self.x) * math.cos(windmill.x) * math.sin(yDis / 2)**2)
                distance = (2 * math.atan2(np.sqrt(firstdis), np.sqrt(1 - firstdis))) * r

                work_perf = ((((0.5*rho*v_sq*v_f*CW_ref*sur_ref)/ER_ref) - (0.5*rho*v_sq*((math.sin(alpha/2))**3)*v_w*CW_ref*sur_ref)))*distance

        #    else:
        #        r = 6373
        #        xDis = abs(math.radians(self.x) - math.radians(windmill.x))
        #        yDis = abs(math.radians(self.y) - math.radians(windmill.y))

        #        firstdis = abs(math.sin(xDis / 2)**2 + math.cos(self.x) * math.cos(windmill.x) * math.sin(yDis / 2)**2)
        #        distance = (2 * math.atan2(np.sqrt(firstdis), np.sqrt(1 - firstdis))) * r
        #        fuelcon = 1.1 * distance * 30 * 5.5 * (38.89 / (38.89 - 7.2))/1000
        #
        else:
            r = 6373
            v_f = 10
            v_w = 5
            v_sq = (v_f + v_w)**2
            xDis = abs(math.radians(self.x) - math.radians(windmill.x))
            yDis = abs(math.radians(self.y) - math.radians(windmill.y))

            firstdis = abs(math.sin(xDis / 2)**2 + math.cos(self.x) * math.cos(windmill.x) * math.sin(yDis / 2)**2)
            distance = (2 * math.atan2(np.sqrt(firstdis), np.sqrt(1 - firstdis))) * r
            work_perf = ((((0.5*rho*v_sq*v_f*CW_ref*sur_ref)/ER_ref) - (0.5*rho*v_sq*((math.sin(alpha/2))**3)*v_w*CW_ref*sur_ref)))*distance

        return work_perf

    def __repr__(self):
        
        return self.name

def jsonToData(file='Json-Data/Qurtinz_OK.json', datasetName='Qurtinz_dataset'):
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

fuelcons = 0

if fuelcons == 0:
    pathcons = 0
            
    for i in range(0, len(list_with_windmill_objects)):
        fromWindmill = list_with_windmill_objects[i]
        toWindmill = None

        if i + 1 < len(list_with_windmill_objects):
            toWindmill = list_with_windmill_objects[i + 1]

        else:
            toWindmill = list_with_windmill_objects[i]

        pathcons += fromWindmill.fuelcon(toWindmill)
             
        fuelcons = pathcons
    

print(fuelcons)
