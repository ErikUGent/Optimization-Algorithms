import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, sqrt, atan2, radians

np.set_printoptions(threshold=sys.maxsize)

lat_long = pd.DataFrame({'LATITUDE':[51.330278, 51.6539, 51.64278, 51.63002, 51.62131, 51.66732, 56.72580, 53.27261, 53.27302], 'LONGITUDE': [3.206389, 2.817, 2.81062, 2.79656, 2.80156, 2.83209, -1.52460, 4.07229, 4.00878]})

lat_long

test = lat_long.iloc[2:,:]

def distance(city1, city2):
    lat1 = radians(city1['LATITUDE'])
    lon1 = radians(city1['LONGITUDE'])
    lat2 = radians(city2['LATITUDE'])
    lon2 = radians(city2['LONGITUDE'])

    R = 6373.0

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = round(R * c)
    
    return distance

dist = np.zeros([lat_long.shape[0],lat_long.shape[0]])
for i1, city1 in lat_long.iterrows():
    for i2, city2 in lat_long.iloc[i1+1:,:].iterrows():
        dist[i1,i2] = distance(city1, city2)
        dist[i2,i1] = distance(city2, city1)


    with open('Dist.txt', mode='w') as file_object:
        print(dist, file=file_object)