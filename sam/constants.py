import os

# Constants related to weather functionality

DARK_SKY_URL = 'https://api.darksky.net/forecast/'
DARK_SKY_KEY = os.environ['DARK_SKY_KEY']

GOOGLE_MAPS_TIMEZONE_URL = 'https://maps.googleapis.com/maps/api/timezone/json'
GOOGLE_MAPS_TIMEZONE_KEY = os.environ['GOOGLE_MAPS_TIMEZONE_KEY']
GOOGLE_MAPS_GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
GOOGLE_MAPS_GEOCODE_KEY = os.environ['GOOGLE_MAPS_GEOCODE_KEY']
DAYLIGHT_SAVINGS = True

WEATHER_PARAMETERS = ['currently', 'minutely', 'hourly', 'daily', 'alerts', 'flags']

# Constants related to the Spotify API

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
SPOTIFY_BASE_AUTHORIZATION_URL = os.environ['SPOTIFY_AUTHORIZATION_URL']
SPOTIFY_REDIRECT_URI = os.environ['SPOTIFY_REDIRECT_URI']
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_SCOPE = ['user-read-playback-state', 'user-read-currently-playing', 'user-modify-playback-state',
                 'playlist-modify-public', 'playlist-modify-private']

# Constants related to the Google Calendar API

GOOGLE_CALENDAR_CLIENT_ID = os.environ['GOOGLE_CALENDAR_CLIENT_ID']
GOOGLE_CALENDAR_CLIENT_SECRET = os.environ['GOOGLE_CALENDAR_CLIENT_SECRET']
GOOGLE_CALENDAR_PROJECT_ID = os.environ['GOOGLE_CALENDAR_PROJECT_ID']
GOOGLE_CALENDAR_AUTHORIZATION_URI = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_CALENDAR_REDIRECT_URI = os.environ['GOOGLE_CALENDAR_REDIRECT_URI']
GOOGLE_CALENDAR_TOKEN_URI = 'https://www.googleapis.com/oauth2/v3/token'
GOOGLE_CALENDAR_SCOPE = os.environ['GOOGLE_CALENDAR_SCOPE']
GOOGLE_CALENDAR_CERTS_URI = 'https://www.googleapis.com/oauth2/v1/certs'
GOOGLE_CALENDAR_WRAPPER_STR = '_CALENDAR_WRAPPER'
GOOGLE_CALENDAR_CUSTOM_CALENDAR_IDS = os.environ['GOOGLE_CALENDAR_CUSTOM_CALENDAR_IDS'].split('_')

# Constants related to file serving

STATIC_FILES_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), 'static'))
SAMPLE_DIALOGFLOW_REQUESTS_DIRECTORY = os.path.abspath(os.path.join(STATIC_FILES_DIRECTORY,
                                                                    'sample_dialogflow_requests'))
SPOTIFY_PLAYLISTS_FILE = os.path.abspath(os.path.join(STATIC_FILES_DIRECTORY,
                                                      'spotify_playlists.json'))
# Constants related to dialogflow connection
DIALOGFLOW_CLIENT_ACCESS_TOKEN = os.environ['DIALOGFLOW_CLIENT_ACCESS_TOKEN']

# Constants related to inner SAM workings
NOT_IMPLEMENTED = 'Not implemented yet!'
SPOTIFY_WRAPPER_STR = '_SPOTIFY_WRAPPER'  # For logging
