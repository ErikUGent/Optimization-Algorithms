number = int(input("Enter the number of installations: "))
print(number)

for i in range(number):
    address = input("Please give the address: ")
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="admin")
    location = geolocator.geocode(address)
    print(location.address)

    print((location.latitude, location.longitude))
