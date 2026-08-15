from weather import get_coordinates, get_weather

location = "Bhubaneswar"

lat, lon = get_coordinates(location)

print("Latitude :", lat)
print("Longitude:", lon)

weather = get_weather(lat, lon)

print(weather)