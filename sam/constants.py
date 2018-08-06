import os

# Constants related to weather functionality

DARK_SKY_URL = 'https://api.darksky.net/forecast/'

DARK_SKY_KEY = os.environ['DARK_SKY_KEY']

GOOGLE_MAPS_TIMEZONE_URL = 'https://maps.googleapis.com/maps/api/timezone/json'

GOOGLE_MAPS_TIMEZONE_KEY = os.environ['GOOGLE_MAPS_TIMEZONE_KEY']

GOOGLE_MAPS_GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

GOOGLE_MAPS_GEOCODE_KEY = os.environ['GOOGLE_MAPS_GEOCODE_KEY']

DAYLIGHT_SAVINGS = True

# Constants related to the Spotify web API

SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

SPOTIFY_BASE_AUTHORIZATION_URL = os.environ.get('SPOTIFY_AUTHORIZATION_URL')
SPOTIFY_REDIRECT_URI = os.environ.get('SPOTIFY_REDIRECT_URI')
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

SPOTIFY_SCOPE = ['user-read-playback-state', 'user-read-currently-playing']
