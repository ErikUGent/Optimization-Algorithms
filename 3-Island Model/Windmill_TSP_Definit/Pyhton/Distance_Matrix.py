import sys
import pandas as pd
#import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, sqrt, atan2, radians
import googlemaps
import json

#np.set_printoptions(threshold=sys.maxsize)
api_key = 'AIzaSyDhyx2JqH_Il1kLh4AH7_2cKAkul7yYpsM'#enter Google Maps API key
gmaps = googlemaps.Client(key=api_key)

def jsonData(file='Json-Data/Qurtinz.json', datasetName='Qurtinz_dataset'):
    with open(file, 'r') as f:
        datasetsdict = json.load(f)
    jsondata = datasetsdict[datasetName]
    return jsondata

data_d = jsonData()
i_max = len(data_d)
cols = ['LATITUDE', 'LONGITUDE']
lat_long = pd.DataFrame(columns=cols, index=range(i_max))
print(lat_long)

#for i in range(number):
for x in data_d:
    address = [x['Address']]
    #address = [x['Addres'] for x in data_d]
    y = data_d.index(x)
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="admin")
    location = geolocator.geocode(address)
    print(location.address)
    print((location.latitude, location.longitude))
    lat_long.loc[y].LATITUDE = location.latitude
    lat_long.loc[y].LONGITUDE = location.longitude
    print (lat_long)


#lat_long

#test = lat_long.iloc[2:,:]

def distance(city1, city2):
    
    api_key = 'AIzaSyDhyx2JqH_Il1kLh4AH7_2cKAkul7yYpsM'#enter Google Maps API key
    gmaps = googlemaps.Client(key=api_key)
    
    lat1 = city1['LATITUDE']
    lon1 = city1['LONGITUDE']
    lat2 = city2['LATITUDE']
    lon2 = city2['LONGITUDE']

    origin = (lat1, lon1)
    destination = (lat2, lon2)
    result = gmaps.distance_matrix(origin, destination) 

    print(result)
    #distance_in_meters = result['rows'][0]['elements'][0]['distance']['text']
    time_taken_s = result['rows'][0]['elements'][0]['duration']['value']
    time_taken = (time_taken_s/60)
    
    #return distance_in_minutes
    return round(time_taken)
    
#def dist_matrix():
dist_matrix = [[0 for x in range(i_max)] for y in range(i_max)] 
    #dist_matrix = np.zeros([lat_long.shape[0],lat_long.shape[0]])
for i1, city1 in lat_long.iterrows():
    for i2, city2 in lat_long.iloc[i1+1:,:].iterrows():
        dist_matrix [i1][i2] = distance(city1, city2)
        dist_matrix [i2][i1] = distance(city2, city1)
print (dist_matrix)
    
#    with open('Dist.txt', mode='w') as file_object:
#        print(dist_matrix, file=file_object)

#    return (dist_matrix)