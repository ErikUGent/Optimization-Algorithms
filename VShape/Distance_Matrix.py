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

def jsonData(file='JsonExport.json', datasetName='Qurtinz_dataset'):
    with open(file, 'r') as f:
        datasetsdict = json.load(f)
    jsondata = datasetsdict[datasetName]
    return jsondata

data_d = jsonData()
i_max = len(data_d)
cols = ['LATITUDE', 'LONGITUDE']
lat_long = pd.DataFrame(columns=cols, index=range(i_max))

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
    #print (lat_long)

'''
#Qurtinz
lat_long = pd.DataFrame({'LATITUDE':[51.13308, 50.91840, 51.20496, 50.92058, 50.89327, 51.07950, 51.11038, 50.78700, 51.30778, 50.97909, 51.13308, 50.97010, 51.05852, 51.04502, 51.09441, 50.89942, 51.03099, 51.30226, 50.99678, 50.98198, 51.13308, 50.96432, 50.92210, 51.21664, 50.93520, 50.87334, 51.26352, 51.02721, 50.97337, 50.92743, 51.13308, 51.20292, 51.32481, 51.07679, 50.91886, 51.22223, 50.95421, 51.07333, 50.82915, 50.89358, 51.13308], 'LONGITUDE': [3.74511, 2.63064, 4.40352, 5.25137, 5.64441, 3.76623, 3.70918, 3.50654, 4.46086, 3.00883, 3.74511, 4.63070, 4.81290, 3.73360, 3.71467, 3.19107, 3.77983, 4.43313, 4.98743, 3.57350, 3.74511, 4.51168, 2.96181, 4.23826, 4.46529, 3.63436, 3.55449, 4.05721, 4.58802, 4.52145, 3.74511, 4.41781, 4.52884, 3.68330, 4.98244, 3.74942, 4.53728, 3.74684, 4.25162, 4.11861, 3.74511]})

#lat_long

#test = lat_long.iloc[2:,:]
'''
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
    return round(time_taken, 2)
    
def dist_matrix():
    dist_matrix = [[0 for x in range(i_max)] for y in range(i_max)] 
    #dist_matrix = np.zeros([lat_long.shape[0],lat_long.shape[0]])
    for i1, city1 in lat_long.iterrows():
        for i2, city2 in lat_long.iloc[i1+1:,:].iterrows():
            dist_matrix [i1][i2] = distance(city1, city2)
            dist_matrix [i2][i1] = distance(city2, city1)
   
    
#    with open('Dist.txt', mode='w') as file_object:
#        print(dist_matrix, file=file_object)

    return (dist_matrix)