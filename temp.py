from geopy.geocoders import Nominatim

def get_lat_lon(location):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(location)
    if location:
        return location.latitude, location.longitude
    else:
        return None

if __name__ == '__main__':

    # Example usage
    print(get_lat_lon("Paravai, Madurai"))  # Output: (40.7127281, -74.0060152)
