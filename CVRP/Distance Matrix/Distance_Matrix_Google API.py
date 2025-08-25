
import pandas as pd
import googlemaps
import json

api_key = 'AIzaSyDhyx2JqH_Il1kLh4AH7_2cKAkul7yYpsM'# Google Maps API key
gmaps = googlemaps.Client(key=api_key)

def jsonData(file='Json-Data/Qurtinz_OK.json', datasetName='Qurtinz_dataset'):
    with open(file, 'r') as f:
        datasetsdict = json.load(f)
    jsondata = datasetsdict[datasetName]
    return jsondata

data_d = jsonData()
i_max = len(data_d)
cols = ['LATITUDE', 'LONGITUDE']
lat_long = pd.DataFrame(columns=cols, index=range(i_max))

for x in data_d:
    coord_x = [x['x-cord']]
    coord_y = [x['y-cord']]
    y = data_d.index(x)

    lat_long.loc[y].LATITUDE = coord_x
    lat_long.loc[y].LONGITUDE = coord_y

def distance(city1, city2):
    
    api_key = 'AIzaSyDhyx2JqH_Il1kLh4AH7_2cKAkul7yYpsM' # Google Maps API key
    gmaps = googlemaps.Client(key=api_key)
    
    lat1 = city1['LATITUDE']
    lon1 = city1['LONGITUDE']
    lat2 = city2['LATITUDE']
    lon2 = city2['LONGITUDE']

    origin = (lat1, lon1)
    destination = (lat2, lon2)
    result = gmaps.distance_matrix(origin, destination) 

    time_taken_s = result['rows'][0]['elements'][0]['duration']['value']
    time_taken = (time_taken_s/60)

    return round(time_taken)
    
def dist_matrix():
    dist_matrix = [[0 for x in range(i_max)] for y in range(i_max)] 

    for i1, city1 in lat_long.iterrows():
        for i2, city2 in lat_long.iloc[i1+1:,:].iterrows():
            dist_matrix [i1][i2] = distance(city1, city2)
            dist_matrix [i2][i1] = distance(city2, city1)

    return (dist_matrix)
