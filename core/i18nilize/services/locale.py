from geocoder import ip
from geopy.geocoders import Nominatim
from babel.languages import get_official_languages


def get_default_language():
    # get user's coordinates based on ip address
    g = ip('me')
    coord = str(g.latlng[0]) + ", " + str(g.latlng[1])

    # convert coordinates to country code
    geolocator = Nominatim(user_agent="localization_launchpad")
    location = geolocator.reverse(coord, exactly_one=True)
    address = location.raw['address']
    country_code = address["country_code"]

    # pick the first (most popular) language
    return get_official_languages(country_code)[0]
