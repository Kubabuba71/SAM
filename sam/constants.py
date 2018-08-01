import os

# Constants related to weather functionality

DARK_SKY_URL = 'https://api.darksky.net/forecast/'

DARK_SKY_KEY = os.environ['DARK_SKY_KEY']

GOOGLE_MAPS_TIMEZONE_URL = 'https://maps.googleapis.com/maps/api/timezone/json'

GOOGLE_MAPS_TIMEZONE_KEY = os.environ['GOOGLE_MAPS_TIMEZONE_KEY']

GOOGLE_MAPS_GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

GOOGLE_MAPS_GEOCODE_KEY = os.environ['GOOGLE_MAPS_GEOCODE_KEY']

DAYLIGHT_SAVINGS = True
