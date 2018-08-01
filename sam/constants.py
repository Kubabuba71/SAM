import os

# Constants related to weather functionality

DARKSKY_URL = 'https://api.darksky.net/forecast/04b3caa34ed42ad8bb58ccecee191e91/'

GOOGLE_MAPS_TIMEZONE_URL = 'https://maps.googleapis.com/maps/api/timezone/json'

GOOGLE_MAPS_TIMEZONE_KEY = os.environ['GOOGLE_MAPS_TIMEZONE_KEY']

GOOGLE_MAPS_GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

GOOGLE_MAPS_GEOCODE_KEY = os.environ['GOOGLE_MAPS_GEOCODE_KEY']

DAYLIGHT_SAVINGS = True
