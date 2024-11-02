# src/internationalize/helpers/location_singleton.py
from geopy.geocoders import Nominatim
from countryinfo import CountryInfo
import logging

# Configure logging
logging.basicConfig(
    filename='internationalize.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)
logger = logging.getLogger(__name__)

class LocationSingleton:
    _instance = None
    _language_mappings = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocationSingleton, cls).__new__(cls)
            cls._initialize(cls._instance)
        return cls._instance

    @classmethod
    def _initialize(cls, instance):
        # Initialize with dummy geolocation coordinates
        # Replace with actual geolocation when available
        dummy_coordinates = (40.7128, -74.0060)  # New York City
        language = cls.get_language_from_coordinates(dummy_coordinates)
        instance._language_mappings = language

    @staticmethod
    def get_language_from_coordinates(coordinates):
        lat, lng = coordinates
        geolocator = Nominatim(user_agent="geoapiExercises")
        try:
            location = geolocator.reverse((lat, lng), language='en')
            country = location.raw['address']['country_code'].upper()
            logger.info(f"Determined country code: {country} for coordinates: {coordinates}")
        except Exception as e:
            logger.error(f"Geocoding error for coordinates {coordinates}: {e}")
            return 'English'  # Default

        try:
            country_info = CountryInfo(country)
            languages = country_info.languages()
            logger.info(f"Languages for country {country}: {languages}")
            # Return the first language as primary
            if languages:
                return languages[0].capitalize()
            else:
                return 'English'
        except Exception as e:
            logger.error(f"CountryInfo error for country {country}: {e}")
            return 'English'  # Default

    def get_language(self):
        # Retrieve the language based on current mappings
        return self._language_mappings

    def add_mapping(self, location, language):
        self._language_mappings[location] = language

    def remove_mapping(self, location):
        if location in self._language_mappings:
            del self._language_mappings[location]