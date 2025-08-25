
import googlemaps

# Perform request to use the Google Maps API web service
api_key = 'AIzaSyDhyx2JqH_Il1kLh4AH7_2cKAkul7yYpsM'# Google Maps API key
gmaps = googlemaps.Client(key=api_key)

origin = (50.9981542, 3.6426087)
destination = (50.9727618, 3.14627673318225)
result = gmaps.distance_matrix(origin, destination) 

distance_in_meters = result['rows'][0]['elements'][0]['distance']['text']
time_taken = result['rows'][0]['elements'][0]['duration']['text']

print(time_taken)
print()